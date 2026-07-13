"""Build the static study site (docs/index.html) from the interview-prep markdown.

Usage:  pip install markdown && python build_site.py
Output: <repo-root>/docs/index.html  — serve via GitHub Pages (main branch, /docs folder).

Every `**question**` line becomes a collapsible card; everything else renders as prose.
Re-run after editing any markdown file, commit docs/ along with the content change.
"""

import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]          # interview-prep/
DOCS = ROOT.parent / "docs"                          # repo-root/docs/

PAGES = [
    ("start", "Start Here", ROOT / "README.md"),
    ("defense", "Project Defense", ROOT / "project-defense.md"),
    ("jobs", "Live Job Matches", ROOT / "jobs-snapshot.md"),
    ("in-loop", "India · The Loop", ROOT / "india/README.md"),
    ("in-core", "India · GenAI/LLM Core", ROOT / "india/01-genai-llm-core-questions.md"),
    ("in-py", "India · Python Round", ROOT / "india/02-python-and-coding-round.md"),
    ("in-dsa", "India · DSA/SDE Round", ROOT / "india/03-dsa-sde-round.md"),
    ("in-companies", "India · Company Experiences", ROOT / "india/04-company-experiences.md"),
    ("in-hr", "India · HR & Behavioral", ROOT / "india/05-hr-behavioral.md"),
    ("us-loop", "US/Global · The Loop", ROOT / "us-global/README.md"),
    ("us-core", "US/Global · GenAI/LLM Depth", ROOT / "us-global/01-genai-llm-questions.md"),
    ("us-design", "US/Global · System Design", ROOT / "us-global/02-llm-system-design.md"),
    ("us-code", "US/Global · Coding Rounds", ROOT / "us-global/03-coding-rounds.md"),
    ("us-companies", "US/Global · Company Loops", ROOT / "us-global/04-company-loops.md"),
    ("us-behavioral", "US/Global · Behavioral", ROOT / "us-global/05-behavioral.md"),
    ("sources", "Sources", ROOT / "SOURCES.md"),
]

GROUPS = [
    ("Getting ready", ["start", "defense", "jobs"]),
    ("India", ["in-loop", "in-core", "in-py", "in-dsa", "in-companies", "in-hr"]),
    ("US / Global", ["us-loop", "us-core", "us-design", "us-code", "us-companies", "us-behavioral"]),
    ("Reference", ["sources"]),
]

Q_RE = re.compile(r"^\*\*(?P<q>.+?)\*\*(?P<tag>\s*\*\(.+?\)\*)?\s*$")

md = markdown.Markdown(extensions=["tables", "fenced_code"])


def render(text: str) -> str:
    md.reset()
    return md.convert(text)


def render_inline(text: str) -> str:
    html = render(text)
    return re.sub(r"^<p>|</p>$", "", html.strip())


def build_page(slug: str, title: str, path: Path) -> str:
    lines = path.read_text().splitlines()
    out, buf, answer, question, tag, fence = [], [], [], None, "", False

    def flush_prose():
        if buf:
            out.append(render("\n".join(buf)))
            buf.clear()

    def flush_qa():
        nonlocal question, tag
        if question is not None:
            tag_html = f'<span class="qtag">{render_inline(tag.strip())}</span>' if tag.strip() else ""
            answer_html = render("\n".join(answer))
            out.append(
                f'<details class="qa"><summary>{render_inline(question)}{tag_html}</summary>'
                f'<div class="answer">{answer_html}</div></details>'
            )
            question, tag = None, ""
            answer.clear()

    for line in lines:
        if line.lstrip().startswith("```"):
            fence = not fence
            (answer if question is not None else buf).append(line)
            continue
        m = None if fence else Q_RE.match(line.strip())
        if m:
            flush_qa()
            flush_prose()
            question, tag = m.group("q"), (m.group("tag") or "").strip().strip("*")
        elif not fence and question is not None and (line.startswith("#") or line.strip() == "---"):
            flush_qa()
            buf.append(line)
        elif question is not None:
            answer.append(line)
        else:
            buf.append(line)
    flush_qa()
    flush_prose()

    body = "\n".join(out)
    # drop the file's own H1; the section header replaces it
    body = re.sub(r"<h1>.*?</h1>", "", body, count=1)
    return f'<section id="{slug}" data-title="{title}"><h1 class="page-title">{title}</h1>{body}</section>'


