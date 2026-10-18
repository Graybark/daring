# daring — Daring Dozen campaign archive

Public source repository for the Daring Dozen campaign browser, migrated from `Graybark/Doldrum`.

## GitHub Pages

**Website:** https://graybark.github.io/daring/

**Session 133:** https://graybark.github.io/daring/#133

The owner intentionally made this repository public and explicitly approved proceeding with both the repository and website public on 18 October 2026.

The website and repository are **public, not private or password-protected**. All material embedded in the browser is readable, including unrevealed material in older sessions and reference entries. Source files and the separate GM notes are also accessible in this public repository. Search-engine `noindex` directives are retained, but do not provide access control.

The `Build and publish archive` workflow rebuilds, checks, and deploys the browser whenever its source files change on `main`, and can be run manually from Actions. It verifies that the deployed archive includes Session 133. The latest Actions run is the publication status record.

Only `_site/index.html`, `_site/favicon.svg`, and `_site/.nojekyll` are deployed to Pages. Separate Markdown, the source PDF, Python code, and the separate Session 133 GM-note file are not copied into the Pages artifact; they remain publicly accessible on GitHub. Source links in the published browser point to this repository.

Under repository **Settings → Pages → Build and deployment**, Source is **GitHub Actions**. The workflow uses GitHub's official configure/upload/deploy actions and no longer requires the source repository to be private.

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

The Pages staging step preserves the offline document's content and design. It adjusts source links, removes misleading private-site labels from the published version, and retains search-indexing exclusions.

## Campaign continuity

- Keep played events separate from preparation. Mark uncertain details **To confirm**.
- Session 133's player-facing record is [DaringDozen133.md](Daring%20Dozen/Sessions/DaringDozen133.md).
- Its separate GM record is [sessions/gm/session-133.md](sessions/gm/session-133.md). That file is not embedded in Session 133's player recap or deployed to Pages, but it is publicly accessible in this repository.
- The complete browser is a GM archive, not a player-safe recap. Public publication does not change that content distinction.

## Migration scope

[Migration record](MIGRATION.md) identifies the verified source snapshot. The original Doldrum files were preserved, not deleted. This repository is a separate copy; edits are not automatically exchanged between the two repositories or with a Windows/OneDrive folder. Edits made here are automatically rebuilt and published through this site's workflow. Windows synchronization scripts were not carried over. The publishing workflow acts only on `Graybark/daring`; it does not change the visibility or files of `Graybark/Doldrum` or `Graybark/spell-balance`.

## Documentation

- [Configuring a GitHub Pages publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [Private Pages access control](https://docs.github.com/en/enterprise-cloud%40latest/pages/getting-started-with-github-pages/changing-the-visibility-of-your-github-pages-site)
- [Search-engine noindex directives](https://developers.google.com/search/docs/crawling-indexing/block-indexing)
