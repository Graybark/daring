"""Build a self-contained, offline HTML browser for Daring Dozen sessions."""

from __future__ import annotations

import base64
import html
import json
import re
from pathlib import Path

from build_lore_data import build_lore_data


ROOT = Path(__file__).resolve().parents[1]
SESSION_DIR = ROOT / "Daring Dozen" / "Sessions"
OUTPUT = SESSION_DIR / "index.html"


def inline_markdown(value: str) -> str:
    links: list[str] = []

    def save_link(match: re.Match[str]) -> str:
        label = html.escape(match.group(1))
        href = html.escape(match.group(2), quote=True)
        links.append(f'<a href="{href}">{label}</a>')
        return f"@@LINK{len(links) - 1}@@"

    value = re.sub(r"\[([^\]]+)\]\(<([^>]+)>\)", save_link, value)
    value = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", save_link, value)
    value = html.escape(value)
    value = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", value)
    value = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", value)
    value = re.sub(r"`([^`]+)`", r"<code>\1</code>", value)
    for index, link in enumerate(links):
        value = value.replace(f"@@LINK{index}@@", link)
    return value


def render_markdown(source: str, highlight_opening_quote: bool = False) -> str:
    out: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []
    opening_quote = highlight_opening_quote

    def flush() -> None:
        if paragraph:
            content = " ".join(inline_markdown(line.strip()) for line in paragraph)
            out.append(f"<p>{content}</p>")
            paragraph.clear()
        if list_items:
            out.append("<ul>" + "".join(f"<li>{inline_markdown(item)}</li>" for item in list_items) + "</ul>")
            list_items.clear()

    for raw in source.splitlines():
        line = raw.strip()
        if not line:
            flush()
        elif line.startswith("# "):
            flush()
            out.append(f"<h1>{inline_markdown(line[2:])}</h1>")
        elif line.startswith("## "):
            flush()
            opening_quote = line == "## Session notes"
            out.append(f"<h2>{inline_markdown(line[3:])}</h2>")
        elif line.startswith("### "):
            flush()
            opening_quote = False
            out.append(f"<h3>{inline_markdown(line[4:])}</h3>")
        elif line.startswith("> "):
            flush()
            quote_class = ' class="memorable"' if opening_quote else ""
            out.append(f"<blockquote{quote_class}>{inline_markdown(line[2:])}</blockquote>")
            opening_quote = False
        elif line.startswith(("- ", "• ")):
            if paragraph:
                flush()
            list_items.append(line[2:])
        else:
            if list_items:
                flush()
            paragraph.append(line)
    flush()
    rendered = "\n".join(out)
    player_sections = re.compile(
        r"(<h3>Attending Players</h3>\n(?:<ul>.*?</ul>|<p>.*?</p>))"
        r"(?:\n(<h3>Absent Players</h3>\n(?:<ul>.*?</ul>|<p>.*?</p>)))?",
        re.DOTALL,
    )

    def arrange_players(match: re.Match[str]) -> str:
        attending, absent = match.groups()
        if absent is None:
            absent = "<h3>Absent Players</h3><p>Not recorded.</p>"
        return f'<div class="player-headcount"><section>{attending}</section><section>{absent}</section></div>'

    return player_sections.sub(arrange_players, rendered)


