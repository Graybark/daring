"""Stage only the campaign browser for PUBLIC Pages; keep source files private.

This is not authentication or a player-safe content filter. All content embedded
in the browser is published. Separate PDFs, Markdown and GM files are not copied.
"""
from __future__ import annotations

import copy
import html
import json
import posixpath
import re
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
BROWSER_DIR = 'Daring Dozen/Sessions'
SOURCE = ROOT / BROWSER_DIR / 'index.html'
OUTPUT = ROOT / '_site'
REPOSITORY = 'https://github.com/Graybark/daring/blob/main/'
DATA = re.compile(r'(<script id="session-data" type="application/json">)(.*?)(</script>)', re.S)
ALLOWED = {'index.html', 'favicon.svg', '.nojekyll'}


def source_url(value: str) -> str:
    """Resolve a source link in the original browser to authenticated GitHub."""
    value = html.unescape(value)
    if not value or value.startswith('#'):
        return value
    parts = urlsplit(value)
    if parts.scheme in ('http', 'https'):
        return value
    if parts.scheme or parts.netloc or parts.path.startswith('/'):
        raise ValueError('Unexpected source link; review it before publication')
    path = posixpath.normpath(posixpath.join(BROWSER_DIR, unquote(parts.path)))
    if path.startswith('../') or not (ROOT / path).is_file():
        raise ValueError(f'Missing or unsafe source path: {path}')
    return urlunsplit(('https', 'github.com', '/Graybark/daring/blob/main/' + quote(path, safe='/'), '', parts.fragment))


def link_sources(body: str) -> str:
    def replace(match: re.Match[str]) -> str:
        return 'href=' + match[1] + html.escape(source_url(match[2]), quote=True) + match[1]
    return re.sub(r'href=([\'\"])(.*?)\1', replace, body)


def make_public_browser(source: str) -> str:
    matches = list(DATA.finditer(source))
    if len(matches) != 1:
        raise ValueError('Expected exactly one embedded archive')
    original = json.loads(matches[0][2])
    archive = copy.deepcopy(original)
    if not archive['sessions'] or len({s['number'] for s in archive['sessions']}) != len(archive['sessions']):
        raise ValueError('Missing or duplicate sessions')
    for entry in archive['sessions']:
        entry['file'] = source_url(entry['file'])
        entry['html'] = link_sources(entry['html'])
    for entry in archive['lore']:
        entry['source'] = source_url(entry['source'])
        entry['html'] = link_sources(entry['html'])
    data = json.dumps(archive, ensure_ascii=False, separators=(',', ':'))
    data = data.replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    output = DATA.sub(lambda m: m[1] + data + m[3], source)
    # Change only misleading privacy labels; preserve the offline source/design.
    output = output.replace('Private GM archive</p>', 'Campaign archive</p>')
    output = output.replace('Private GM archive: some older pages contain preparation alongside played events. Do not share the complete browser as a player recap.',
                            'GM archive: some older pages contain preparation alongside played events. This website is publicly accessible.')
    output = output.replace('Open session file ↗', 'Open source on GitHub ↗')
    output = output.replace('Open OneNote page ↗', 'Open source PDF on GitHub ↗')
    output = output.replace('Open related session ↗', 'Open source on GitHub ↗')
    if '<meta name="robots" content="noindex,nofollow,noarchive">' not in output:
        output = output.replace('<head>', '<head>\n  <meta name="robots" content="noindex,nofollow,noarchive">', 1)
    output = output.replace('<head>', '<head>\n  <meta name="referrer" content="no-referrer">', 1)
    if re.search(r'gh[pousr]_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{20,}|[?&](?:token|sig|access_token)=', output):
        raise ValueError('Possible credential in public output; review before publication')
    return output


def main() -> None:
    source = SOURCE.read_text(encoding='utf-8')
    public = make_public_browser(source)
    OUTPUT.mkdir(exist_ok=True)
    if OUTPUT.is_symlink() or any(p.is_symlink() or not p.is_file() or p.name not in ALLOWED for p in OUTPUT.iterdir()):
        raise ValueError('_site contains unexpected files; refusing to publish it')
    (OUTPUT / 'index.html').write_text(public, encoding='utf-8')
    (OUTPUT / 'favicon.svg').write_bytes((ROOT / BROWSER_DIR / 'favicon.svg').read_bytes())
    (OUTPUT / '.nojekyll').write_text('', encoding='utf-8')
    if {p.name for p in OUTPUT.iterdir()} != ALLOWED:
        raise ValueError('Unexpected public artifact contents')
    archive = json.loads(DATA.search(public)[2])
    print(f"Staged PUBLIC browser: {len(archive['sessions'])} sessions, {len(archive['lore'])} reference entries.")
    print('Public artifact: .nojekyll, favicon.svg, index.html only. Separate source files remain in the private repository.')


if __name__ == '__main__':
    main()
