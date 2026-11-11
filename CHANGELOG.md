# Changelog

Todos los cambios relevantes de SEO Ops Studio se registran aquí. Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/); versiones según [SemVer](https://semver.org/lang/es/).

## [0.1.0] - 2026-11-10

Primera versión pública (edición básica).

### Añadido
- `/seo-ops`: menú, detección del primer uso y auditoría completa de un sitio con informe y PDF (`/seo-ops auditoria <url>`).
- `/seo-ops-configurar`: onboarding de APIs (Google, DataForSEO, Bing, Moz) con plantillas de credenciales que nunca se sobrescriben y verificación que nunca imprime secretos.
- `scripts/ops_setup.py` (plantillas y estado de las APIs) y `scripts/ops_pdf.py` (PDF con las fuentes de datos reales, sin depender de WeasyPrint).
- Guías en español: `docs/es/01-apis.md` y `docs/es/02-cuenta-de-servicio.md`.

### Cambiado respecto a claude-seo v2.5.0
- Todos los comandos usan el prefijo `/seo-ops`: el orquestador `/seo` pasa a `/seo-ops-analisis` y cada skill y agente `seo-X` a `seo-ops-X`, para convivir con el plugin original.
- Lanzador `scripts/seo-ops`, variables `SEO_OPS_*` y configuración en `~/.config/seo-ops-studio/`.

El historial del motor de auditoría anterior a este fork está en el [CHANGELOG de claude-seo](https://github.com/AgriciDaniel/claude-seo/blob/main/CHANGELOG.md).
