# Archive migration

Copied the verified Doldrum campaign-browser snapshot into Graybark/daring.
Imported 144 archive/source files, including sessions 1-133, all six reference categories,
the reference source PDF, five build/test modules, and the separate Session 133 GM notes.
The original Doldrum files have not been deleted or redirected.
Windows sync scripts and the historical import/migration scripts were deliberately not copied.

Source: Graybark/Doldrum, private-session-archive workflow run 39071790046,
artifact 12115755192, private-doldrum-session-archive.
Archive SHA-256: 2f5dfd8f6d457accedd3437db39364b159dfbcfb9319035245e47ae389724fb6
Verified source index Git blob: 82b1bfe645665bbc60db201a5a4199dec2c16a96

## Publication status at the time of migration

No Pages deployment was configured during the migration. The repository remained private.
GitHub Pages access-controlled private publication requires an organization using
GitHub Enterprise Cloud. A personal private repository does not provide private Pages.
No client-side password gate or noindex directive should be treated as access control.

## Subsequent publication request — 18 October 2026

The owner subsequently requested public Pages publication. At that stage, the plan was
for the source repository to remain private. A build/deployment workflow was added,
staging only the complete HTML browser, favicon and .nojekyll. Separate PDFs, Markdown,
Python code and separate GM-note files were excluded from the Pages artifact.

## Public repository approval — 18 October 2026

The owner made Graybark/daring public while enabling Pages. After being informed that
this also exposes the separate source documents and GM notes on GitHub, the owner
confirmed that the visibility change was intentional and approved proceeding.

The workflow's private-repository checks have therefore been removed. It remains scoped
to Graybark/daring on main and publishes only the browser, favicon and .nojekyll. Source
links point to this now-public repository. Search-engine noindex tags remain, without
implying access control. Original Doldrum files and repository visibility were not changed.
See README.md and the latest Actions run for the current deployment status.
