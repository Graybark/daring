"""Extract the named campaign reference pages from the OneNote PDF export."""

from __future__ import annotations

import html
import re
import unicodedata
from pathlib import Path

from pypdf import PdfReader

from campaign_reference import CAMPAIGN, GM_CHARACTER_NOTES


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Dungeons & Dragons.pdf"
SECTIONS = {
    "Characters": (164, 221),
    "Encounters": (6, 28),
    "Mythology": (254, 262),
    "Factions": (229, 232),
    "Culture and History": (222, 228),
    "Locations": (233, 253),
}
TIMESTAMP = re.compile(
    r"^(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),? "
    r"\d{1,2} [A-Za-z]+ \d{4} \d{2}:\d{2}$"
)


def repair_text(value: str) -> str:
    """Correct common broken glyphs in this PDF's font map."""
    for old, new in {
        "Sel�ne": "Selûne",
        "Zzara�kath": "Zzara'kath",
        "� ": "— ",
        " �": " —",
    }.items():
        value = value.replace(old, new)
    return value.replace("\ufffd", "’").replace("Timo", "Jam").replace("Alyona", "Alëna")


def render_body(value: str) -> str:
    blocks = re.split(r"\n\s*\n", value.strip())
    rendered: list[str] = []
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        if all(line.startswith(("• ", "- ")) for line in lines):
            rendered.append("<ul>" + "".join(f"<li>{html.escape(line[2:])}</li>" for line in lines) + "</ul>")
        else:
            rendered.append(f"<p>{html.escape(' '.join(lines))}</p>")
    return "\n".join(rendered) or "<p>No description recorded in the export.</p>"


def session_file(number: int) -> str:
    directory = ROOT / "Daring Dozen" / "Sessions"
    pattern = re.compile(rf"DaringDozen{number:03d}(?:_|\.)")
    matches = sorted(path.name for path in directory.glob("DaringDozen*.md") if pattern.match(path.name))
    if len(matches) != 1:
        raise ValueError(f"Expected one source file for session {number}; found {matches}")
    return matches[0]


def campaign_html(facts: list[tuple[str, tuple[int, ...]]]) -> str:
    items = []
    for statement, sessions in facts:
        links = ", ".join(f'<a href="#{number}">Session {number}</a>' for number in sessions)
        citation = f' <span class="campaign-sources">({links})</span>' if links else ""
        items.append(f"<li>{html.escape(statement)}{citation}</li>")
    return '<section class="campaign-update"><p><strong>Campaign:</strong></p><ul>' + "".join(items) + "</ul></section>"


def slug(value: str) -> str:
    plain = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", plain.lower()).strip("-")


def build_lore_data() -> list[dict[str, object]]:
    reader = PdfReader(SOURCE)
    results: list[dict[str, object]] = []
    for category, (first, last) in SECTIONS.items():
        current: dict[str, object] | None = None
        for number in range(first, last + 1):
            lines = [line.strip() for line in reader.pages[number - 1].extract_text().splitlines() if line.strip()]
            if not lines or lines[-1] != f"{category} Page {number}":
                raise ValueError(f"Unexpected OneNote footer on PDF page {number}")
            if len(lines) >= 3 and TIMESTAMP.fullmatch(lines[-2]):
                current = {
                    "category": category,
                    "title": repair_text(lines[-3]),
                    "pages": [number],
                    "parts": [repair_text("\n".join(lines[:-3]))],
                }
                results.append(current)
            elif current is not None and len(lines) > 1:
                current["pages"].append(number)
                current["parts"].append(repair_text("\n".join(lines[:-1])))

    entries: list[dict[str, object]] = []
    for item in results:
        pages = item["pages"]
        body = "\n\n".join(part for part in item["parts"] if part.strip())
        if body.strip() == "Pr":
            body = ""
        # OneNote's PDF occasionally repeats the final line at a page break.
        body = re.sub(r"(?m)^(.{20,})\n\1$", r"\1", body)
        preview = re.sub(r"\s+", " ", body).strip()[:130]
        entries.append({
            "category": item["category"],
            "title": item["title"],
            "page": pages[0],
            "id": str(pages[0]),
            "pages": pages,
            "html": f"<h1>{html.escape(item['title'])}</h1>\n{render_body(body)}",
            "text": f"{item['title']} {body}",
            "teaser": preview or "No description recorded in the export.",
            "source": f"../../Dungeons & Dragons.pdf#page={pages[0]}",
            "origin": "onenote",
        })
    existing = {(entry["category"], entry["title"]): entry for entry in entries}
    for (category, title), facts in CAMPAIGN.items():
        for _, session_numbers in facts:
            for number in session_numbers:
                if number < 1:
                    raise ValueError(f"Invalid session reference for {category}: {title}")
                session_file(number)
        if (category, title) in existing:
            entry = existing[(category, title)]
            if "No description recorded in the export." in entry["html"]:
                entry["html"] = f"<h1>{html.escape(title)}</h1>"
                entry["teaser"] = facts[0][0][:130]
            entry["html"] += "\n" + campaign_html(facts)
            entry["text"] += " " + " ".join(statement for statement, _ in facts)
        else:
            first_session = next(number for _, sessions in facts for number in sessions)
            entries.append({
                "category": category,
                "title": title,
                "id": f"campaign-{slug(title)}",
                "page": None,
                "pages": [],
                "html": f"<h1>{html.escape(title)}</h1>\n" + campaign_html(facts),
                "text": f"{title} " + " ".join(statement for statement, _ in facts),
                "teaser": facts[0][0][:130],
                "source": session_file(first_session),
                "origin": "campaign",
            })
    # Future-session portrayals remain distinct from session-derived campaign facts.
    for title, notes in GM_CHARACTER_NOTES.items():
        if ("Characters", title) in existing or any(
            entry["category"] == "Characters" and entry["title"] == title for entry in entries
        ):
            raise ValueError(f"GM profile would replace an existing character entry: {title}")
        fields = (
            ("Appearance", notes["appearance"]),
            ("Voice", notes["voice"]),
            ("Mannerisms", notes["mannerisms"]),
            ("Private GM goal", notes["gm_goal"]),
            ("Example line", notes["example"]),
        )
        body = "\n".join(
            f"<p><strong>{html.escape(label)}:</strong> {html.escape(value)}</p>"
            for label, value in fields
        )
        entries.append({
            "category": "Characters",
            "title": title,
            "id": f"gm-{slug(title)}",
            "page": None,
            "pages": [],
            "html": f"<h1>{html.escape(title)}</h1>\n<p><strong>PRIVATE GM PREPARATION — not yet played.</strong></p>\n" + body,
            "text": title + " " + " ".join(notes.values()),
            "teaser": notes["appearance"][:130],
            "source": "../../Codex/campaign_reference.py",
            "origin": "gm",
        })
    return entries


if __name__ == "__main__":
    from collections import Counter

    print(Counter(entry["category"] for entry in build_lore_data()))

# Dynamic session archive migration 001 applied.
