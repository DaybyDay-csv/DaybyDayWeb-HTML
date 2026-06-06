#!/usr/bin/env python3
"""
markdown_parser.py — convert the M3 markdown output into the JSON shape
that post_builder.py expects.

Input: raw markdown string from M3
Output: dict with keys: title, meta_description, abstract_html,
        key_takeaways_html, h2_blocks, contrarian_block_html,
        table_main_html, faqs, internal_links_used, external_links_used,
        word_count_estimate
"""
import re
import json
from html import escape


def _strip_md_inline(text: str) -> str:
    """Convert <a href>...</a>, <strong>...</strong> etc. preserving them.
    Our markdown is hybrid — the LLM writes HTML inline. We keep <a>, <strong>, <em>.
    Other markdown like **bold** we convert to <strong>.
    """
    # Convert ** to <strong> (markdown bold)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # Convert _italic_ to <em>
    text = re.sub(r"(?<!\w)_(.+?)_(?!\w)", r"<em>\1</em>", text)
    return text.strip()


def _to_p(text: str) -> str:
    return f"<p>{_strip_md_inline(text)}</p>"


def parse(md: str) -> dict:
    out = {
        "title": "",
        "meta_description": "",
        "abstract_html": "",
        "key_takeaways_html": "",
        "h2_blocks": [],
        "contrarian_block_html": "",
        "table_main_html": "",
        "faqs": [],
        "internal_links_used": [],
        "external_links_used": [],
        "word_count_estimate": 0,
    }
    # Normalize: strip "Title:" / "Description:" prefixes from META block
    md = re.sub(r"\*\*Title:\*\*\s*([^\n]+)\n+\*\*Description:\*\*\s*([^\n]+)",
                r"Title: \1\nDescription: \2", md)
    # Also handle "# TITLE" (no colon) -> "# TITLE:"
    md = re.sub(r"^# TITLE\s*$", "# TITLE:", md, flags=re.MULTILINE)
    md = re.sub(r"^# META\s*$", "# META:", md, flags=re.MULTILINE)
    md = re.sub(r"^# ABSTRACT\s*$", "# ABSTRACT:", md, flags=re.MULTILINE)
    md = re.sub(r"^# TAKEAWAYS\s*$", "# TAKEAWAYS:", md, flags=re.MULTILINE)
    md = re.sub(r"^# CONTRARIAN\s*$", "# CONTRARIAN:", md, flags=re.MULTILINE)
    md = re.sub(r"^# TABLE\s*$", "# TABLE:", md, flags=re.MULTILINE)
    md = re.sub(r"^# FAQ\s*$", "# FAQ:", md, flags=re.MULTILINE)
    md = re.sub(r"^# H2\s*$", "# H2:", md, flags=re.MULTILINE)
    # Split on lines starting with # (our custom directives)
    sections = re.split(r"\n(?=# )", md)
    for sec in sections:
        sec = sec.strip()
        if not sec:
            continue
        first_line, _, rest = sec.partition("\n")
        first_line = first_line.strip()
        rest = rest.strip()
        if first_line == "# TITLE:":
            out["title"] = rest.strip()
        elif first_line == "# META:":
            # Try to extract title/description if formatted as "Title: X\nDescription: Y"
            m_t = re.search(r"(?im)^Title:\s*(.+)$", rest)
            m_d = re.search(r"(?im)^Description:\s*(.+)$", rest)
            if m_d:
                out["meta_description"] = m_d.group(1).strip()
            elif rest:
                out["meta_description"] = rest.strip()
        elif first_line == "# ABSTRACT:":
            out["abstract_html"] = _to_p(rest.strip())
        elif first_line == "# TAKEAWAYS:":
            bullets = []
            for line in rest.splitlines():
                line = line.strip()
                if line.startswith("- "):
                    bullets.append(f"<li>{_strip_md_inline(line[2:].strip())}</li>")
            if bullets:
                out["key_takeaways_html"] = "<ul>" + "".join(bullets) + "</ul>"
        elif first_line == "# CONTRARIAN:":
            # Could be a single line or blockquote-style
            content = _strip_md_inline(rest.strip())
            if not content.startswith("<blockquote"):
                content = f"<blockquote><p>{content}</p></blockquote>"
            else:
                content = content.replace("\n", " ")
            out["contrarian_block_html"] = content
        elif first_line == "# TABLE:":
            out["table_main_html"] = _to_html_table(rest.strip())
        elif first_line == "# FAQ:":
            # Each FAQ is "## question\nanswer"
            faq_blocks = re.split(r"\n(?=## )", rest)
            for fb in faq_blocks:
                fb = fb.strip()
                if not fb.startswith("## "):
                    continue
                q, _, a = fb.partition("\n")
                q = q[3:].strip()
                a = a.strip()
                if q and a:
                    out["faqs"].append({"q": q, "a": a})
        elif first_line.startswith("# H2:"):
            h2_title = first_line[5:].strip()
            # paragraphs are separated by blank lines
            paras = [p.strip() for p in re.split(r"\n\s*\n", rest) if p.strip()]
            paragraphs_html = "".join(_to_p(p) for p in paras[:2])
            block = {"h2": h2_title, "paragraphs_html": paragraphs_html, "h3_blocks": [], "table_html": "", "list_html": ""}
            # extract links used
            for p in paras:
                for m in re.finditer(r'<a\s+href="(/blog/[^"]+)"[^>]*>([^<]+)</a>', p):
                    out["internal_links_used"].append({"slug": m.group(1).replace("/blog/", "").replace(".html", ""), "anchor": m.group(2)})
                for m in re.finditer(r'<a\s+href="(https?://[^"]+)"[^>]*>([^<]+)</a>', p):
                    out["external_links_used"].append({"url": m.group(1), "anchor": m.group(2)})
            out["h2_blocks"].append(block)
    # Word count
    all_text = out["title"] + " " + out["abstract_html"] + " " + out["key_takeaways_html"] + " " + out["contrarian_block_html"]
    for blk in out["h2_blocks"]:
        all_text += " " + blk.get("paragraphs_html", "")
    text = re.sub(r"<[^>]+>", " ", all_text)
    text = re.sub(r"\s+", " ", text).strip()
    out["word_count_estimate"] = len(text.split())
    # Dedupe links (preserve order)
    seen_int = set()
    dedup_int = []
    for l in out["internal_links_used"]:
        k = l["slug"]
        if k in seen_int:
            continue
        seen_int.add(k)
        dedup_int.append(l)
    out["internal_links_used"] = dedup_int
    seen_ext = set()
    dedup_ext = []
    for l in out["external_links_used"]:
        k = l["url"]
        if k in seen_ext:
            continue
        seen_ext.add(k)
        dedup_ext.append(l)
    out["external_links_used"] = dedup_ext
    return out


def _to_html_table(md_table: str) -> str:
    """Convert a markdown pipe table to HTML."""
    lines = [l.strip() for l in md_table.splitlines() if l.strip() and "|" in l]
    if len(lines) < 2:
        return ""
    # Header
    header_cells = [c.strip() for c in lines[0].strip("|").split("|")]
    # Skip separator line (---|---|---)
    body_lines = lines[2:]
    thead = "<thead><tr>" + "".join(f"<th>{escape(c)}</th>" for c in header_cells) + "</tr></thead>"
    rows_html = []
    for line in body_lines:
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != len(header_cells):
            cells = (cells + [""] * len(header_cells))[:len(header_cells)]
        rows_html.append("<tr>" + "".join(f"<td>{escape(c)}</td>" for c in cells) + "</tr>")
    tbody = "<tbody>" + "".join(rows_html) + "</tbody>"
    return f"<table>{thead}{tbody}</table>"


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: markdown_parser.py <md_file>")
        sys.exit(1)
    md = open(sys.argv[1], encoding="utf-8").read()
    out = parse(md)
    print(json.dumps(out, ensure_ascii=False, indent=2))