def nav_html() -> str:
    slug_title = {s: t for s, t, _ in PAGES}
    parts = []
    for group, slugs in GROUPS:
        items = "".join(f'<a href="#{s}" data-nav="{s}">{slug_title[s]}</a>' for s in slugs)
        parts.append(f'<div class="nav-group"><h3>{group}</h3>{items}</div>')
    return "\n".join(parts)


CSS = """
:root{
  --bg:#fdfdfc; --panel:#f4f4f2; --text:#1c1c1a; --muted:#6f6f68; --line:#e4e4df;
  --accent:#0b7261; --accent-soft:#e3f1ee; --code-bg:#f0f0ed; --mark:#fff3bf;
}
[data-theme="dark"]{
  --bg:#111113; --panel:#1a1a1e; --text:#ececea; --muted:#9a9a92; --line:#2a2a2f;
  --accent:#4cc4ae; --accent-soft:#15332e; --code-bg:#1f1f24; --mark:#4d431a;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:1rem}
body{margin:0;background:var(--bg);color:var(--text);
  font-family:'Geist',ui-sans-serif,system-ui,-apple-system,'Segoe UI',sans-serif;
  font-size:16.5px;line-height:1.75;-webkit-font-smoothing:antialiased}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
.layout{display:flex;min-height:100vh}
nav{width:280px;flex-shrink:0;border-right:1px solid var(--line);background:var(--panel);
  padding:1.2rem 1rem 3rem;position:sticky;top:0;height:100vh;overflow-y:auto}
nav .brand{font-weight:700;font-size:1.05rem;margin:.2rem 0 1rem;display:block;color:var(--text)}
.nav-group h3{font-size:.72rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin:1.2rem 0 .3rem}
.nav-group a{display:block;padding:.3rem .6rem;border-radius:8px;color:var(--text);font-size:.92rem}
.nav-group a:hover{background:var(--accent-soft);text-decoration:none}
main{flex:1;min-width:0;padding:2rem clamp(1.2rem,4vw,3.5rem) 6rem;max-width:54rem}
.toolbar{display:flex;gap:.6rem;align-items:center;position:sticky;top:0;z-index:5;
  background:var(--bg);padding:.8rem 0;border-bottom:1px solid var(--line);margin-bottom:1.5rem}
#search{flex:1;padding:.6rem .9rem;border:1px solid var(--line);border-radius:10px;
  background:var(--panel);color:var(--text);font:inherit;font-size:.95rem}
#search:focus{outline:2px solid var(--accent);border-color:transparent}
.toolbar button{padding:.55rem .8rem;border:1px solid var(--line);border-radius:10px;
  background:var(--panel);color:var(--text);font:inherit;font-size:.85rem;cursor:pointer}
.toolbar button:hover{background:var(--accent-soft)}
#count{font-size:.85rem;color:var(--muted);white-space:nowrap}
section{margin-bottom:4rem}
.page-title{font-size:1.7rem;line-height:1.25;margin:2.5rem 0 1rem;letter-spacing:-.02em}
h2{font-size:1.25rem;margin:2.2rem 0 .8rem;letter-spacing:-.01em}
h3{font-size:1.05rem}
p{margin:.8rem 0}
blockquote{margin:1rem 0;padding:.6rem 1rem;border-left:3px solid var(--accent);
  background:var(--panel);border-radius:0 10px 10px 0;color:var(--muted)}
code{font-family:'Geist Mono',ui-monospace,monospace;font-size:.86em;
  background:var(--code-bg);padding:.12em .35em;border-radius:5px}
pre{background:var(--code-bg);padding:1rem;border-radius:12px;overflow-x:auto;line-height:1.55}
pre code{background:none;padding:0}
table{border-collapse:collapse;display:block;overflow-x:auto;margin:1rem 0;font-size:.92rem}
th,td{border:1px solid var(--line);padding:.5rem .7rem;text-align:left;vertical-align:top}
th{background:var(--panel)}
details.qa{border:1px solid var(--line);border-radius:12px;margin:.6rem 0;background:var(--panel)}
details.qa summary{cursor:pointer;padding:.75rem 1rem;font-weight:600;list-style:none;
  display:flex;gap:.5rem;align-items:baseline;flex-wrap:wrap}
details.qa summary::before{content:'+';color:var(--accent);font-weight:700;margin-right:.2rem}
details.qa[open] summary::before{content:'–'}
details.qa summary:hover{color:var(--accent)}
.qtag{font-weight:400;font-size:.8rem;color:var(--muted);font-style:italic}
.answer{padding:0 1.1rem .9rem;border-top:1px dashed var(--line)}
mark{background:var(--mark);color:inherit;border-radius:3px;padding:0 .1em}
.hidden{display:none!important}
#menu-btn{display:none}
@media (max-width:820px){
  nav{position:fixed;left:0;top:0;transform:translateX(-100%);transition:transform .2s;z-index:20;box-shadow:4px 0 20px rgba(0,0,0,.15)}
  nav.open{transform:none}
  #menu-btn{display:inline-block}
  main{padding-top:.5rem}
}
"""

