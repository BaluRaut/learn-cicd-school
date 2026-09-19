# Single source of truth for the learn-cicd-school site generator.
SITE = "https://baluraut.github.io/learn-cicd-school/"
REPO = "https://github.com/BaluRaut/learn-cicd-school"
SCHOOL = "https://baluraut.github.io/school/"
G, A, I = "#16a34a", "#d97706", "#4f46e5"     # Part 1 CI · Part 2 CD · Part 3 real world

LESSONS = [
 # num, slug, emoji, title, analogy one-liner (card), part color
 (1,  "why-cicd",              "📮", "Why CI/CD",                    "The homework pile-up vs a mailroom that checks every submission the day it arrives.", G),
 (2,  "pipeline-anatomy",      "🧩", "Anatomy of a pipeline",        "The conveyor belt: a bell (trigger), desks (jobs), tasks (steps), clerks (runners) — same words, four dialects.", G),
 (3,  "first-pipeline",        "✅", "Your first pipeline",          "The checking desk stamps ✅ or ❌ on every push — fork it and watch it go green.", G),
 (4,  "cache-parallel-matrix", "⚡", "Fast pipelines",               "The drawer of sharpened pencils (cache), several desks at once (parallel), three rulers (matrix).", G),
 (5,  "artifacts-reports",     "📎", "Artifacts &amp; test reports", "The envelope carried between desks, and the report card pinned on the board.", G),
 (6,  "secrets-oidc",          "🪪", "Secrets &amp; least privilege", "The courier never carries the master key — it shows a badge and gets a day pass (OIDC). 🔗 IAM", G),
 (7,  "build-push-image",      "📦", "Build &amp; push the image",   "The photocopier: copy the checked homework, label it with the commit's fingerprint, file it in the locker. 🔗 Docker", A),
 (8,  "environments-gates",    "🛑", "Environments &amp; gates",     "The practice board first; the principal signs before anything reaches the main board.", A),
 (9,  "deploy-strategies",     "🔁", "Deploy strategies &amp; rollback", "Replace the pins one by one, flip between two boards, or show the notice to one class first. 🔗 Kubernetes", A),
 (10, "deploy-to-kubernetes",  "🚚", "Deploy to Kubernetes from CI", "The delivery van: drive to the cluster with the day pass, pin the notice, wait until it's readable.", A),
 (11, "four-dialects",         "🗣️", "The same pipeline in four dialects", "Four courier companies, same route, different forms: GitHub Actions, CircleCI, GitLab CI, Jenkins.", I),
 (12, "pipeline-hygiene",      "🧹", "Pipeline hygiene &amp; the handoff", "The mailroom rulebook, the DORA scoreboard — and the baton pass to ArgoCD.", I),
]

def branch(n, slug): return f"lesson-{n:02d}-{slug}"
def lesson_url(n, slug): return f"{REPO}/blob/{branch(n,slug)}/lessons/{n:02d}-{slug}/README.md"

