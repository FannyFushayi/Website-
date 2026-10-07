# Site audit

The repository was audited before edits. `site-audit-before.json` preserves the original 52-page inventory, local-reference problems and quantitative statements. `site-audit.json` records the resulting 58 root-level pages.

## Existing strengths

The homepage’s warm paper/ink palette, condensed typography, field photography and restrained editorial layout provide a clear identity. The Writing landing page already extends that identity and has useful category lists and search. The site has substantial technical and personal writing, real project photographs, diagrams, models and demonstrations.

## Architecture and deployment

The project consists of standalone HTML pages with inline CSS and scripts, two legacy standalone stylesheets, image/video assets and a custom-domain `CNAME`. There is no frontend framework, application router, package manifest or deployment workflow in the repository. Links serve as routes. The Git remote is a GitHub repository, but remote publishing settings were not available in the project.

## Main findings and resolution

- Deeper pages used unrelated navy, purple, white and dark themes; reusable static shell and editorial CSS now align them with the homepage.
- Projects used flat previews and modal-only detail. A hierarchy and direct case-study routes replace those modals, retaining all twelve original project/competition entries.
- The robot motor-driver page contained copied PV specifications and outcomes. Its content now comes from its own existing project notes.
- The contact form only logged personal information and showed an invented success message. It now offers working email and professional contact links.
- Decorative homepage statistics started at zero and described arbitrary counts. They were removed.
- Legacy article scripts intercepted all navigation links, animated decorative particles, invoked nonexistent charts or assumed missing text elements. These were repaired or removed; actual article controls and existing demos were retained.
- Incorrect local paths, capitalization and placeholder image endpoints were repaired or replaced with explicit TODOs.
- The original duplicate Writing prototype at `test.html` now redirects to `blog.html` with a visible fallback link.
- Article references and personal endnotes were checked against Git HEAD and preserved, including notes previously placed in footers.
- Large referenced images now have smaller derivatives, dimension attributes and appropriate loading behaviour. Project videos use controls and posters instead of autoplay.
- Shared semantic navigation, active states, keyboard focus, skip links, reduced motion, responsive widths and page-specific metadata were added.

## Content evidence

Project dates and tools were taken from existing content. The digit-recognizer preview was corrected to match the NumPy/MNIST implementation described in its article, rather than repeating the old preview’s unsupported CNN/deployment wording.

HESS figures are presented as model-based results, with their assumptions and baseline awaiting documentation. PV scenario costs are labelled as model outputs. Unsupported modal claims about braking recovery, diesel savings, efficiency and robot battery life are not repeated as achievements. The prior figures remain in the audit record for review. The flywheel article’s unconditional battery-lifespan claim was softened without inventing an alternative figure.

The four industrial automation case studies are visibly marked draft outlines and carry `noindex, follow`. Their proposed technologies are topics to confirm, not assertions of implementation.

## Verification and limits

See `qa/static-results.json`, `qa/browser-results.json`, `qa/acceptance-results.json` and `qa/external-results.json`. Browser checks cover every root route at six viewport sizes; additional checks cover keyboard interactions, no-JavaScript reading/navigation, reduced motion, decoded images and custom 404 behaviour.

External-reference checks cannot establish whether a restricted research article, private notebook or rate-limited service is available to an authenticated reader. Those results are retained for manual review. Existing remote ML services were preserved; this task did not upload images or run remote inference. No live deployment was performed.