JS = """
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const root=document.documentElement;
const saved=localStorage.getItem('theme');
if(saved)root.dataset.theme=saved;
else root.dataset.theme=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';
$('#theme-btn').onclick=()=>{root.dataset.theme=root.dataset.theme==='dark'?'light':'dark';
  localStorage.setItem('theme',root.dataset.theme)};
$('#menu-btn').onclick=()=>$('nav').classList.toggle('open');
$$('.nav-group a').forEach(a=>a.onclick=()=>$('nav').classList.remove('open'));
let allOpen=false;
$('#toggle-btn').onclick=()=>{allOpen=!allOpen;
  $$('details.qa:not(.hidden)').forEach(d=>d.open=allOpen);
  $('#toggle-btn').textContent=allOpen?'Collapse all':'Expand all';};
const cards=$$('details.qa'),sections=$$('main section');
const norm=t=>t.toLowerCase();
$('#search').oninput=e=>{
  const q=norm(e.target.value.trim());
  if(!q){cards.forEach(d=>{d.classList.remove('hidden');d.open=false});
    sections.forEach(s=>s.classList.remove('hidden'));
    $('#count').textContent='';return;}
  let hits=0;
  cards.forEach(d=>{const hit=norm(d.textContent).includes(q);
    d.classList.toggle('hidden',!hit);d.open=hit;if(hit)hits++;});
  sections.forEach(s=>{
    const any=[...s.querySelectorAll('details.qa')].some(d=>!d.classList.contains('hidden'));
    s.classList.toggle('hidden',!any);});
  $('#count').textContent=hits+' match'+(hits===1?'':'es');
};
"""

HTML = """<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Interview Prep — 1 YOE</title>
<meta name="description" content="Real interview questions and answers for AI/GenAI/LLM engineer roles at ~1 YOE — India and US/Global.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>__CSS__</style>
</head>
<body>
<div class="layout">
<nav>
<a class="brand" href="#start">🎯 AI Interview Prep <span style="color:var(--muted);font-weight:400">· 1 YOE</span></a>
__NAV__
</nav>
<main>
<div class="toolbar">
<button id="menu-btn" title="Menu">☰</button>
<input id="search" type="search" placeholder="Search all questions… (e.g. chunking, LoRA, Pinecone)">
<span id="count"></span>
<button id="toggle-btn">Expand all</button>
<button id="theme-btn" title="Toggle theme">◐</button>
</div>
__CONTENT__
<footer style="color:var(--muted);font-size:.85rem;border-top:1px solid var(--line);padding-top:1rem">
Built from the <a href="https://github.com/prayagtushar/prayagtushar/tree/main/interview-prep">interview-prep</a> question bank.
Regenerate with <code>python interview-prep/site/build_site.py</code>.
</footer>
</main>
</div>
<script>__JS__</script>
</body>
</html>
"""


def main() -> None:
    content = "\n".join(build_page(s, t, p) for s, t, p in PAGES)
    html = (
        HTML.replace("__CSS__", CSS)
        .replace("__NAV__", nav_html())
        .replace("__CONTENT__", content)
        .replace("__JS__", JS)
    )
    DOCS.mkdir(exist_ok=True)
    (DOCS / "index.html").write_text(html)
    (DOCS / ".nojekyll").write_text("")
    qa = html.count('class="qa"')
    print(f"wrote {DOCS / 'index.html'} ({len(html) // 1024} KB, {qa} question cards)")


if __name__ == "__main__":
    main()
