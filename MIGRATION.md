# Private archive migration

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

The owner subsequently requested: "I don't think my players would find it. Just publish it there."
The response explicitly clarified that anyone can open or guess the address, the website
will be public, and all content already embedded in the browser will be publicly readable.
The source repository must remain private.

A Pages build/deployment workflow was added for that request. It stages only the complete
HTML browser, favicon and .nojekyll. Separate PDFs, Markdown, Python code and separate
GM-note files are excluded from the public artifact. Source links lead to the private
GitHub repository. Search-engine noindex tags are retained, without implying access control.
See README.md and the latest Actions run for activation and deployment status.
