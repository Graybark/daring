# daring — Daring Dozen campaign archive

Private source repository for the Daring Dozen campaign browser, migrated from `Graybark/Doldrum`.

## GitHub Pages publication

The owner requested public Pages publication after being informed that the website is not link-restricted. The repository must remain private. The intended site address is **https://graybark.github.io/daring/**, with Session 133 at **https://graybark.github.io/daring/#133**. A successful Pages deployment is required before these addresses work.

**The website is public, not private or password-protected.** Anyone can open, guess, or share its address. Search-engine `noindex` directives discourage indexing by cooperating engines; they are not access control. All campaign material already embedded in the browser is publicly readable, including any unrevealed material in older sessions and reference entries.

The `Build and publish archive` workflow rebuilds, checks, and deploys the document when its source files change on `main`. It publishes only `_site/index.html`, `_site/favicon.svg`, and `_site/.nojekyll`. The separate Markdown files, source PDF, Python code, and separate Session 133 GM-note file are **not** deployed. Source links in the published browser point back to the private repository and require authorized GitHub access.

Under repository **Settings → Pages → Build and deployment**, the source must be **GitHub Actions**. Pages from a private personal repository requires GitHub Pro or another eligible plan. Do not make this repository public to get around that requirement. The workflow uses GitHub's official configure/upload/deploy actions; initial Pages enablement may require a repository administrator to select the setting.

## Editing and rebuilding

Edit numbered Markdown files in `Daring Dozen/Sessions/`, not the generated HTML. Use the [_template.md](Daring%20Dozen/Sessions/_template.md) for future sessions. Reference facts are maintained in `Codex/campaign_reference.py`; the historical reference source is `Dungeons & Dragons.pdf`.

The full offline document is [Daring Dozen/Sessions/index.html](Daring%20Dozen/Sessions/index.html). The root repository `index.html` is an offline redirect, not the deployed Pages entry point. The Pages build stages the complete browser at the website root and preserves session links such as `#133`.

The imported snapshot contains **133 sessions and 163 reference entries** across Characters, Encounters, Mythology, Factions, Culture and History, and Locations. Session 133, *Into Death Heart*, is included.

To build manually with Python 3.12:

```sh
python -m pip install -r Codex/requirements-session-browser.txt
python Codex/build_session_browser.py
python Codex/test_session_browser.py
python Codex/build_pages.py
```

The Pages staging step does not modify the offline document's content or design. It adjusts source links, removes misleading private-site labels from the published version, and retains search-indexing exclusions.

## Campaign continuity

- Keep played events separate from preparation. Mark uncertain details **To confirm**.
- Session 133's player-facing record is [DaringDozen133.md](Daring%20Dozen/Sessions/DaringDozen133.md).
- Its separate private GM record is [sessions/gm/session-133.md](sessions/gm/session-133.md). That file is not embedded in Session 133's player recap or deployed to Pages.
- The complete browser is a GM archive, not a player-safe recap. Public publication does not change that content distinction.

## Migration scope

[Migration record](MIGRATION.md) identifies the verified source snapshot. The original Doldrum files were preserved, not deleted. This repository is a separate copy; edits are not automatically exchanged between the two repositories or with a Windows/OneDrive folder. Edits made here are automatically rebuilt for this site's deployment. Windows synchronization scripts were not carried over.

## Documentation

- [Creating a GitHub Pages site](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)
- [Private Pages access control](https://docs.github.com/en/enterprise-cloud%40latest/pages/getting-started-with-github-pages/changing-the-visibility-of-your-github-pages-site)
- [Search-engine noindex directives](https://developers.google.com/search/docs/crawling-indexing/block-indexing)
