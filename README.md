# SEO Ops Studio

**Auditorías SEO completas, con datos reales y un PDF listo para entregar, desde Claude Code.** En español.

Escribe `/seo-ops auditoria https://tusitio.com` y obtienes un informe con Health Score, problemas priorizados, plan de acción y un PDF con las fuentes de datos que se usaron (y las que no).

> 28 sub-skills y 19 sub-agents. Licencia MIT. Basado en [claude-seo](https://github.com/AgriciDaniel/claude-seo) de Daniel Agrici (ver `CREDITS.md`).

---

## Qué incluye

- **Onboarding de APIs guiado** (`/seo-ops-configurar`): crea las plantillas de credenciales, explica para qué sirve cada API y cuánto cuesta, guía la cuenta de servicio de Google paso a paso y verifica la conexión. Nunca te pide claves en el chat.
- **Auditoría completa con PDF** (`/seo-ops auditoria <url>`): especialistas en paralelo (técnico, contenido, schema, rendimiento, GEO, imágenes, sitemap…), Health Score ponderado y PDF con las fuentes reales.
- **Análisis sueltos** (`/seo-ops-analisis …`): técnico, contenido (E-E-A-T), schema, sitemap, Core Web Vitals, GEO para buscadores con IA, hreflang, SEO local, e-commerce, backlinks, clusters de keywords y más.
- **APIs conectadas**: Search Console, GA4, CrUX y PageSpeed (gratis), DataForSEO (pago por uso), Bing Webmaster y Moz (gratis).

## Comandos

| Comando | Qué hace |
|---|---|
| `/seo-ops` | Menú. En el primer uso lanza el onboarding |
| `/seo-ops-configurar` | Conecta y verifica las APIs |
| `/seo-ops auditoria <url>` | Auditoría completa → informe + PDF en `auditorias/<dominio>/` |
| `/seo-ops estado` | Qué APIs están conectadas y qué falta |
| `/seo-ops-analisis …` | Análisis sueltos del motor (`technical`, `content`, `schema`, `geo`, `hreflang`, `local`, `page`…) |

## Instalación

Requiere [Claude Code](https://claude.com/claude-code) y Python 3.11 to 3.14 (el plugin crea su propio entorno aislado).

```bash
/plugin marketplace add juanpulag/seo-ops-studio
/plugin install seo-ops-studio@seo-ops-studio
```

Reinicia Claude Code y, en cualquier carpeta, escribe `/seo-ops`.

> Todos los comandos empiezan por `/seo-ops`, así que SEO Ops Studio puede convivir con el claude-seo original.

Para actualizar:

```bash
/plugin marketplace update seo-ops-studio
/plugin update seo-ops-studio@seo-ops-studio
```

## Primeros pasos

1. `/seo-ops-configurar`: conecta al menos Google (cuenta de servicio + clave de API). Sin APIs también funciona, pero los datos de rendimiento y tráfico serán estimados.
2. Abre Claude Code en la carpeta donde quieras guardar las auditorías.
3. `/seo-ops auditoria https://tusitio.com`.

Guías en `docs/es/`:
- `01-apis.md`: qué APIs conectar y por qué.
- `02-cuenta-de-servicio.md`: crear la cuenta de servicio de Google paso a paso.

## SEO Ops Studio Premium

Para consultores y agencias que gestionan **varios clientes y muchos sitios**. Añade la metodología de operación:

| Básica (este repo) | Premium |
|---|---|
| Auditoría + PDF de un sitio | Auditoría por cliente, comparada con los demás sitios del cliente |
| Informe con hallazgos | Cada hallazgo se convierte en una tarea de un **backlog en Notion**, con evidencia, criterio de aceptación y cómo validarla, sin duplicados |
| No incluido | Detección de problemas de **plataforma** que se repiten entre sitios (una sola tarea, no treinta) |
| No incluido | Una carpeta, una memoria y un Notion **por cliente** |
| No incluido | Tablero en **Looker Studio** (GSC y GA4 nativos + datos de las auditorías) |
| No incluido | Prioridad calculada (impacto × severidad × alcance ÷ esfuerzo) y tablero de pendientes por país y severidad |

¿Te interesa? Abre un [issue](https://github.com/juanpulag/seo-ops-studio/issues) con el título «Premium».

## Seguridad

- Las credenciales viven solo en `~/.config/seo-ops-studio/` y en el conector de DataForSEO. Nunca en tu proyecto ni en Git.
- El plugin nunca te pide claves en el chat ni las imprime.
- Detalles en `SECURITY.md` y `PRIVACY.md`.

## Créditos

El motor de auditoría proviene de **claude-seo** (MIT) de Daniel Agrici, y el framework FLOW (CC BY 4.0) es del mismo autor. Detalles en `CREDITS.md` y `LICENSE`.
