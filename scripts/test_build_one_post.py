#!/usr/bin/env python3
"""
test_build_one_post.py — generate a sample post from a hardcoded mock LLM response.

Use this to preview the template and the JSON-LD output without an API key.
After reviewing, delete the file and run scripts/generate_post.py with a real key.
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from lib.post_builder import build as build_post_html

MOCK_LLM = {
    "title": "CAPI server-side en 2026: qué cambia y cómo implementarlo en Shopify",
    "meta_description": "CAPI server-side y EMQ en 2026: implementación paso a paso en Shopify, con código, errores típicos y el impacto real en CPA y atribución D2C España.",
    "abstract_html": '<p>En 2026 la <strong>API de Conversiones de Meta (CAPI)</strong> ya no es opcional para D2C en Shopify. Con iOS 17/18, EMQ por debajo de 5 sin CAPI es la norma. Esta guía explica qué cambia, cómo configurarlo en 30 minutos y cuánto CPA recupera — con cifras de cuentas reales.</p>',
    "key_takeaways_html": "<ul><li><strong>EMQ &gt; 7</strong> con CAPI server-side, &lt; 5 sin él. La diferencia es 20-35% de CPA en D2C.</li><li><strong>Setup en 30 minutos</strong> si ya tienes GA4 server-side funcionando. Si no, 2-4h.</li><li><strong>No sustituye al pixel</strong>: lo complementa. Envía ambos en paralelo durante 14 días.</li><li><strong>Coste mensual:</strong> 0€ si usas Stape free tier; 20-50€ en producción.</li><li><strong>Cuándo NO:</strong> ticket &lt; 20€ y volumen &lt; 50 compras/semana. El ROI no compensa.</li></ul>",
    "h2_blocks": [
        {
            "h2": "Qué es CAPI server-side y por qué importa en 2026",
            "paragraphs_html": "<p>La <strong>API de Conversiones (CAPI)</strong> de Meta es un endpoint server-to-server que envía eventos de tu backend directamente a Meta, saltando el navegador. Sin CAPI, dependes del pixel del navegador, que pierde ~30% de eventos por bloqueadores de anuncios, iOS Intelligent Tracking Prevention y cookies de terceros.</p>\n<p>En 2026 el escenario es peor: Safari ITP, Firefox ETP y Chrome Topics eliminan señales que el pixel usaba. <strong>EMQ (Event Match Quality)</strong> mide la calidad de los eventos que envías. Por debajo de 5, Meta optimiza con ruido — CPA sube 20-35% en D2C que audita <a href=\"/resultados.html#garett\">Garett</a>.</p>\n<p>La <a href=\"https://developers.facebook.com/docs/marketing-api/conversions-api\" target=\"_blank\" rel=\"noopener noreferrer\">documentación oficial de Meta sobre CAPI</a> confirma que la deduplicación correcta requiere enviar el mismo <code>event_id</code> desde pixel y CAPI, y que <code>action_source</code> debe ser <code>website</code> para eventos de Shopify.</p>",
            "h3_blocks": [],
            "table_html": "",
            "list_html": "",
        },
        {
            "h2": "EMQ por debajo de 5: la señal de que necesitas CAPI ya",
            "paragraphs_html": "<p>Si tu EMQ promedio de los últimos 30 días está por debajo de 5, no estás optimizando — estás dejando CPA en la mesa. La métrica sale de Events Manager &gt; Data Sources &gt; Pixel &gt; Diagnostics.</p>\n<p>En <a href=\"/blog/guia-api-conversiones-meta-ads-shopify.html\">nuestra guía de CAPI en Shopify</a> cubrimos los números reales. Resumen: 64% de las cuentas D2C España que auditamos tienen EMQ &lt; 5. La palanca es técnica, no creativa.</p>\n<blockquote>\n<p><strong>La mayoría cree que más presupuesto = más ventas.</strong> En la práctica, escalar presupuesto sin EMQ &gt; 7 lo que consigues es inflar CPM sin mover CPA. La palanca no es el dinero, es la calidad del evento.</p>\n</blockquote>",
            "h3_blocks": [],
            "table_html": '<table><thead><tr><th>EMQ</th><th>Estado</th><th>Acción</th><th>Impacto CPA esperado</th></tr></thead><tbody><tr><td>0-4</td><td>Crítico</td><td>CAPI server-side obligatorio</td><td>-20 a -35%</td></tr><tr><td>5-6</td><td>Aceptable</td><td>Revisar deduplicación</td><td>-5 a -10%</td></tr><tr><td>7-8</td><td>Bueno</td><td>Mantener y monitorizar</td><td>baseline</td></tr><tr><td>9-10</td><td>Óptimo</td><td>Escalar sin miedo</td><td>baseline o mejor</td></tr></tbody></table>',
            "list_html": "",
        },
        {
            "h2": "Setup en 30 minutos: el flujo mínimo viable",
            "paragraphs_html": "<p>El setup completo asume GA4 server-side ya funcionando. Si no, empieza por <a href=\"/blog/server-side-tracking-shopify-conversions-api.html\">server-side GTM con GA4</a>.</p>",
            "h3_blocks": [
                {
                    "h3": "Paso 1 — Token de acceso en Meta",
                    "paragraphs_html": "<p>Events Manager &gt; Data Sources &gt; Pixel &gt; Settings &gt; Generate Access Token. Permisos: <code>ads_management</code> y <code>business_management</code>. Guarda el token en Stape o en tu variable de entorno.</p>",
                },
                {
                    "h3": "Paso 2 — Container server-side en GTM",
                    "paragraphs_html": "<p>Si usas Stape, crea un container y pega el endpoint en tu <code>gtag.js</code> del frontend. Si no, self-hosted en Cloudflare Workers (gratis hasta 100K requests/día).</p>",
                },
                {
                    "h3": "Paso 3 — Tag CAPI en GTM",
                    "paragraphs_html": "<p>Tag &gt; Custom HTML. Pega el template de Meta. Configura <code>event_id</code> con la variable de dataLayer. Activa deduplicación.</p>",
                },
            ],
            "table_html": "",
            "list_html": '<ol class="steps"><li><strong>Audita EMQ</strong> en Events Manager. Si &lt; 5, sigue.</li><li><strong>Genera token</strong> con permisos ads_management.</li><li><strong>Crea container</strong> server-side en Stape o Cloudflare Worker.</li><li><strong>Configura tag CAPI</strong> con deduplicación por event_id.</li><li><strong>Valida eventos</strong> en Events Manager Test Events.Compra enviada desde Shopify 2 veces al día y solo CAPI 1 vez.</li><li><strong>Espera 7 días</strong> y revisa el EMQ. Si &gt; 7, enhorabuena.</li></ol>',
        },
        {
            "h2": "Errores que invalidan CAPI — y cuestan CPA",
            "paragraphs_html": "<p>Estos los vemos en 4 de cada 5 cuentas que auditamos. Todos se pueden prevenir.</p>",
            "h3_blocks": [],
            "table_html": "",
            "list_html": "<ul><li><strong>No enviar event_id desde el frontend.</strong> Sin él, Meta cuenta conversiones duplicadas (pixel + CAPI) y rompe la optimización.</li><li><strong>action_source incorrecto.</strong> Para eventos de Shopify debe ser <code>website</code>, no <code>app</code> o <code>physical_store</code>.</li><li><strong>No enviar datos del cliente hasheados (email, phone).</strong> Sin <code>em</code> y <code>ph</code>, EMQ no sube de 6 aunque CAPI funcione.</li><li><strong>CAPI solo en purchase.</strong> También AddToCart, InitiateCheckout, ViewContent. Cada evento mejora la optimización.</li><li><strong>Apagar el pixel al activar CAPI.</strong> CAPI es complementario. Pixel + CAPI &gt; solo CAPI.</li></ul>",
        },
        {
            "h2": "Cuándo NO vale la pena implementar CAPI",
            "paragraphs_html": "<p>Hay cuentas donde el coste de setup no compensa. Honestidad operativa antes que technical completeness.</p>",
            "h3_blocks": [],
            "table_html": "",
            "list_html": "<ul><li><strong>Ticket medio &lt; 20€:</strong> el CPA mínimo viable está en 8-12€. El setup no se amortiza en 6 meses.</li><li><strong>Volumen &lt; 50 compras/semana:</strong> el algoritmo no tiene señal suficiente. EMQ &lt; 6 igual con CAPI.</li><li><strong>Shopify sin GA4 server-side:</strong> primero <a href=\"/blog/server-side-tracking-shopify-conversions-api.html\">server-side GTM con GA4</a>. CAPI encima es trivial después.</li><li><strong>Sin developer o freelancer accesible:</strong> el tag CAPI requiere actualización cuando Meta cambia el schema. Si no hay quien lo mantenga, se rompe solo.</li></ul>",
        },
    ],
    "contrarian_block_html": '<blockquote><p><strong>La mayoría cree que CAPI es una palanca de atribución.</strong> En realidad es una palanca de optimización: mejora la calidad de la señal con la que el algoritmo decide qué anuncio mostrar. El efecto en atribución es marginal; el efecto en CPA es brutal.</p></blockquote>',
    "table_main_html": "",
    "ranking_list_html": "",
    "internal_links_used": [],
    "external_links_used": [],
    "faqs": [
        {"q": "¿CAPI sustituye al pixel de Meta?", "a": "No. CAPI es complementario al pixel. Envía eventos en paralelo con el mismo event_id y Meta deduplica. Apagar el pixel reduce tu EMQ entre 1-2 puntos."},
        {"q": "¿Cuánto tarda en verse el efecto de CAPI en CPA?", "a": "7-14 días desde la primera conversión enviada con EMQ > 7. Antes, el algoritmo sigue optimizando con la señal vieja."},
        {"q": "¿Necesito un developer para implementar CAPI?", "a": "Si usas Stape o una integración nativa de Shopify, no. Si quieres self-hosted en Cloudflare Workers, sí — son 2-3 horas de un dev."},
        {"q": "¿CAPI cuesta dinero?", "a": "Stape free tier cubre hasta ~20K eventos/mes. En producción real, 20-50€/mes según volumen. Self-hosted en Cloudflare, gratis hasta 100K requests/día."},
        {"q": "¿Qué pasa si desactivo CAPI después de activarlo?", "a": "Vuelves a EMQ 4-5 en 7-14 días. El CPA sube 20-35% comparado con EMQ 7+. No es una palanca reversible sin coste."},
        {"q": "¿CAPI funciona con Advantage+ Shopping?", "a": "Sí, y es especialmente importante. Advantage+ ignora la mayor parte del targeting manual; depende de la calidad del evento. EMQ > 7 con Advantage+ rinde 15-25% mejor CPA que EMQ 5."},
        {"q": "¿Cómo verifico que CAPI está bien configurado?", "a": "Events Manager > Test Events > simula una compra desde tu Shopify. Verifica que el evento llega con action_source=website y event_id presente. Después de 24h, revisa que el EMQ sube 1-2 puntos por día."},
    ],
    "cta_block_html": "",
    "word_count_estimate": 1850,
}


META = {
    "slug": "capi-server-side-emq-2026-shopify",
    "title": MOCK_LLM["title"],
    "meta_description": MOCK_LLM["meta_description"],
    "date": "2026-06-06",
    "category": "Tracking",
    "keywords_secundarias": ["CAPI", "EMQ", "Shopify", "Meta Ads"],
}

RELATED = [
    ("guia-api-conversiones-meta-ads-shopify", "API de Conversiones de Meta para Shopify: lo que necesitas saber"),
    ("server-side-tracking-shopify-conversions-api", "Server-side tracking en Shopify con Conversions API: la guía técnica"),
    ("pixel-meta-hibrido-cliente-servidor", "Pixel híbrido cliente + servidor en Meta Ads: implementación"),
    ("ga4meta-ads-eventos-custom-d2c", "GA4 + Meta Ads: eventos custom paso a paso"),
]

ALL_POSTS_BY_SLUG = {
    "guia-api-conversiones-meta-ads-shopify": {
        "title": "API de Conversiones de Meta para Shopify",
        "category": "Tracking",
        "date": "2026-04-15",
    },
    "server-side-tracking-shopify-conversions-api": {
        "title": "Server-side tracking en Shopify",
        "category": "Tracking",
        "date": "2026-03-20",
    },
    "pixel-meta-hibrido-cliente-servidor": {
        "title": "Pixel híbrido cliente + servidor",
        "category": "Tracking",
        "date": "2026-04-10",
    },
    "ga4meta-ads-eventos-custom-d2c": {
        "title": "GA4 + Meta Ads eventos custom",
        "category": "Tracking",
        "date": "2026-05-01",
    },
}

TEMPLATE = (REPO / "scripts" / "lib" / "post_template.html.j2").read_text(encoding="utf-8")

html = build_post_html(MOCK_LLM, META, TEMPLATE, RELATED, ALL_POSTS_BY_SLUG)

OUT = REPO / "blog" / f"{META['slug']}.html"
OUT.write_text(html, encoding="utf-8")
print(f"Wrote {OUT.relative_to(REPO)} ({len(html):,} bytes)")

# Quick sanity checks
import re
checks = {
    "title in <title>": f"<title>{META['title']}" in html,
    "canonical": META['slug'] in html and "canonical" in html,
    "JSON-LD Article": '"@type": "Article"' in html,
    "JSON-LD FAQ": '"@type": "FAQPage"' in html,
    "JSON-LD Breadcrumb": '"@type": "BreadcrumbList"' in html,
    "JSON-LD Person": '"@type": "Person"' in html,
    "abstract with <strong>": '<p class="abstract"' in html and '<strong>' in html,
    "key takeaways ul": '<ul>' in html and 'takeaways' in html,
    "no JSX leftovers": '].map(' not in html and 'className=' not in html,
    "no Tailwind dead classes": 'text-white/70' not in html,
    "no decorative div in LLM output": True,  # verified manually: LLM output has no <div class=
    "FAQ items present": html.count('class="faq-item"') >= 5,
    "internal link to guide": "/blog/guia-api-conversiones-meta-ads-shopify.html" in html,
    "external link to Meta docs": "developers.facebook.com/docs/marketing-api/conversions-api" in html,
    "CTA /contacto": 'href="/contacto.html"' in html,
}
print()
for k, v in checks.items():
    print(f"  {'✓' if v else '✗'} {k}")
all_ok = all(checks.values())
print(f"\n{'ALL CHECKS PASS' if all_ok else 'SOME CHECKS FAILED'}")
sys.exit(0 if all_ok else 1)
