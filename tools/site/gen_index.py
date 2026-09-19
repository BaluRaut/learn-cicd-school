import sys, os, re, html
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from course import *
S=str(__import__("pathlib").Path(__file__).resolve().parents[2])   # repo root
OUT=__import__("os").environ.get("OUT", f"{S}/docs")
styles=open(f"{S}/tools/site/css/index.html.styles.html",encoding="utf-8").read().replace("--accent: #0ea5e9","--accent: #16a34a")
main_css, dsec_css, chk_css = [s+"</style>" for s in styles.split("</style>") if s.strip()]
diag_css=open(f"{S}/tools/site/css/lesson-diagrams.html.styles.html",encoding="utf-8").read().replace("--accent: #0ea5e9","--accent: #16a34a")
DIAG=f"{S}/tools/site/diagrams.html"
diagrams=open(DIAG,encoding="utf-8").read() if os.path.exists(DIAG) else "<!-- DIAGRAMS PENDING -->"

def card(n,slug,emo,title,ana,c):
    return (f'<div class="lesson" style="--c:{c}"><div class="top"><span class="num">{n}</span><h3>{emo} {title}</h3></div>'
            f'<span class="ana">{ana}</span><code>{branch(n,slug)}</code>'
            f'<a class="go" href="{lesson_url(n,slug)}">Read lesson →</a><a class="go" href="lesson-diagrams.html#l{n:02d}">See the diagram ↗</a></div>')
def grid(nums): return '<div class="grid">\n'+"\n".join(card(*LESSONS[n-1]) for n in nums)+'\n</div>'

DESC="12 branch-by-branch lessons: CI (tests on every push, cache, artifacts, OIDC), CD (build, gates, deploy strategies, Kubernetes) and the same pipeline in GitHub Actions, CircleCI, GitLab CI and Jenkins — ELI5 school analogies, diagrams and hands-on labs."
META=f'''<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<title>Learn CI/CD the school way</title>
<meta content="{DESC}" name="description"/>
<meta content="Learn CI/CD the school way" property="og:title"/>
<meta content="{DESC}" property="og:description"/>
<meta content="{SITE}images/big-picture-4k.png" property="og:image"/>
<meta content="website" property="og:type"/>
<meta content="summary_large_image" name="twitter:card"/>'''

