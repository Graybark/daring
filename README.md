# daring — Daring Dozen campaign archive

Private home for the Daring Dozen browser, migrated from `Graybark/Doldrum`.

## Open the document

The full document is [Daring Dozen/Sessions/index.html](Daring%20Dozen/Sessions/index.html). The root `index.html` opens that document and preserves session deep links such as `#133`.

The imported snapshot contains **133 sessions and 163 reference entries** across Characters, Encounters, Mythology, Factions, Culture and History, and Locations. Session 133, *Into Death Heart*, is included. All linked session Markdown and the reference source PDF are retained.

## Editing and rebuilding

Edit numbered Markdown files in `Daring Dozen/Sessions/`, not the generated HTML. Use the [_template.md](Daring%20Dozen/Sessions/_template.md) for future sessions. Reference facts are maintained in `Codex/campaign_reference.py`; the historical reference source is `Dungeons & Dragons.pdf`.

The `Build private archive` workflow regenerates the browser and runs its integrity checks when these source files change on `main`. It commits only the generated browser. This is a build workflow, **not** a Pages deployment or a Windows/OneDrive synchronization service.

To build manually with Python 3.12:

```sh
python -m pip install -r Codex/requirements-session-browser.txt
python Codex/build_session_browser.py
python Codex/test_session_browser.py
```

## Campaign continuity and privacy

- Keep played events separate from preparation. Mark uncertain details **To confirm**.
- Session 133's player-facing record is [DaringDozen133.md](Daring%20Dozen/Sessions/DaringDozen133.md).
- Its separate private GM record is [sessions/gm/session-133.md](sessions/gm/session-133.md). That record is not embedded in the player recap.
- The complete browser is a **private GM archive**, not a player-safe public website; older sessions and reference entries can contain unrevealed material.
- The repository must remain private. No Pages site has been enabled during this migration.

## Pages publication: awaiting private hosting eligibility

A private GitHub repository does not make its GitHub Pages website private. GitHub's access-controlled private Pages requires a private or internal project repository owned by an organization using **GitHub Enterprise Cloud**. `Graybark/daring` currently belongs to a personal account, so it cannot provide that access control in its present location.

Official documentation: [Changing the visibility of your GitHub Pages site](https://docs.github.com/en/enterprise-cloud%40latest/pages/getting-started-with-github-pages/changing-the-visibility-of-your-github-pages-site).

The build workflow intentionally refuses to proceed if this repository becomes public or Pages is enabled. Configure and verify genuinely private hosting before changing that guard. `noindex`, a hidden URL, or a client-side password screen is not a substitute for access control.

## Migration scope

[Migration record](MIGRATION.md) identifies the verified source snapshot. The original files in Doldrum were preserved, not deleted. This repository is a separate copy; edits are not automatically exchanged between the two repositories or with a Windows folder. Windows synchronization scripts were not carried over.
