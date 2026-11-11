# Create the Google service account and connect it

A **service account** is a technical Google user that SEO Ops Studio uses to read your clients' Search Console, GA4 and Tag Manager. You create it **once**. Each new client only adds its email as a reader.

Estimated time: 15-20 minutes.

## 1. Google Cloud project

1. Go to https://console.cloud.google.com/ with your work account.
2. In the project selector at the top → **New project** → a name, for example `seo-ops-studio` → Create.

## 2. Enable the APIs

In **APIs & Services → Library**, search for and click **Enable** on each:

- Google Search Console API
- Google Analytics Data API
- Google Analytics Admin API
- Tag Manager API
- Chrome UX Report API
- PageSpeed Insights API

## 3. Create the service account

1. **IAM & Admin → Service Accounts → Create service account.**
2. Name: `seo-ops-read`. It needs no project roles → Done.
3. Open the account → **Keys** tab → **Add key → Create new key → JSON**. A file downloads.
4. Move that file to a private folder, for example `~/.config/seo-ops-studio/service-account.json`. **Do not** leave it in Downloads or in a client folder, and do not share it.

> Some organizations block key creation by policy. If you see that error, ask IT to allow it for this project or to give you a key.

## 4. API key (PageSpeed and CrUX)

**APIs & Services → Credentials → Create credentials → API key.** Recommended: **Restrict key** → only "PageSpeed Insights API" and "Chrome UX Report API".

## 5. Connect it to SEO Ops Studio

Open `~/.config/seo-ops-studio/google-api.json` (`/seo-ops-setup` creates it and opens the folder) and write, **yourself**:

```json
{
  "service_account_path": "~/.config/seo-ops-studio/service-account.json",
  "api_key": "YOUR-API-KEY",
  "default_property": null,
  "ga4_property_id": null
}
```

Each client's properties do not go here: they go in the `seo-ops.client.json` in the client's folder.

Verify in Claude with `/seo-ops-setup status`. It shows the **service account email**, like `seo-ops-read@seo-ops-studio.iam.gserviceaccount.com`.

## 6. Grant access for each client

With that email:

- **Search Console:** property → Settings → Users and permissions → Add user → the email → **Restricted** permission (read).
- **GA4:** Admin → Property access management → **+** → the email → **Viewer** role.
- **Tag Manager** (optional, to audit analytics): Admin → Container user management → the email → **Read**.

Then `/seo-ops-setup` verifies the account can see its properties.
