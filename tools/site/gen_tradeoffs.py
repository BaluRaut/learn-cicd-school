import sys, html
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from course import *
S=str(__import__("pathlib").Path(__file__).resolve().parents[2])   # repo root
OUT=__import__("os").environ.get("OUT", f"{S}/docs")
css=open(f"{S}/tools/site/css/before-and-tradeoffs.html.styles.html",encoding="utf-8").read().replace("--accent: #0ea5e9","--accent: #16a34a")

T=[
 ("ci", G, "📮 Continuous Integration — lessons 01–05", "⏮️ Before CI",
  "The merge-day era: everyone worked on a private copy for weeks, then integrated at the end of the term — conflicts, builds that wouldn't compile, a 'build master' who spent days gluing it together, and a printed test checklist someone forgot. Nightly builds helped; CI servers (CruiseControl 2001, Hudson/Jenkins 2005–2011) and later hosted services made check every push the normal way to work.",
  ["feedback in minutes, not weeks","small merges → small conflicts","one shared definition of done: green = mergeable","a clean, repeatable environment for every run"],
  ["the pipeline is code you now maintain","slow or flaky suites erode trust in the green check","runner minutes cost money at scale","each vendor's YAML is its own dialect (lesson 11)"],
  ["more than one person touches the code","anything that ships more than once","any repo with tests worth running"],
  ["a throwaway prototype","no tests yet — write three first, then the pipeline","a run slower than a coffee — fix speed before adding steps"], "l01"),
 ("pipelines-as-code", G, "📜 Pipelines as code — lessons 02, 11", "⏮️ Before pipelines as code",
  "Build jobs were configured by clicking through a web UI on one server nobody dared upgrade; 'job 37' did something important and only Bob knew what. Jenkinsfile (2016), <code>.gitlab-ci.yml</code>, <code>.circleci/config.yml</code> and workflow files moved the pipeline into the repo, next to the code.",
  ["versioned and reviewable in pull requests","each branch carries its own pipeline","reproducible on a fresh server","diffable when something breaks"],
  ["YAML sprawl and copy-paste across repos","hard to run locally (act, gitlab-ci-local — imperfect)","logic hidden in YAML is hard to test","dialect lock-in"],
  ["always, for any pipeline more than one person relies on","when 'how do we build this?' should have one answer: the file"],
  ["don't write logic in YAML — call scripts or package.json so the YAML stays thin and portable","a one-off script you'll run once from a laptop"], "l02"),
 ("oidc", G, "🪪 Short-lived credentials (OIDC) — lesson 06", "⏮️ Before OIDC",
  "Long-lived cloud keys pasted into CI secrets, copied into five repos, rotated rarely, and leaked through logs, forks or an old laptop — a recurring theme in public incident write-ups. OIDC federation lets the CI run present a signed identity token and receive credentials that expire in minutes.",
  ["nothing to leak — credentials live for one job","scoped to one repo/branch by the trust policy","every use lands in CloudTrail with the run's identity","no rotation chores"],
  ["one-time setup per cloud account and CI vendor","the <code>sub</code> condition is easy to get subtly wrong (too wide = any repo can assume the role)","some older tools still expect static keys"],
  ["any deploy from CI to AWS, GCP or Azure (all support it)","the moment a key would otherwise be pasted into a secret"],
  ["self-hosted runners already inside the cloud can use instance or pod identity instead","a personal sandbox with nothing to protect — fine to start, don't graduate it"], "l06"),
 ("gates", A, "🛑 Environments &amp; approval gates — lesson 08", "⏮️ Before gates",
  "Whoever had the production password deployed; change windows lived on a shared spreadsheet; 'don't deploy on Fridays'; and nobody could say who approved what. Environments with protection rules put a named human, a staging step and an audit trail in front of production.",
  ["a named human accountable for each production change","staging first catches the obvious","the audit trail is free","blast-radius control (which branches may deploy where)"],
  ["gates rot into rubber stamps","approvals queue up and stretch lead time","a gate that never says no is pure delay","humans approve badly at 2 a.m."],
  ["production and anything regulated","the first months of a new pipeline, while trust is built"],
  ["staging and dev — automate fully","a gate that hasn't rejected anything in months: replace it with an automated check and measure"], "l08"),
 ("progressive", A, "🔁 Progressive delivery — lesson 09", "⏮️ Before rolling / blue-green / canary",
  "'Maintenance window 02:00–04:00', big-bang deploys of everything at once, and rollbacks by restoring last week's tarball. Rolling updates, blue/green and canaries replace the pins gradually — and let you put yesterday's notice back in seconds.",
  ["no downtime for users","fast rollback: flip back or redeploy the previous SHA","learn from a small slice before everyone sees it","pairs with readiness probes so bad pods never get traffic"],
  ["old and new run side by side → releases must be backward compatible","blue/green needs double capacity for a while","a canary is only as good as the metrics you watch","database schema changes need expand/contract discipline"],
  ["user-facing services","anything with an SLO","teams that deploy often"],
  ["batch jobs and one-shot scripts","schema-breaking changes — migrate first","tiny internal tools where a short blip is fine"], "l09"),
 ("push", A, "🚚 Push-model CD (vs GitOps) — lessons 10, 12", "⏮️ Before any pipeline deployed",
  "<code>kubectl apply</code> from whichever laptop happened to hold the kubeconfig — 'works on my cluster'. A push pipeline made that repeatable: the courier drives to the cluster and applies. It is a huge upgrade, with one blind spot the ArgoCD school opens with.",
  ["one tool for build and deploy","the run log is the deploy log — simple to reason about","works for any target: Kubernetes, VMs, Lambda, S3 sites"],
  ["the pipeline holds cluster access — a valuable target","nothing watches the cluster afterwards → drift","deploy state lives in CI history, not in git","many clusters = many kubeconfigs in CI"],
  ["getting started","non-Kubernetes targets","a single cluster owned by one team"],
  ["many clusters or many teams — that's the ArgoCD school (pull, self-heal, drift-free)","when 'who changed prod by hand?' has come up more than once"], "l10"),
 ("hosted", I, "🏢 Hosted vs self-hosted CI — lesson 11", "⏮️ Before hosted CI",
  "One Jenkins box under a desk, upgraded never, disk full on release day. Hosted services (Travis CI 2011, CircleCI 2011, GitLab CI 2012, GitHub Actions 2019) sell the mailroom as a service; self-hosted runners let you keep the machines while the SaaS keeps the schedule.",
  ["hosted: zero maintenance, elastic, free allowance for open source","self-hosted: private-network access, special hardware, predictable cost at scale","the best of both: hosted control plane + self-hosted runners"],
  ["hosted: minutes/credits bills grow, noisy neighbors, vendor limits","self-hosted: you patch, scale and secure it","a compromised self-hosted runner has your secrets"],
  ["hosted for most teams, most of the time","self-hosted runners when builds need private networks, GPUs or compliance says so"],
  ["running your own controller (a whole Jenkins) without someone owning it","self-hosting to 'save money' before measuring the minutes"], "l11"),
]
toc="".join(f'<a href="#{i}">{t.split(" — ")[0]}</a>' for i,_,t,*_ in T)
secs=[]
for i,c,t,hb,hp,mer,dem,use,avoid,dl in T:
    li=lambda xs:"".join(f"<li>{x}</li>" for x in xs)
    secs.append(f'''<section class="term" id="{i}" style="--c:{c}">
<h2>{t}</h2>
<div class="hist"><b>{hb}</b>
<p>{hp}</p>
</div>
<div class="quad">
<div class="q merit"><h4>✅ Merits</h4><ul>{li(mer)}</ul></div>
<div class="q demerit"><h4>❌ Demerits</h4><ul>{li(dem)}</ul></div>
<div class="q use"><h4>👍 Use when</h4><ul>{li(use)}</ul></div>
<div class="q avoid"><h4>👎 Think twice when</h4><ul>{li(avoid)}</ul></div>
</div>
<p class="foot"><a href="lesson-diagrams.html#{dl}">Diagram ↗</a></p>
</section>''')
desc="For every big CI/CD idea: what the world looked like before it, its merits and demerits, and where to use it vs where not."
page=f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<title>Before &amp; trade-offs — Learn CI/CD School</title>
<meta content="{desc}" name="description"/>
<meta content="Before &amp; trade-offs — Learn CI/CD School" property="og:title"/>
<meta content="{desc}" property="og:description"/>
<meta content="{SITE}images/big-picture-4k.png" property="og:image"/>
<meta content="website" property="og:type"/>
<meta content="summary_large_image" name="twitter:card"/>
{css}
</head>
<body>
<div class="wrap">
<header>
<p><a href="index.html">← Back to the course home</a></p>
<h1>⏮️ Before &amp; trade-offs</h1>
<p class="sub">Every tool replaced something worse — and is itself the wrong tool somewhere.
  For each big idea in this course: what life was like <b>before</b> it, its honest
  <b>merits ✅ and demerits ❌</b>, and <b>where to use it 👍 vs where not 👎</b>.</p>
<nav class="toc">
{toc}
</nav>
</header>
{chr(10).join(secs)}
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
open(f"{OUT}/before-and-tradeoffs.html","w",encoding="utf-8").write(page)
print("before-and-tradeoffs written:", page.count("<section"), "sections")
