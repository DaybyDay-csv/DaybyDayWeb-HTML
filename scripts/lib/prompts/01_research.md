# 01_research.md — research JSON contract
# Used in step 2 of generate_post.py. ~1.5KB.

Devuelve SOLO un JSON válido con esta estructura exacta. Sin texto adicional.

```json
{
  "keyword_principal": "string (3-5 palabras, sintagma exacto que la gente busca)",
  "keywords_secundarias": ["3-5 strings"],
  "search_intent": "transactional | commercial | informational",
  "abstract_60w": "string (40-45 palabras, respuesta directa y citable, contiene keyword verbatim)",
  "key_takeaways": ["3 bullets, 8-12 palabras cada uno, empiezan con verbo"],
  "h2_structure": [
    {"h2": "Pregunta o afirmación fuerte, ≤ 8 palabras", "h3_subsections": ["opcional 1-3"]}
  ],
  "faqs": [
    {"q": "pregunta PAA realista", "a": "respuesta 1 frase, ≤ 25 palabras, dato concreto"}
  ],
  "internal_link_targets": ["slug1", "slug2"],
  "external_authority_targets": [
    {"url": "URL del trusted_urls pool (NO inventes URLs)", "anchor": "texto ancla descriptivo", "domain": "facebook.com|google.com|shopify.com|...", "why": "una frase"}
  ],
  "table_concept": "título de tabla HTML a generar (ej: 'ROAS benchmark por sector España 2026')",
  "table_columns": ["col1","col2","col3"],
  "ranking_concept": "string (1 frase — qué ranking o lista numerada incluir)",
  "contrarian_angle": "string (1 frase — la tesis contraintuitiva o diferenciadora)",
  "internal_links_context": "para cada internal_link_targets, una frase de cómo enlazarlo"
}
```

## Reglas duras (BREVEDAD)
- abstract_60w: MÁXIMO 45 palabras. Ni una más.
- h2_structure: 3 H2 exactos, cada uno ≤ 8 palabras.
- key_takeaways: 3 frases ≤ 12 palabras cada una.
- external_authority_targets: 2 URLs DEL POOL (no inventes).
- internal_link_targets: 2 slugs.
- FAQs: 4 Q&As, cada respuesta ≤ 25 palabras.

Output total estimado: ~700 tokens. Si te excedes, el JSON se trunca.

## REGLA CRÍTICA: external_authority_targets
Las URLs externas deben venir EXCLUSIVAMENTE de la lista `trusted_urls_disponibles` que recibirás en el input del usuario. Esa lista está verificada y clasificada por cluster. Si ninguna URL del pool encaja con el topic, devuelve `external_authority_targets: []`. **JAMÁS inventes una URL.** Una URL inventada es peor que no tener enlace.

Por cada URL elegida, escoge un anchor text descriptivo de 2-5 palabras que refleje la página enlazada. No "click aquí", no "este post", no "pincha".
