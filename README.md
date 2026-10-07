# Fanny Fushayi’s portfolio

A static personal website at **fushayifanny.co.za**. Root-level HTML URLs and the existing `CNAME` are retained. There is no frontend framework, package manager or required hosting build step.

## Preview

With Node installed, run `node scripts/preview.cjs`, then open `http://127.0.0.1:8123`. The preview serves the custom 404 for unknown paths. Use an HTTP server rather than opening files directly: shared asset URLs are relative to the domain root.

## Shared presentation

- `home.css`: existing homepage art direction.
- `writing.css`: existing Writing landing-page art direction.
- `site.css`: shared shell, editorial layouts, mobile behaviour and accessibility.
- `site.js`: menu, scroll state, optional reveals and footer year.
- `writing-index.json`: article titles, URLs and categories for reading metadata and previous/next links.
- `scripts/build_site.py`: refreshes shared navigation/footer, page metadata and image dimensions in static HTML. Generated elements use `data-shared` markers. Python, lxml and Pillow are needed only for maintenance; the published website does not run Python.
- `templates/*.html.example`: adaptable starting points for new articles and case studies. Copy a template to a root-level HTML file and replace every TODO. Remove draft/noindex markers only after the content is approved.

Page-specific CSS and scripts remain where needed for technical diagrams, charts and existing article interactions. Core page presentation is controlled by `site.css`.

## Content maintenance

Edit article and case-study content directly in HTML, then run `python scripts/build_site.py`. Add new Writing entries to the index and the appropriate list in `blog.html`. Add new project previews to `Projects.html`; extend the `PROJECTS` set in the build script to give the new case study the Projects navigation state.

The industrial automation pages are **explicit drafts** awaiting factual details. See `IMPLEMENTATION_REPORT.md` for missing information and claims needing review. Do not publish client details, responsibilities or metrics that have not been verified.

`Images/optimized/` contains WebP derivatives of large referenced assets. Original images are retained for full-size diagrams and future exports. New images should receive meaningful alt text, dimensions and appropriate loading behaviour.

## Verification

`python scripts/check_static.py` checks local links, URL case, anchors, landmarks, metadata and changes to substantial paragraphs against Git HEAD. `python scripts/audit_site.py` refreshes the inventory and quantitative-claim review list.

`scripts/check_browser.cjs` uses Playwright and the locally bundled Edge/browser runtime to test all root pages at six viewport widths. `--acceptance` adds keyboard, interaction, no-JavaScript, reduced-motion, decoded-image and external-reference checks. Browser tooling is local verification infrastructure, not a website dependency. Results are saved in `qa/`; screenshots are intentionally ignored by Git.

The deployment configuration provided in this repository is the static site and `CNAME`. No remote publishing settings were changed. A root-level `404.html` is compatible with GitHub Pages’ custom error-page convention.