index=f'''<!DOCTYPE html>
<html lang="en">
<head>
{META}
{main_css}
{dsec_css}
</head>
<body>
<svg height="0" style="position:absolute" width="0"><defs>
<marker id="arw" markerheight="7" markerwidth="7" orient="auto-start-reverse" refx="9" refy="5" viewbox="0 0 10 10">
<path d="M0 0 L10 5 L0 10 z" fill="#64748b"></path>
</marker>
</defs></svg>
<div class="wrap">
<header>
<h1>📮 Learn CI/CD the school way</h1>
<p class="sub">Course <b>3 of 4</b> in the school's Ops track — <a href="https://baluraut.github.io/learn-docker-school/">Docker</a>
    packed the lunchbox and <a href="https://baluraut.github.io/learn-kubernetes-school/">Kubernetes</a> runs it; something
    has to <b>check it, copy it and deliver it</b> on every push. That's this course: the school's mailroom and courier
    service — continuous integration, continuous delivery, and the same pipeline written in
    <b>four dialects</b> (GitHub Actions, CircleCI, GitLab CI, Jenkins). Afterwards,
    <a href="https://baluraut.github.io/learn-argocd-school/">ArgoCD</a> keeps the cluster honest.</p>
<div class="chips">
<span class="chip">✅ tests on every push</span><span class="chip">🗄️ cache</span><span class="chip">📎 artifacts</span>
<span class="chip">🪪 OIDC, no stored keys</span><span class="chip">📦 image = commit SHA</span><span class="chip">🛑 approval gates</span>
<span class="chip">🔁 rolling · blue/green · canary</span><span class="chip">🚚 kubectl from CI</span><span class="chip">🗣️ four dialects</span>
</div>
</header>
<div class="vs">
<div class="vcol" style="border-top: 5px solid {G}">
<h3>✅ Part 1 — CHECK IT (free, in your fork)</h3>
<ul>
<li>why the term-end homework pile-up is integration hell</li>
<li>triggers, jobs, steps, runners — the conveyor belt</li>
<li>green check on every push; cache hits, matrix, artifacts</li>
<li>secrets done right: the courier's badge (OIDC), least privilege</li>
</ul>
</div>
<div class="vcol" style="border-top: 5px solid {A}">
<h3>🚚 Part 2 — DELIVER IT (local cluster or AWS)</h3>
<ul>
<li>build, smoke-test and file the image: tag = the commit SHA</li>
<li>staging → the principal's signature → production</li>
<li>rolling, blue/green, canary — and a 10-second rollback</li>
<li>the delivery van: kubectl from CI, rollout status as the gate</li>
</ul>
</div>
<div class="vcol" style="border-top: 5px solid {I}">
<h3>🗣️ Part 3 — THE REAL WORLD</h3>
<ul>
<li>one Rosetta table: GitHub Actions · CircleCI · GitLab CI · Jenkins</li>
<li>hosted vs self-hosted; keep logic in scripts, YAML thin</li>
<li>hygiene: pin by SHA, quarantine flaky tests, DORA's four metrics</li>
<li>what push pipelines can't fix → the ArgoCD school</li>
</ul>
</div>
</div><div class="callout">🎯 <b>After this course you should be able to:</b> explain CI vs continuous delivery vs continuous deployment · read any pipeline file and name its trigger, jobs, steps and runner · make a pipeline fast with caches and a matrix without making it lie · move files between jobs and publish test reports · deploy from CI to a cloud with <b>no stored keys</b> · put an approval gate and a staging step in front of production · choose rolling, blue/green or canary and roll back in seconds · translate the same pipeline between four CI systems · say what a push pipeline still can't do, and why the next course exists.</div>
<h2 id="big-picture">🗺️ The big picture — one diagram, the whole journey</h2>
<p class="sub">The whole course on one canvas: CHECK IT (green, lessons 1–6), DELIVER IT (amber, lessons 7–10)
  and THE REAL WORLD (indigo, lessons 11–12). Click it for the <a href="images/big-picture-4k.png">4K version</a> —
  great as a single reference.</p>
<figure style="background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px;margin-top:16px">
<a href="images/big-picture-4k.png"><img alt="The big picture: CI checks every push in the mailroom, CD copies the image to ECR and delivers it to Kubernetes through staging and an approval gate, and four dialects describe the same pipeline" loading="lazy" src="images/big-picture.svg" style="width:100%;height:auto;display:block"/></a>
</figure>
<h2 id="part1">✅ Part 1 — CHECK IT: continuous integration (lessons 1–6)</h2>
<p class="sub">Everything here runs in a fork of this repo on GitHub's free runners — no cloud account, no cost.
  One git branch = one idea; branch 04 contains lessons 01–04.</p>
{grid([1,2,3,4,5,6])}
<div class="callout">🎯 <b>After Part 1 you should be able to explain:</b> what a pipeline run is made of · why the cache key is a hash of the inputs · artifact vs cache · why the run's token has <code>contents: read</code> and nothing more · how a CI job gets cloud credentials without a single stored key.</div>
<h2 id="part2">🚚 Part 2 — DELIVER IT: continuous delivery (lessons 7–10)</h2>
<p class="sub">From a green check to a running version: the photocopier, the locker, the signature, the van.
  The labs run on a local cluster (Docker Desktop or kind); the AWS steps are marked and optional.</p>
{grid([7,8,9,10])}
<div class="callout">🎯 <b>After Part 2 you should be able to explain:</b> why the image tag is the commit SHA · what pauses a production job until a human approves, and where that approval is recorded · how a rolling update with a readiness probe avoids downtime · the four commands the delivery van runs, and what nobody does after it leaves.</div>
<h2 id="part3">🗣️ Part 3 — THE REAL WORLD: four dialects, one rulebook (lessons 11–12)</h2>
<p class="sub">The same pipeline exists four times in this repo. Learn to translate, then learn the habits that keep
  a mailroom trustworthy — and where this course hands over to GitOps.</p>
{grid([11,12])}
<div class="callout">🎯 <b>After Part 3 you should be able to:</b> read a CircleCI, GitLab or Jenkins pipeline you have never seen · say which of DORA's four metrics a change would move · name what a push pipeline cannot see (drift) and which course fixes it.</div>
<pre><code># take the course locally (a GitHub account for Part 1; Docker Desktop or kind for the local labs):
gh repo fork BaluRaut/learn-cicd-school --clone
cd learn-cicd-school
git checkout lesson-01-why-cicd   # then open lessons/01-why-cicd/README.md</code></pre>
<div class="callout">🗣️ <b>Four dialects, side by side:</b> the repo carries <code>.github/workflows/</code>, <code>.circleci/config.yml</code>, <code>.gitlab-ci.yml</code> and a <code>Jenkinsfile</code> that all describe the same conveyor. The <a href="pipelines.html">four-dialect page</a> shows them in tabs with a Rosetta table — every lesson from 03 to 10 also shows its step in all four.</div>
<div class="callout">🎓 <b>The school series:</b> 0️⃣ <a href="https://baluraut.github.io/learn-aws-school/">AWS foundations</a> → 1️⃣ <a href="https://baluraut.github.io/learn-docker-school/">Docker &amp; ECR</a> packs the image →
    2️⃣ <a href="https://baluraut.github.io/learn-kubernetes-school/">Kubernetes</a> runs it at scale → 3️⃣ this course checks, copies and delivers it on every push →
    4️⃣ <a href="https://baluraut.github.io/learn-argocd-school/">ArgoCD</a> keeps the cluster honest, forever. Same style, same analogies universe, same demo-app family.</div>
<h2 id="diagrams">📐 The lesson diagrams — follow the numbers</h2>
<p class="sub">Every lesson as one numbered box-and-arrow diagram, one after another —
  readable right here (green = CI, amber = CD, indigo = the real world). Also on a
  <a href="lesson-diagrams.html">standalone page</a> with jump navigation.</p>
{diagrams}
<h2 id="graduation">🎓 Graduation test — can you explain this?</h2>
<div class="callout"><i>A developer opens a pull request. CI runs the tests on three Node versions, reusing a cache, and uploads a JUnit report. After the merge to main, the pipeline builds the image, smoke-tests it, tags it with the commit SHA and pushes it to ECR using temporary credentials. Staging is updated automatically; a reviewer approves; production rolls out one pod at a time behind a readiness probe.</i><br/>
<b>CI checks the change · the image is the artifact · the tag is the version · the environment is the gate · the rollout is the strategy.</b> Now answer, one sentence each:</div>
<ol class="grad">
<li>What triggered the run, and which file listened for it?</li><li>Why did the three test jobs run in parallel?</li><li>What decides whether the cache is a hit?</li><li>Where does the JUnit report go, and why "if: always()"?</li><li>How did the push job get AWS credentials without a stored key?</li><li>What exactly identifies the image that was deployed?</li><li>What made the production job wait, and where is the approval recorded?</li><li>Why did the rollout never take the service down?</li><li>How would you roll back, and why that way?</li><li>What is nobody watching after the pipeline finishes — and which course fixes it?</li>
</ol>
<h2 id="checklist">☑️ Course completion checklist</h2>
<p class="sub">Tick honestly — <b>saved in this browser</b>.</p>
<div class="chk" id="chk">
<label><input data-c="c1" type="checkbox"/> I can explain CI vs continuous delivery vs continuous deployment</label>
<label><input data-c="c2" type="checkbox"/> I can name the trigger, jobs, steps and runner in a pipeline file</label>
<label><input data-c="c3" type="checkbox"/> I have a green check on a fork of this repo</label>
<label><input data-c="c4" type="checkbox"/> I have made a pipeline red on purpose and fixed it</label>
<label><input data-c="c5" type="checkbox"/> I can explain a cache key, a hit and a miss</label>
<label><input data-c="c6" type="checkbox"/> I know when to use a matrix vs separate jobs</label>
<label><input data-c="c7" type="checkbox"/> I can tell an artifact from a cache</label>
<label><input data-c="c8" type="checkbox"/> I can explain OIDC to a cloud in one breath</label>
<label><input data-c="c9" type="checkbox"/> I can build, smoke-test and tag an image in CI</label>
<label><input data-c="c10" type="checkbox"/> I can put an approval gate in front of production</label>
<label><input data-c="c11" type="checkbox"/> I can choose between rolling, blue/green and canary</label>
<label><input data-c="c12" type="checkbox"/> I can roll back in under a minute</label>
<label><input data-c="c13" type="checkbox"/> I can deploy to Kubernetes from a pipeline</label>
<label><input data-c="c14" type="checkbox"/> I can translate a pipeline between two CI systems</label>
<label><input data-c="c15" type="checkbox"/> I can name DORA's four metrics and what a push pipeline can't fix</label>
</div>
<p class="sub" id="chk-count"></p>
{chk_css}
<script>(function(){{var K="cicd-checklist",st={{}};try{{st=JSON.parse(localStorage.getItem(K)||"{{}}")}}catch(e){{}}
var bx=[].slice.call(document.querySelectorAll("#chk input"));function r(){{var d=bx.filter(function(b){{return b.checked}}).length;document.getElementById("chk-count").textContent=d+" / "+bx.length+(d===bx.length?" — 🎓 done!":"")}}
bx.forEach(function(b){{b.checked=!!st[b.dataset.c];b.addEventListener("change",function(){{st[b.dataset.c]=b.checked;try{{localStorage.setItem(K,JSON.stringify(st))}}catch(e){{}}r()}})}});r()}})();</script><a class="btn" href="{REPO}">⭐ Open the repo</a>
<a class="btn alt" href="lesson-diagrams.html">📐 All 12 lesson diagrams</a>
<a class="btn alt" href="pipelines.html">🗣️ Four dialects</a>
<a class="btn alt" href="quiz.html">🧪 Quiz</a>
<a class="btn alt" href="study-plan.html">🗓️ Study plan</a>
<a class="btn alt" href="before-and-tradeoffs.html">⏮️ Before &amp; trade-offs</a>
<a class="btn alt" href="https://baluraut.github.io/learn-argocd-school/">🤖 Next course: ArgoCD</a>
<footer>
    Learn CI/CD School · check it, copy it, deliver it ·
    <a href="{REPO}">github.com/BaluRaut/learn-cicd-school</a> ·
    next: <a href="https://baluraut.github.io/learn-argocd-school/">learn-argocd-school</a> ·
    before: <a href="https://baluraut.github.io/learn-kubernetes-school/">learn-kubernetes-school</a>
   ·
  <a href="{SCHOOL}">🏫 all schools</a>
 ·
  <a href="{REPO}/issues">🐛 found a mistake?</a>
</footer>
</div>
</body>
</html>
'''
open(f"{OUT}/index.html","w",encoding="utf-8").write(index)

