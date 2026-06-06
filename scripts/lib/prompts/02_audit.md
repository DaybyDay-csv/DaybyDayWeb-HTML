# 02_audit.md — Hormozi-style audit checklist adapted
# Used in step 6 of generate_post.py. ~3KB.

AUDITA el siguiente artículo con esta checklist DayByDay. Devuelve SOLO JSON.

```json
{
  "score_voz": 0-5,
  "score_estructura": 0-8,
  "score_contenido": 0-5,
  "score_antiia": 0-5,
  "score_seo": 0-4,
  "score_geo_aeo": 0-3,
  "score_total": 0-30,
  "lista_negra_count": 0+,
  "lista_negra_hits": ["término prohibido encontrado"],
  "verdict": "publicar" | "reescribir" | "regenerar",
  "bloques_a_reescribir": ["VOZ.1","CONT.2"],
  "feedback_especifico": "1-2 frases accionables si verdict != publicar"
}
```

## A · VOZ (5 ítems, todos obligatorios)
- VOZ.1: Frase media ≤ 12 palabras. Si pasa de 14 palabras en >30% de frases, fail.
- VOZ.2: Tuteo consistente (cero "el lector", "usted", "uno debería"). Tuteo: tú, te, tu, contigo.
- VOZ.3: Variación de ritmo — no 3 frases seguidas del mismo largo.
- VOZ.4: ≤ 2 adverbios en "-mente" en todo el artículo.
- VOZ.5: Cero jerga sin definir la primera vez (CAC, LTV, MER, CAPI, EMQ, COGS).

## B · ESTRUCTURA (8 ítems, mínimo 7 obligatorios)
- EST.1: Empieza con escena o cifra cruda. No intro genérica ("En este artículo vamos a…").
- EST.2: Abstract de 40-60 palabras en los primeros 200, contiene keyword principal verbatim.
- EST.3: Key takeaways en `<ul>` inmediatamente después del abstract.
- EST.4: 5-7 H2s, cada uno pregunta o afirmación con número/dato.
- EST.5: FAQ section con 5-7 Q&As en formato PAA, después del último H2.
- EST.6: CTA final con uno de: "Hablamos", "Auditoría gratuita", "Pedir diagnóstico" (enlaza a /contacto.html).
- EST.7: ≥ 1 tabla HTML con datos concretos (no decorativa).
- EST.8: ≥ 1 lista numerada o ranking ("Top 5", "7 señales", etc.).

## C · CONTENIDO (5 ítems, todos obligatorios)
- CONT.1: ≥ 5 cifras concretas (no "muchos", "varios", "diversos"). Cifras con formato español (3,2M€, 264.712€).
- CONT.2: ≥ 3 dispositivos retóricos (cadena lógica "Más X → más Y → más Z", negación encadenada "Aunque X, no Y", cifra que abofetea, pregunta retórica, regla de tres, auto-burla).
- CONT.3: ≥ 1 vulnerabilidad o "cagada propia" — ejemplo real con cifra de coste/resultado.
- CONT.4: ≥ 1 mención de cómo DayByDay lo hace (diferencial).
- CONT.5: ≥ 1 acción concreta que el lector puede hacer HOY (no "considera", sí "mide X en Y minutos").

## D · LISTA NEGRA (cero tolerancia)
Cualquier aparición de: "en el panorama actual", "en el mundo de hoy", "en la era digital", "verdaderamente", "sinceramente", "es importante destacar", "a nivel de", "en términos de", "holístico", "sinergia", "transversal", "como sabes", "como bien sabrás", "en definitiva", "a grosso modo", "libera tu potencial", "transforma tu negocio", "explora", "sumérgete", "click aquí", "pincha aquí".

## E · ANTI-IA (5 ítems, todos obligatorios)
- AI.1: No hay 3 bullets seguidos con la misma estructura sintáctica.
- AI.2: No hay frases repetidas literalmente dos veces.
- AI.3: No hay listas donde todos los items tienen el mismo largo exacto.
- AI.4: No hay arranques idénticos ("Además,", "Por otro lado,", "Asimismo,").
- AI.5: No hay "en conclusión", "en resumen", "para finalizar" como inicio de cierre.

## F · SEO (4 ítems, todos obligatorios)
- SEO.1: Title tag ≤ 60 caracteres, contiene keyword principal, formato "Tema: beneficio | DayByDay Consulting" (sin el sufijo, lo añade el template).
- SEO.2: Meta description ≤ 155 caracteres, contiene keyword principal, termina con CTA implícito.
- SEO.3: Keyword principal en H1 (lo pone el template), primer párrafo, ≥ 2 H2s.
- SEO.4: Slug kebab-case sin stop words (lo genera el script, no el LLM).

## G · GEO/AEO (3 ítems, todos obligatorios)
- GEO.1: Abstract de 40-60 palabras en los primeros 200 con respuesta directa citable.
- GEO.2: FAQ section con 5-7 Q&As PAA (1-2 frases, ≤ 40 palabras cada respuesta).
- GEO.3: ≥ 1 "cuándo NO" o contraargumento (evita tono sycophantic).

## Veredicto
- score_total ≥ 22: "publicar"
- 18 ≤ score_total < 22: "reescribir" con feedback_especifico
- score_total < 18: "regenerar"

## UMBRAL MÍNIMO
- lista_negra_count debe ser 0.
- score_voz ≥ 3, score_estructura ≥ 6, score_contenido ≥ 3, score_antiia ≥ 3, score_seo = 4, score_geo_aeo ≥ 2.