QUIZ = [
 {"q":"CI vs continuous delivery vs continuous deployment?","o":["Three names for the same thing","Integrate + check on every push · always releasable (a human presses the button) · every green change goes live automatically","CI is for developers, CD is for operations"],"c":1,"w":"L01: the mailroom checks every submission; delivery keeps a button; deployment removes the button."},
 {"q":"Which one is the RUNNER?","o":["The YAML file","The machine that executes a job's steps","The git branch being built"],"c":1,"w":"L02: desks (jobs) need clerks (runners)."},
 {"q":"You push to a feature branch. Which ship.yml jobs run?","o":["All of them","None — ship.yml listens only to pushes on main; ci.yml is what runs on every branch","Only the deploy job"],"c":1,"w":"L03/L07: `on: push: branches: [main]` — the photocopier only copies homework that reached main."},
 {"q":"You change one space character in app/prepare.js. The next run's cache is a…","o":["Hit — whitespace doesn't count","Miss — the key is hashFiles('app/prepare.js') and the bytes changed","Hit, but slower"],"c":1,"w":"L04: the key IS the hash of the file's bytes; a new key means an empty drawer."},
 {"q":"Artifact vs cache?","o":["The same mechanism with two names","Artifact = an output of this run kept for humans or later jobs; cache = a speed-up that may vanish","Caches are for tests, artifacts are for images"],"c":1,"w":"L05: the envelope vs the drawer."},
 {"q":"Why does the push job download image.tar.gz instead of reusing the image the build job made?","o":["Docker requires it","Each job runs on a fresh machine — nothing from job A exists in job B unless it travels as an artifact","To slow the run down on purpose"],"c":1,"w":"L05: desks don't share drawers."},
 {"q":"OIDC in ship.yml means…","o":["AWS keys are stored as GitHub secrets","No stored keys: the run presents a signed badge and AWS STS hands out temporary credentials for that one job","The runner is hosted inside AWS"],"c":1,"w":"L06: the badge and the day pass — the AWS school's robots never get passwords either."},
 {"q":"The image tag pushed to ECR is…","o":["latest","the full commit SHA","the branch name"],"c":1,"w":"L07: immutable and traceable — the box is labeled with the homework's fingerprint."},
 {"q":"What makes the production job wait for a human?","o":["A sleep step","The `environment: production` key plus required reviewers configured on that environment","A comment in the YAML"],"c":1,"w":"L08: the principal's signature lives in Settings → Environments, not in the file."},
 {"q":"maxSurge: 1, maxUnavailable: 0 with a readiness probe means…","o":["All pods restart at once","One new pod comes up and must answer /healthz before an old one is removed","Zero downtime is impossible"],"c":1,"w":"L09: replace the pins one at a time; the probe is the 'readable?' check."},
 {"q":"The safest default rollback?","o":["SSH to the node and edit the container","Re-run the deploy with yesterday's image tag","Delete the namespace and start over"],"c":1,"w":"L09: the tag is the version and the pipeline is the paved road; `rollout undo` is the emergency lever."},
 {"q":"After a push-model deploy finishes…","o":["The pipeline keeps watching the cluster","Nothing watches the board — hand edits drift silently (the ArgoCD school's opening problem)","Kubernetes reports back to CI"],"c":1,"w":"L10: push ends at apply; GitOps pulls forever."},
 {"q":"CircleCI `type: approval`, GitLab `when: manual`, Jenkins `input` are all…","o":["Ways to run tests in parallel","The manual approval gate in that dialect","Cache settings"],"c":1,"w":"L11: four courier companies, same route, different forms."},
 {"q":"A test fails about once in twenty runs. You should…","o":["Add retries and move on","Quarantine it, fix the cause, then bring it back — retries hide rot","Delete the test"],"c":1,"w":"L12: a flaky test destroys trust in the green check, which is the whole product."},
 {"q":"Pinning `uses: actions/checkout@<full commit SHA>` protects against…","o":["Slow checkouts","A tag being moved to different code later (supply chain)","Nothing — tags can't change"],"c":1,"w":"L12: tags can move; a SHA cannot."},
]

WEEKS = [
 ("WEEK 1","📮 Meet the mailroom",[1,2,3],"fork the repo, push a commit, get a green check — then break a test on purpose and fix it."),
 ("WEEK 2","⚡ Make it fast and safe",[4,5,6],"show a cache MISS then a HIT in the logs, download the JUnit report, and explain OIDC in one sentence."),
 ("WEEK 3","📦 Photocopy and deliver",[7,8,9],"build and smoke-test the image locally; protect main with a required check; roll a new version out on a local cluster and watch pods replace one at a time."),
 ("WEEK 4","🚚 To production, honestly",[10,11,12],"run the four-command deploy loop end to end on a local cluster; redraw the Rosetta table from memory; name DORA's four metrics."),
]