def build_data() -> list[dict[str, str | int]]:
    sessions = []
    for path in SESSION_DIR.glob("DaringDozen*.md"):
        match = re.match(r"DaringDozen(\d{3,})(?:_|\.)", path.name)
        if not match:
            continue
        number = int(match.group(1))
        source = path.read_text(encoding="utf-8")
        title = next((line[2:].strip() for line in source.splitlines() if line.startswith("# ")), f"Session {number}")
        date_match = re.search(r"\*\*(Date played|Archive timestamp):\*\*\s*(.+?)(?:  |$)", source, re.MULTILINE)
        archive_match = re.search(r"^Archive timestamp:\s*([^\.\n]+)", source, re.MULTILINE)
        date_label = date_match.group(1) if date_match else ("Archive timestamp" if archive_match else "Date")
        date = date_match.group(2).strip() if date_match else (archive_match.group(1).strip() if archive_match else "Unknown")
        game_date_match = re.search(r"^\*\*In-game date:\*\*\s*(.+)$", source, re.MULTILINE)
        game_date = game_date_match.group(1).strip() if game_date_match else "Not recorded"
        year_match = re.search(r"\b(20\d{2})\b", date)
        year = year_match.group(1) if year_match else "Unknown"
        body = re.split(r"^## (?:Archived notes|Session notes|What happened|Summary)\s*$", source, maxsplit=1, flags=re.MULTILINE)
        game_content = body[-1].split("\n---\n", 1)[0].strip()
        display_source = f"# {title}\n\n{game_content}"
        plain = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", display_source)
        plain = re.sub(r"[#*>`]", "", plain)
        body_lines = game_content.splitlines()
        teaser = next((re.sub(r"[*`#]", "", line).strip() for line in body_lines if len(line.strip()) > 45 and not line.lstrip().startswith(("[", ">"))), "Session notes")
        teaser = teaser[:110].rstrip()
        sessions.append({
            "number": number,
            "title": title,
            "date": date,
            "dateLabel": date_label,
            "gameDate": game_date,
            "year": year,
            "file": path.name,
            "html": render_markdown(display_source, highlight_opening_quote="## Session notes" in source),
            "text": plain,
            "teaser": teaser,
        })
    sessions.sort(key=lambda item: item["number"], reverse=True)
    if not sessions:
        raise ValueError("No session source files found")
    numbers = [item["number"] for item in sessions]
    duplicates = sorted({n for n in numbers if numbers.count(n) > 1})
    missing = sorted(set(range(1, max(numbers) + 1)) - set(numbers))
    if duplicates or missing or min(numbers) < 1:
        raise ValueError(f"Invalid session sequence: duplicates={duplicates}, missing={missing}")
    return sessions


