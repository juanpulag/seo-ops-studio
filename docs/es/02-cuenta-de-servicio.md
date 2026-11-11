# Crear la cuenta de servicio de Google y conectarla

Una **cuenta de servicio** es un usuario técnico de Google que SEO Ops Studio usa para leer Search Console, GA4 y Tag Manager de tus clientes. La creas **una vez**. Cada cliente nuevo solo añade su correo como lector.

Tiempo estimado: 15-20 minutos.

## 1. Proyecto de Google Cloud

1. Entra en https://console.cloud.google.com/ con tu cuenta de trabajo.
2. Arriba, en el selector de proyectos → **Proyecto nuevo** → nombre, por ejemplo `seo-ops-studio` → Crear.

## 2. Habilitar las APIs

En **APIs y servicios → Biblioteca**, busca y pulsa **Habilitar** en cada una:

- Google Search Console API
- Google Analytics Data API
- Google Analytics Admin API
- Tag Manager API
- Chrome UX Report API
- PageSpeed Insights API
- Google Sheets API
- Google Drive API

## 3. Crear la cuenta de servicio

1. **IAM y administración → Cuentas de servicio → Crear cuenta de servicio.**
2. Nombre: `seo-ops-lectura`. No hace falta darle roles del proyecto → Listo.
3. Abre la cuenta → pestaña **Claves → Agregar clave → Crear clave nueva → JSON**. Se descarga un archivo.
4. Mueve ese archivo a una carpeta privada, por ejemplo `~/.config/seo-ops-studio/cuenta-servicio.json`. **No** lo dejes en Descargas ni en la carpeta de un cliente, y no lo compartas.

> En algunas organizaciones la creación de claves está bloqueada por política. Si ves ese error, pide a TI que la habilite para este proyecto o que te den una clave.

## 4. Clave de API (PageSpeed y CrUX)

**APIs y servicios → Credenciales → Crear credenciales → Clave de API.** Recomendado: **Restringir clave** → solo «PageSpeed Insights API» y «Chrome UX Report API».

## 5. Conectarla a SEO Ops Studio

Abre `~/.config/seo-ops-studio/google-api.json` (`/seo-ops-configurar` lo crea y abre la carpeta) y escribe **tú**:

```json
{
  "service_account_path": "~/.config/seo-ops-studio/cuenta-servicio.json",
  "api_key": "TU-CLAVE-DE-API",
  "default_property": null,
  "ga4_property_id": null
}
```

Las propiedades de cada cliente no van aquí: van en el `seo-ops.cliente.json` de su carpeta.

Verifica en Claude con `/seo-ops-configurar estado`. Te mostrará el **correo de la cuenta de servicio**, del tipo `seo-ops-lectura@seo-ops-studio.iam.gserviceaccount.com`.

## 6. Dar acceso en cada cliente

Con ese correo:

- **Search Console:** propiedad → Configuración → Usuarios y permisos → Añadir usuario → el correo → permiso **Restringido** (lectura).
- **GA4:** Administrar → Gestión de acceso a la propiedad → **+** → el correo → rol **Lector**.
- **Tag Manager** (opcional, para auditar analítica): Administrar → Gestión de usuarios del contenedor → el correo → **Lectura**.

Después, `/seo-ops-configurar` verifica que la cuenta ve sus propiedades.
