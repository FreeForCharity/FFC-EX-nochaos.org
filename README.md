# FFC-EX-nochaos.org

Static GitHub Pages site for **NO CHAOS INC.** (nochaos.org), migrated from a live
Hostinger WordPress site as part of the Free For Charity WordPress-to-Pages migration
(Wave 1, epic
[FFC-Cloudflare-Automation#702](https://github.com/FreeForCharity/FFC-Cloudflare-Automation/issues/702)).

## What this is

- A full static capture of the WordPress site (16 pages + all media), taken 2026-07-12
  with `FFC-Static-Site-Capture-Tools`.
- **Fully localized assets**: Google Fonts (Inter) and all same-domain media are served
  from this repository (`public/external-assets/` holds former third-party assets).
  CI enforces this via `scripts/check_assets.py`.
- **Stripped**: WordPress REST/oEmbed/xmlrpc discovery links, emoji script,
  analytics/tracking scripts (WPMU DEV), comment forms, and the contact form — none of
  which can function on a static host.
- **Removed**: GiveWP donation-form iframes (the embed endpoints return 403 and cannot
  work statically) — replaced with a visible notice on the donate pages. Also removed
  theme-demo images pointing at dead template hosts (fk10.ejuwork.top,
  block20/block22.oitemplates.org, smartyrart.oidev.org) that were already broken on
  the live site.
- **FFC standard footer** injected on every page (attribution, hub login, copyright).

## Deployment

Deployed to the **default GitHub Pages URL**
(https://freeforcharity.github.io/FFC-EX-nochaos.org/) — no custom domain, no DNS
changes. Cutover is separately gated.

- `CI - Build and Test` validates structure and asset localization on every PR/push.
- `Deploy to GitHub Pages` runs after CI succeeds on `main` (static upload of `public/`).
- `Lighthouse CI` audits the deployed structure, staged under the repo subpath
  (pattern from FFC-EX-catnipandcattitude.org).

## Notes

- The site mentions "tax-deductible donations" but publishes no EIN or explicit
  501(c)(3) statement; the footer therefore carries the charity name only (never
  fabricate EIN/status).
- Online donation capability is lost in the static version — needs a follow-up decision
  (e.g. external donation processor link) before any cutover.
