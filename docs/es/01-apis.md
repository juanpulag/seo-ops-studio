# APIs de SEO Ops Studio: qué conectar y por qué

Sin APIs, SEO Ops Studio audita con lo que ve desde fuera: HTML, cabeceras, sitemap y búsquedas web. Con ellas, cada auditoría usa **datos reales** y el backlog se prioriza por impacto medido. Conéctalas **una sola vez**: sirven para todos tus clientes.

## 1. Google: imprescindibles y gratis

Todas salen de **un proyecto de Google Cloud con una cuenta de servicio** (guía: `02-cuenta-de-servicio.md`).

| API | Para qué | Credencial |
|---|---|---|
| Google Search Console API | Clics, impresiones, CTR, posiciones, sitemaps e indexación (unos 16 meses de historial) | Cuenta de servicio, añadida como usuario en cada propiedad |
| URL Inspection API (parte de Search Console) | Cómo ve Google cada URL: indexación, canonical elegido, renderizado. Unas 2.000 consultas al día por propiedad | La misma cuenta de servicio |
| Google Analytics Data API (GA4) | Tráfico orgánico, páginas de entrada, conversiones | Cuenta de servicio con rol Lector en cada propiedad GA4 |
| Google Analytics Admin API | Listar propiedades y revisar la configuración de GA4 | La misma cuenta de servicio |
| Tag Manager API (lectura) | Auditar contenedores de GTM: etiquetas, activadores, Consent Mode | Cuenta de servicio con lectura en cada contenedor |
| Chrome UX Report (CrUX) API | Core Web Vitals reales (LCP, INP, CLS) | Clave de API |
| PageSpeed Insights API | Lighthouse sin el límite público (error 429) | Clave de API (la misma que CrUX) |
| Google Sheets API + Drive API | Escribir en Sheets los datos que Looker Studio no conecta de forma nativa | Cuenta de servicio |

**Looker Studio no necesita API**: se conecta de forma nativa a Search Console, GA4 y Sheets.

**No uses la Google Indexing API para páginas normales.** Google solo la admite para ofertas de empleo y transmisiones en vivo.

## 2. Gratis y complementarias

| API | Para qué | Dónde se guarda |
|---|---|---|
| Bing Webmaster Tools API | Indexación y backlinks en Bing (que alimenta a Copilot) | `backlinks-api.json` → `bing_api_key` |
| Moz API (nivel gratuito) | Autoridad de dominio y enlaces, como respaldo | `backlinks-api.json` → `moz_api_key` |
| Notion (conector de Claude, solo Premium) | Crear y actualizar el backlog de cada cliente | Conector de Notion en la app de Claude |

## 3. De pago: datos externos

| API | Para qué | Nota |
|---|---|---|
| **DataForSEO** | Posiciones reales por país e idioma, volúmenes, competencia, backlinks, Lighthouse a escala, menciones en LLMs | Pago por uso. Recomendado: cuenta con **correo de empresa** (límites más altos, soporte prioritario, sin verificación telefónica). Las credenciales de API no son las del inicio de sesión web |
| Semrush API | Llevar datos de Semrush a Claude y a Looker Studio | Normalmente requiere el plan Business más unidades de API aparte. Si solo usas Semrush desde su interfaz, no la necesitas |

## 4. Opcionales

Firecrawl (rastreo con JavaScript), Ahrefs o SE Ranking (alternativas a DataForSEO: elige una), Profound (visibilidad en IA), Gemini (solo para la extensión de imágenes). Se instalan desde `extensions/`.

## Lo mínimo para arrancar

1. Un proyecto de Google Cloud con: Search Console, Analytics Data, Analytics Admin, Tag Manager, CrUX, PageSpeed, Sheets y Drive.
2. Una cuenta de servicio (su archivo JSON) y una clave de API para CrUX y PageSpeed.
3. DataForSEO.
4. Bing Webmaster Tools.

## Seguridad

- Las credenciales viven en `~/.config/seo-ops-studio/` (solo tu usuario puede leerlas) o en el instalador de DataForSEO. Nunca en la carpeta de un cliente ni en Git.
- **No pegues claves en el chat.** Si lo haces por error, regenera la clave.
- Si trabajas con datos de clientes corporativos, confirma con su TI que pueden dar acceso de lectura a tu cuenta de servicio, y revisa si tu plan de Claude cumple sus requisitos de privacidad.
