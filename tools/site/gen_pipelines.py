import sys, html
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from course import *
S=str(__import__("pathlib").Path(__file__).resolve().parents[2])   # repo root
R=S; OUT=__import__("os").environ.get("OUT", f"{R}/docs")
base_css=open(f"{S}/tools/site/css/index.html.styles.html",encoding="utf-8").read().split("</style>")[0]+"</style>"
base_css=base_css.replace("--accent: #0ea5e9","--accent: #16a34a")
extra='''<style>
  .tabs { display:flex; flex-wrap:wrap; gap:6px; margin-top:14px; }
  .tab { border:1px solid var(--line); background:var(--card); color:var(--ink); border-radius:10px 10px 0 0; padding:9px 16px; font-weight:700; cursor:pointer; font-size:.92rem; }
  .tab[aria-selected="true"] { background:var(--accent); color:#fff; border-color:var(--accent); }
  .panel { display:none; } .panel.on { display:block; }
  .panel pre { margin-top:0; border-top-left-radius:0; max-height:70vh; }
  .panel .path { font-size:.82rem; color:var(--muted); margin:8px 0 4px; }
  table { border-collapse:collapse; width:100%; margin-top:14px; font-size:.9rem; background:var(--card); border:1px solid var(--line); border-radius:12px; overflow:hidden; }
  th, td { text-align:left; padding:9px 10px; border-bottom:1px solid var(--line); vertical-align:top; }
  th { background:var(--bg); font-size:.85rem; }
  td:first-child { font-weight:600; white-space:nowrap; }
  td code { font-size:.8rem; background:var(--bg); border:1px solid var(--line); border-radius:6px; padding:1px 5px; }
  .tablewrap { overflow-x:auto; }
  .callout { background: var(--card); border: 1px solid var(--line); border-left: 6px solid var(--ok); border-radius: 14px; padding: 18px 20px; margin-top: 16px; }
  footer { margin-top: 56px; border-top: 1px solid var(--line); padding-top: 18px; color: var(--muted); font-size: .88rem; }
</style>'''
FILES=[("actions","⚙️ GitHub Actions",[".github/workflows/ci.yml",".github/workflows/ship.yml",".github/workflows/deploy.yml"]),
       ("circleci","🔄 CircleCI",[".circleci/config.yml"]),
       ("gitlab","🦊 GitLab CI",[".gitlab-ci.yml"]),
       ("jenkins","🎩 Jenkins",["Jenkinsfile"])]
ROWS=[
 ("Config file","<code>.github/workflows/*.yml</code>","<code>.circleci/config.yml</code>","<code>.gitlab-ci.yml</code>","<code>Jenkinsfile</code>"),
 ("Trigger 🔔","<code>on: push / pull_request</code>","every push by default; narrow with <code>filters:</code>","every push by default; narrow with <code>rules: if:</code>","every push (multibranch); narrow with <code>when { branch }</code>"),
 ("The whole run","workflow","workflow","pipeline","pipeline"),
 ("Unit of work","job (<code>runs-on</code>)","job (<code>docker:</code> executor)","job inside a <code>stage</code>","<code>stage</code> (+ <code>agent</code>)"),
 ("One task","<code>steps: - run:</code> / <code>uses:</code>","<code>steps: - run:</code> / orb command","one <code>script:</code> line","<code>steps { sh '…' }</code>"),
 ("The machine","runner (<code>ubuntu-latest</code>)","executor (<code>cimg/node:22.12</code>)","runner (<code>image: node:22-alpine</code>)","agent (<code>docker { image }</code>)"),
 ("Matrix 📏","<code>strategy: matrix:</code>","<code>matrix: parameters:</code>","<code>parallel: matrix:</code>","<code>matrix { axes { … } }</code>"),
 ("Cache 🗄️","<code>actions/cache</code> keyed by <code>hashFiles()</code>","<code>restore_cache</code> / <code>save_cache</code> keyed by <code>checksum</code>","<code>cache: key: files:</code>","none built in — persistent workspace or the Job Cacher plugin"),
 ("Artifact 📎","<code>upload-artifact</code> / <code>download-artifact</code>","<code>store_artifacts</code> / <code>persist_to_workspace</code>","<code>artifacts: paths:</code>","<code>archiveArtifacts</code> / <code>stash</code>"),
 ("Test report 📋","upload the JUnit XML as an artifact","<code>store_test_results</code>","<code>artifacts: reports: junit</code> (MR widget)","<code>junit</code> step"),
 ("Secrets 🔐","<code>secrets.X</code> (masked) · <code>vars.X</code> (plain)","project env vars · <code>context:</code> per job","CI/CD variables (masked, protected)","Credentials + <code>withCredentials</code> / <code>withAWS</code>"),
 ("Cloud identity 🪪","<code>permissions: id-token: write</code> + <code>configure-aws-credentials</code>","<code>aws-cli/setup</code> with <code>role_arn</code>","<code>id_tokens:</code> + <code>assume-role-with-web-identity</code>","plugin or an instance role on the agent"),
 ("Only on main","<code>on: push: branches: [main]</code>","<code>filters: branches: only: main</code>","<code>rules: - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH</code>","<code>when { branch 'main' }</code>"),
 ("Approval gate 🛑","<code>environment:</code> + required reviewers","<code>type: approval</code>","<code>when: manual</code>","<code>input</code> step"),
 ("Environments","<code>environment: staging / production</code>","contexts + approval jobs","<code>environment: name:</code>","stages (plugins add more)"),
]
tabs="".join(f'<button class="tab" role="tab" aria-selected="{"true" if i==0 else "false"}" data-tab="{k}">{t}</button>' for i,(k,t,_) in enumerate(FILES))
panels=[]
for i,(k,t,paths) in enumerate(FILES):
    blocks="".join(f'<p class="path">📄 {p}</p><pre><code>{html.escape(open(f"{R}/{p}",encoding="utf-8").read())}</code></pre>' for p in paths)
    panels.append(f'<div class="panel{" on" if i==0 else ""}" data-panel="{k}" role="tabpanel">{blocks}</div>')
