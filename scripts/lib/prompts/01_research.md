# 01_research.md — research JSON contract
# Used in step 2 of generate_post.py. ~1KB.

Devuelve SOLO un JSON válido con esta estructura exacta. Sin texto adicional.

```json
{
  "keyword_principal": "string (3-5 palabras, sintagma exacto que la gente busca)",
  "keywords_secundarias": ["3-5 strings"],
  "search_intent": "transactional | commercial | informational",
  "abstract_60w": "string (40-60 palabras, respuesta directa y citable, contiene keyword verbatim)",
  "key_takeaways": ["3-5 bullets, 8-15 palabras cada uno, empiezan con verbo"],
  "h2_structure": [
    {"h2": "Pregunta o afirmación fuerte", "h3_subsections": ["opcional 1-3"]}
  ],
  "faqs": [
    {"q": "pregunta PAA realista", "a": "respuesta 1-2 frases, ≤ 40 palabras, dato concreto"}
  ],
  "internal_link_targets": ["slug1", "slug2", "slug3"],
  "external_authority_targets": [
    {"url": "https://...", "anchor": "texto ancla descriptivo", "domain": "facebook.com|google.com|...", "why": "una frase"}
  ],
  "table_concept": "título de tabla HTML a generar (ej: 'ROAS benchmark por sector España 2026')",
  "table_columns": ["col1","col2","col3"],
  "ranking_concept": "string (1 frase — qué ranking o lista numerada incluir)",
  "contrarian_angle": "string (1 frase — la tesis contraintuitiva o diferenciadora)",
  "internal_links_context": "para cada internal_link_targets, una frase de cómo enlazarlo"
}
```

Reglas duras (BREVEDAD):
- abstract_60w: MÁXIMO 45 palabras. Ni una más.
- h2_structure: 3 H2 exactos, cada uno ≤ 6 palabras.
- key_takeaways: 3 frases ≤ 12 palabras cada una.
- external_authority_targets: 2 URLs.
- internal_link_targets: 2 slugs.
- FAQs: 4 Q&As, cada respuesta ≤ 25 palabras.

Output total estimado: ~600 tokens. Si te excedes, el JSON se trunca.