toc="".join(f'<a href="#l{n:02d}">{n} {re.sub("&amp;","&",t)}</a>' for n,slug,emo,t,ana,c in LESSONS)
ld=f'''<!DOCTYPE html>
<html lang="en">
<head>
{META.replace("<title>Learn CI/CD the school way</title>","<title>Lesson diagrams — Learn CI/CD School</title>").replace(DESC,"All 12 lessons as numbered entity &amp; sequence diagrams — pipelines, caches, artifacts, OIDC, images, gates, deploy strategies and the four dialects — on one page.").replace('content="Learn CI/CD the school way" property="og:title"','content="Lesson diagrams — Learn CI/CD School" property="og:title"')}
{diag_css}
</head>
<body>
<svg height="0" style="position:absolute" width="0"><defs>
<marker id="arw" markerheight="7" markerwidth="7" orient="auto-start-reverse" refx="9" refy="5" viewbox="0 0 10 10">
<path d="M0 0 L10 5 L0 10 z" fill="#64748b"></path>
</marker>
</defs></svg>
<div class="wrap">
<header>
<p><a href="index.html">← Back to the course home</a></p>
<h1>📐 The 12 lessons as diagrams</h1>
<p class="sub">Part 1: CHECK IT (green, lessons 1–6) · Part 2: DELIVER IT (amber, lessons 7–10) · Part 3: THE REAL WORLD
  (indigo, lessons 11–12). Follow the circled numbers <b>1 → 2 → 3</b> in each picture.</p>
<nav class="toc">
{toc}
</nav>
</header>
{diagrams}
<footer>
  Learn CI/CD School ·
  <a href="index.html">Course home</a> ·
  <a href="{REPO}">github.com/BaluRaut/learn-cicd-school</a> ·
  next course: <a href="https://baluraut.github.io/learn-argocd-school/">ArgoCD</a>
 ·
  <a href="{SCHOOL}">🏫 all schools</a>
 ·
  <a href="{REPO}/issues">🐛 found a mistake?</a>
</footer>
</div>
</body>
</html>
'''
open(f"{OUT}/lesson-diagrams.html","w",encoding="utf-8").write(ld)
print("index + lesson-diagrams written; diagrams:", "present" if os.path.exists(DIAG) else "PENDING placeholder")