table="".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td></tr>" for a,b,c,d,e in ROWS)
desc="The same CI/CD pipeline written four times — GitHub Actions, CircleCI, GitLab CI and Jenkins — with a Rosetta table mapping every concept to each dialect's keyword."
page=f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><meta content="width=device-width, initial-scale=1" name="viewport"/>
<title>Four dialects — 📮 CI/CD</title>
<meta content="{desc}" name="description"/>
<meta content="Four dialects — 📮 CI/CD" property="og:title"/><meta content="{desc}" property="og:description"/><meta content="{SITE}images/big-picture-4k.png" property="og:image"/><meta content="website" property="og:type"/><meta content="summary_large_image" name="twitter:card"/>
{base_css}
{extra}
</head><body><div class="wrap">
<p><a href="index.html">← Back to the course home</a></p>
<h1>🗣️ One pipeline, four dialects</h1>
<p class="sub">Four courier companies, the same route, different forms. Every file below lives in the repo and
  describes the <b>same</b> conveyor: test on three Node versions with a cache and a JUnit report → build,
  smoke-test and push the image tagged with the commit SHA → deploy to staging → a human approves →
  production. Lesson 11 walks through the table; lessons 03–10 show each piece in all four.</p>
<h2 id="rosetta">🪨 The Rosetta table</h2>
<p class="sub">Read a row across and you can translate any pipeline you meet. The keywords are the ones the real files use.</p>
<div class="tablewrap"><table>
<tr><th>Concept</th><th>⚙️ GitHub Actions</th><th>🔄 CircleCI</th><th>🦊 GitLab CI</th><th>🎩 Jenkins</th></tr>
{table}
</table></div>
<div class="callout">🧠 <b>Notice what does NOT change:</b> all four run <code>node prepare.js</code>, <code>node --test</code> and
  <code>docker build … &amp;&amp; docker push</code>. Keep the logic in scripts and package.json, keep the YAML thin, and
  switching vendors becomes a translation instead of a rewrite.</div>
<h2 id="files">📄 The four files, side by side</h2>
<div class="tabs" role="tablist">{tabs}</div>
{"".join(panels)}
<footer>
  Learn CI/CD School · <a href="index.html">Course home</a> · <a href="lesson-diagrams.html#l11">lesson 11 diagram</a> ·
  <a href="{REPO}">github.com/BaluRaut/learn-cicd-school</a> · <a href="{SCHOOL}">🏫 all schools</a> ·
  <a href="{REPO}/issues">🐛 found a mistake?</a>
</footer>
</div>
<script>
(function(){{
  var KEY='cicd-dialect', tabs=[].slice.call(document.querySelectorAll('.tab')), panels=[].slice.call(document.querySelectorAll('.panel'));
  function pick(k){{ tabs.forEach(function(t){{t.setAttribute('aria-selected', t.dataset.tab===k?'true':'false')}}); panels.forEach(function(p){{p.classList.toggle('on', p.dataset.panel===k)}}); try{{localStorage.setItem(KEY,k)}}catch(e){{}} }}
  tabs.forEach(function(t){{ t.addEventListener('click', function(){{ pick(t.dataset.tab) }}) }});
  var saved=null; try{{ saved=localStorage.getItem(KEY) }}catch(e){{}}
  if (location.hash && document.querySelector('.tab[data-tab="'+location.hash.slice(1)+'"]')) pick(location.hash.slice(1)); else if (saved) pick(saved);
}})();
</script>
</body></html>
'''
open(f"{OUT}/pipelines.html","w",encoding="utf-8").write(page)
print("pipelines.html written, rows:", len(ROWS))