def main() -> None:
    sessions = build_data()
    lore = build_lore_data()
    data = json.dumps({"sessions": sessions, "lore": lore}, ensure_ascii=False, separators=(",", ":"))
    data = data.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    favicon = base64.b64encode((SESSION_DIR / "favicon.svg").read_bytes()).decode("ascii")
    template = r'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="robots" content="noindex,nofollow,noarchive">
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml;base64,__ICON__">
  <title>Daring Dozen — Session Archive</title>
  <style>
    :root { --ink:#252b2b; --muted:#61706e; --paper:#f8f6f0; --panel:#fffdfa; --line:#d8ddd7; --forest:#174b45; --teal:#dcebe6; --gold:#cfaa63; --shadow:0 8px 32px #233a3214; }
    * { box-sizing:border-box; }
    html { scroll-behavior:smooth; }
    body { margin:0; background:var(--paper); color:var(--ink); font:16px/1.55 Georgia, 'Times New Roman', serif; }
    button,input,select { font:inherit; }
    button { cursor:pointer; }
    a { color:#17665c; text-underline-offset:3px; }
    .app { display:grid; grid-template-columns:minmax(275px,345px) minmax(0,1fr); min-height:100vh; }
    .sidebar { position:sticky; top:0; height:100vh; overflow:hidden; display:flex; flex-direction:column; background:#eef2ec; border-right:1px solid var(--line); }
    .brand { padding:25px 22px 17px; background:var(--forest); color:#fff; }
    .eyebrow { margin:0 0 6px; text-transform:uppercase; letter-spacing:.16em; font:700 11px/1.4 system-ui,sans-serif; color:#c4dfd4; }
    .brand h1 { margin:0; font-size:29px; line-height:1.1; letter-spacing:-.03em; }
    .brand p:last-child { margin:9px 0 0; color:#d7e6df; font:13px/1.4 system-ui,sans-serif; }
    .category-nav { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:6px; padding:12px 10px; border-bottom:1px solid var(--line); }
    .category-button { min-height:34px; padding:6px 7px; text-align:center; border:1px solid transparent; border-radius:7px; background:transparent; color:#35534c; font:600 12px/1.25 system-ui,sans-serif; }
    .category-button:hover { background:#fffaf0; }
    .category-button.active { background:#fff; border-color:#b4cfc4; color:var(--forest); box-shadow:0 2px 8px #1e55400e; }
    .controls { padding:18px 17px 13px; border-bottom:1px solid var(--line); }
    .search-wrap { position:relative; }
    .search-wrap svg { position:absolute; left:13px; top:13px; width:18px; height:18px; color:var(--muted); }
    #search { width:100%; padding:11px 12px 11px 40px; border:1px solid #b9c8bf; border-radius:10px; background:#fff; color:var(--ink); outline:none; font:14px system-ui,sans-serif; }
    #search:focus, #year:focus, button:focus-visible, a:focus-visible { outline:3px solid #c6a663; outline-offset:2px; }
    .filter-row { display:flex; align-items:center; justify-content:space-between; gap:12px; margin-top:12px; font:13px system-ui,sans-serif; color:var(--muted); }
    #year { width:120px; padding:7px 9px; border:1px solid #b9c8bf; border-radius:8px; background:#fff; color:var(--ink); font:13px system-ui,sans-serif; }
    #result-count { font-variant-numeric:tabular-nums; }
    .session-list { overflow-y:auto; padding:9px 9px 20px; }
    .session-link { display:block; width:100%; text-align:left; border:1px solid transparent; background:transparent; border-radius:10px; padding:11px 13px; color:var(--ink); margin:2px 0; }
    .session-link:hover { background:#fffaf0; border-color:#e3dccb; }
    .session-link.active { background:#fff; border-color:#b4cfc4; box-shadow:0 2px 10px #1e55400e; }
    .session-number { display:block; color:var(--forest); font:700 14px/1.3 system-ui,sans-serif; }
    .session-title { display:-webkit-box; margin-top:3px; font:13px/1.35 system-ui,sans-serif; overflow:hidden; -webkit-line-clamp:2; -webkit-box-orient:vertical; }
    .session-date { display:block; margin-top:4px; color:var(--muted); font:12px/1.3 system-ui,sans-serif; }
    .empty { margin:20px 10px; color:var(--muted); font:14px/1.5 system-ui,sans-serif; }
    .main { min-width:0; padding:32px clamp(20px,5vw,76px) 80px; }
    .topbar { max-width:900px; margin:0 auto 26px; display:flex; justify-content:space-between; align-items:center; gap:14px; }
    .breadcrumb { color:var(--muted); font:13px system-ui,sans-serif; }
    .top-actions { display:flex; gap:8px; }
    .nav-button,.mobile-button { border:1px solid #b6c9c0; background:#fff; color:var(--forest); border-radius:9px; padding:8px 12px; font:700 13px system-ui,sans-serif; }
    .nav-button:hover,.mobile-button:hover { background:var(--teal); }
    .nav-button:disabled { opacity:.35; cursor:default; }
    .mobile-button { display:none; }
    .sheet { max-width:900px; min-height:65vh; margin:auto; padding:clamp(26px,5vw,62px); background:var(--panel); border:1px solid #e3e1d9; border-radius:4px; box-shadow:var(--shadow); }
    .sheet-top { padding-bottom:19px; border-bottom:2px solid var(--gold); }
    .chapter { color:var(--forest); text-transform:uppercase; letter-spacing:.16em; font:700 11px system-ui,sans-serif; }
    .game-date { margin-top:5px; color:#1c3431; font:700 clamp(22px,3vw,28px)/1.2 Georgia,serif; }
    .source-link { font:12px system-ui,sans-serif; }
    .entry { overflow-wrap:anywhere; }
    .entry h1 { margin:28px 0 15px; color:#1c3431; font-size:clamp(31px,4vw,44px); line-height:1.15; letter-spacing:-.035em; }
    .entry h2 { margin:32px 0 10px; padding-top:10px; border-top:1px solid var(--line); color:#23483f; font-size:22px; line-height:1.25; }
    .entry h3 { margin:32px 0 8px; color:#23483f; font:700 19px/1.3 Georgia,serif; }
    .entry h3 + p, .entry h3 + ul { margin-top:5px; }
    .entry p { margin:13px 0; }
    .entry p:nth-of-type(-n+2) { color:#46534e; }
    .entry ul { padding-left:1.45em; margin:12px 0; }
    .entry li { margin:6px 0; }
    .player-headcount { display:grid; grid-template-columns:minmax(0,1fr) minmax(0,.65fr); gap:24px; margin:24px 0 28px; padding:16px 20px; background:#f4f7f2; border:1px solid var(--line); border-radius:8px; }
    .entry .player-headcount h3 { margin:0 0 8px; font-size:17px; }
    .entry .player-headcount ul,.entry .player-headcount p { margin:0; }
    .entry .player-headcount li { margin:3px 0; }
    .entry blockquote { margin:20px 0; padding:12px 16px; border-left:3px solid var(--gold); background:#f7f3e9; color:#665a45; font-size:15px; }
    .entry blockquote.memorable { margin:26px 0 30px; padding:18px 22px; border-left-width:4px; color:#31443e; font:italic 18px/1.5 Georgia,serif; }
    .entry.lore h1 { margin-bottom:28px; }
    .entry.lore p { margin:14px 0; }
    .entry.lore p:nth-of-type(-n+2) { color:var(--ink); }
    .campaign-update { margin-top:32px; padding:16px 20px 12px; border-left:4px solid var(--gold); background:#f4f7f2; }
    .campaign-update p { margin:0 0 8px !important; color:var(--forest) !important; }
    .campaign-update ul { margin:8px 0 0; }
    .campaign-update li { margin:9px 0; }
    .campaign-sources { color:var(--muted); font:12px/1.5 system-ui,sans-serif; white-space:nowrap; }
    .entry code { font:13px ui-monospace,monospace; background:#ecf0ec; padding:2px 4px; border-radius:3px; }
    .file-link-row { margin:30px 0 0; padding-top:12px; border-top:1px solid var(--line); text-align:right; }
    .bottom-nav { max-width:900px; margin:22px auto 0; display:flex; justify-content:space-between; gap:12px; }
    .footer { max-width:900px; margin:24px auto 0; color:var(--muted); font:12px/1.45 system-ui,sans-serif; }
    @media (max-width:800px) {
      .app { display:block; }
      .sidebar { position:fixed; z-index:5; left:0; top:0; bottom:0; width:min(88vw,360px); height:100dvh; transform:translateX(-105%); transition:transform .2s ease; box-shadow:var(--shadow); }
      .sidebar.open { transform:translateX(0); }
      .main { padding:18px 15px 50px; }
      .mobile-button { display:inline-block; }
      .topbar { margin-bottom:15px; }
      .breadcrumb { display:none; }
      .sheet { padding:25px 19px; }
      .scrim { display:none; position:fixed; inset:0; background:#102a2580; z-index:4; }
      .scrim.show { display:block; }
    }
    @media (max-width:560px) { .player-headcount { grid-template-columns:1fr; gap:14px; } }
    @media print { .sidebar,.topbar,.bottom-nav,.footer,.source-link,.scrim { display:none !important; } .app { display:block; } .main { padding:0; } .sheet { border:0; box-shadow:none; max-width:none; padding:0; } body { background:#fff; } }
  </style>
</head>
<body>
  <div class="scrim" id="scrim"></div>
  <div class="app">
    <aside class="sidebar" id="sidebar" aria-label="Session navigation">
      <div class="brand"><p class="eyebrow">Private GM archive</p><h1>Daring Dozen</h1><p>__SESSION_COUNT__ sessions · __LORE_COUNT__ reference entries</p></div>
      <nav class="category-nav" id="category-nav" aria-label="Browse archive"></nav>
      <div class="controls">
        <div class="search-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="10.8" cy="10.8" r="6.8"/><path d="m16 16 5 5"/></svg><input id="search" type="search" placeholder="Search names, places, events…" aria-label="Search sessions"></div>
        <div class="filter-row"><span id="result-count">__SESSION_COUNT__ sessions</span><select id="year" aria-label="Filter by year"><option value="all">All years</option></select></div>
      </div>
      <div class="session-list" id="session-list"></div>
    </aside>
    <main class="main">
      <div class="topbar"><button class="mobile-button" id="menu-button" aria-expanded="false">☰ Browse</button><span class="breadcrumb" id="breadcrumb">Daring Dozen / Sessions</span><div class="top-actions"><button class="nav-button" id="older-top">← Older</button><button class="nav-button" id="newer-top">Newer →</button></div></div>
      <article class="sheet"><div class="sheet-top"><span class="chapter" id="sheet-label">In-game date</span><div class="game-date" id="game-date">Not recorded</div></div><div class="entry" id="entry"></div><div class="file-link-row"><a class="source-link" id="source-link" href="#">Open session file ↗</a></div></article>
      <div class="bottom-nav"><button class="nav-button" id="older-bottom">← Older session</button><button class="nav-button" id="newer-bottom">Newer session →</button></div>
      <p class="footer">Dates marked “estimated” follow the session chronology, rests, travel, or waits described in the notes. Single times remain for brief scenes or notes without enough detail to establish elapsed time. Private GM archive: some older pages contain preparation alongside played events. Do not share the complete browser as a player recap.</p>
    </main>
  </div>
  <script id="session-data" type="application/json">__DATA__</script>
  <script>
    const archive = JSON.parse(document.getElementById('session-data').textContent);
    const sessions = archive.sessions;
    const sections = ['Sessions', 'Characters', 'Encounters', 'Mythology', 'Factions', 'Culture and History', 'Locations'];
    const records = { Sessions: sessions };
    for (const name of sections.slice(1)) records[name] = archive.lore.filter(item => item.category === name).sort((a,b) => a.title.localeCompare(b.title));
    const slugs = new Map(sections.map(name => [name.toLowerCase().replace(/[^a-z0-9]+/g, '-'), name]));
    const byNumber = new Map(sessions.map(s => [s.number, s]));
    const list = document.getElementById('session-list');
    const categoryNav = document.getElementById('category-nav');
    const search = document.getElementById('search');
    const year = document.getElementById('year');
    const sidebar = document.getElementById('sidebar');
    const scrim = document.getElementById('scrim');
    let current = null;
    let section = 'Sessions';
    for (const name of sections) {
      const button = document.createElement('button'); button.type = 'button'; button.className = 'category-button';
      button.textContent = name; button.dataset.section = name;
      button.addEventListener('click', () => { search.value = ''; year.value = 'all'; showRecord(name === 'Sessions' ? sessions[0] : records[name][0]); });
      categoryNav.append(button);
    }
    for (const value of [...new Set(sessions.map(s => s.year))].sort((a,b) => b.localeCompare(a))) {
      const option = document.createElement('option'); option.value = value; option.textContent = value; year.append(option);
    }
    const normalized = value => String(value).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
    function closeMenu() { sidebar.classList.remove('open'); scrim.classList.remove('show'); document.getElementById('menu-button').setAttribute('aria-expanded','false'); }
    function filtered() {
      const query = normalized(search.value.trim());
      return records[section].filter(item => (section !== 'Sessions' || year.value === 'all' || item.year === year.value) && (!query || normalized(`${item.title} ${item.date || ''} ${item.text}`).includes(query)));
    }
    function renderList() {
      const visible = filtered(); list.replaceChildren();
      document.getElementById('result-count').textContent = `${visible.length} ${section === 'Sessions' ? (visible.length === 1 ? 'session' : 'sessions') : (visible.length === 1 ? 'entry' : 'entries')}`;
      if (!visible.length) { const p = document.createElement('p'); p.className = 'empty'; p.textContent = 'No entries match your search.'; list.append(p); return; }
      for (const item of visible) {
        const button = document.createElement('button'); button.className = 'session-link' + (item === current ? ' active' : '');
        button.type = 'button'; button.setAttribute('aria-current', item === current ? 'page' : 'false');
        const heading = document.createElement('span'); heading.className = 'session-number'; heading.textContent = section === 'Sessions' ? `Session ${item.number}` : item.title;
        const title = document.createElement('span'); title.className = 'session-title'; title.textContent = section === 'Sessions' ? (item.title.replace(/^Daring Dozen\s*[—-]\s*Session\s*\d+\s*[—-]?\s*/, '') || item.teaser) : item.teaser;
        const date = document.createElement('span'); date.className = 'session-date'; date.textContent = section === 'Sessions' ? item.date : (item.origin === 'onenote' ? `OneNote p. ${item.page}` : 'From sessions');
        button.append(heading, title, date); button.addEventListener('click', () => showRecord(item)); list.append(button);
      }
    }
    function showRecord(item, updateHash = true) {
      if (!item) return;
      current = item; section = item.category || 'Sessions';
      const isSession = section === 'Sessions';
      const entry = document.getElementById('entry'); entry.innerHTML = item.html; entry.classList.toggle('lore', !isSession);
      document.getElementById('sheet-label').textContent = isSession ? 'In-game date' : 'Campaign reference';
      document.getElementById('game-date').textContent = isSession ? item.gameDate : section;
      document.getElementById('breadcrumb').textContent = `Daring Dozen / ${section}`;
      year.style.display = isSession ? '' : 'none';
      search.placeholder = isSession ? 'Search names, places, events…' : `Search ${section.toLowerCase()}…`;
      for (const button of categoryNav.children) { const active = button.dataset.section === section; button.classList.toggle('active', active); button.setAttribute('aria-current', active ? 'page' : 'false'); }
      const source = document.getElementById('source-link'); source.href = isSession ? item.file : item.source; source.textContent = isSession ? 'Open session file ↗' : (item.origin === 'onenote' ? 'Open OneNote page ↗' : 'Open related session ↗');
      document.querySelector('.footer').style.display = isSession ? '' : 'none';
      document.title = `${isSession ? `Session ${item.number}` : item.title} — Daring Dozen`;
      const position = isSession ? -1 : records[section].indexOf(item);
      const previous = isSession ? byNumber.get(item.number - 1) : records[section][position - 1];
      const next = isSession ? byNumber.get(item.number + 1) : records[section][position + 1];
      for (const id of ['older-top','older-bottom']) { const button = document.getElementById(id); button.disabled = !previous; button.textContent = isSession ? (id.endsWith('top') ? '← Older' : '← Older session') : '← Previous'; }
      for (const id of ['newer-top','newer-bottom']) { const button = document.getElementById(id); button.disabled = !next; button.textContent = isSession ? (id.endsWith('top') ? 'Newer →' : 'Newer session →') : 'Next →'; }
      if (updateHash) history.replaceState(null, '', isSession ? `#${item.number}` : `#${section.toLowerCase().replace(/[^a-z0-9]+/g, '-')}/${item.id}`);
      renderList(); closeMenu(); window.scrollTo({top:0,behavior:'instant'});
      const active = list.querySelector('.active'); if (active) active.scrollIntoView({block:'nearest'});
    }
    function move(delta) { if (!current) return; const item = section === 'Sessions' ? byNumber.get(current.number + delta) : records[section][records[section].indexOf(current) + delta]; if (item) showRecord(item); }
    for (const id of ['older-top','older-bottom']) document.getElementById(id).addEventListener('click', () => move(-1));
    for (const id of ['newer-top','newer-bottom']) document.getElementById(id).addEventListener('click', () => move(1));
    search.addEventListener('input', renderList); year.addEventListener('change', renderList);
    document.getElementById('menu-button').addEventListener('click', () => { const open = sidebar.classList.toggle('open'); scrim.classList.toggle('show', open); document.getElementById('menu-button').setAttribute('aria-expanded', String(open)); if (open) search.focus(); });
    scrim.addEventListener('click', closeMenu);
    function openHash() {
      const hash = location.hash.slice(1);
      const match = hash.match(/^([^/]+)\/([^/]+)$/);
      if (match) { const name = slugs.get(match[1]); const item = name && records[name].find(record => String(record.id) === match[2]); if (item) { showRecord(item, false); return; } }
      const number = Number(hash); showRecord(byNumber.get(number) || sessions[0], false);
    }
    window.addEventListener('hashchange', openHash);
    document.addEventListener('keydown', event => { if (event.key === 'Escape') closeMenu(); if (event.key === '/' && !['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)) { event.preventDefault(); if (innerWidth < 801) { sidebar.classList.add('open'); scrim.classList.add('show'); document.getElementById('menu-button').setAttribute('aria-expanded','true'); } search.focus(); } });
    openHash();
  </script>
</body>
</html>'''
    OUTPUT.write_text(template.replace("__DATA__", data).replace("__ICON__", favicon).replace("__LORE_COUNT__", str(len(lore))).replace("__SESSION_COUNT__", str(len(sessions))), encoding="utf-8")
    print(f"Built {OUTPUT} with {len(sessions)} sessions and {len(lore)} reference entries ({OUTPUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()

# Dynamic session archive migration 001 applied.
