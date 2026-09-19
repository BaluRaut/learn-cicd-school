import json, re, sys, html
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from course import *
S=str(__import__("pathlib").Path(__file__).resolve().parents[2])   # repo root
OUT=__import__("os").environ.get("OUT", f"{S}/docs")
css=lambda name: open(f"{S}/tools/site/css/{name}.styles.html",encoding="utf-8").read().replace("--accent: #0ea5e9","--accent: #16a34a")

def head(title, desc, extra_css=""):
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><meta content="width=device-width, initial-scale=1" name="viewport"/>
<title>{title}</title>
<meta content="{html.escape(desc)}" name="description"/>
<meta content="{title}" property="og:title"/><meta content="{html.escape(desc)}" property="og:description"/><meta content="{SITE}images/big-picture-4k.png" property="og:image"/><meta content="website" property="og:type"/><meta content="summary_large_image" name="twitter:card"/>
{extra_css}
</head><body><div class="wrap">
'''
FOOT=f'''<footer>Part of <a href="{SCHOOL}">🏫 The School</a> · <a href="index.html">course home</a> · <a href="quiz.html">🧪 quiz</a> · <a href="study-plan.html">🗓️ study plan</a> ·
  <a href="{REPO}/issues">🐛 found a mistake?</a>
</footer>
</div>'''

# ---------------- quiz ----------------
q=f'''{head("Quiz — 📮 CI/CD", f"Self-test quiz for the 📮 CI/CD school — {len(QUIZ)} questions with explanations.", css("quiz.html"))}<p><a href="index.html">← Back to the course home</a></p>
<h1>🧪 The 📮 CI/CD quiz</h1>
<p class="sub">{len(QUIZ)} questions — pick an answer, get the why. One attempt per question (until reset).
Your best score is saved in this browser.</p>
<div class="scorebox"><div class="score" id="score">0 / {len(QUIZ)} · best: —</div></div>
<div id="quiz"></div>
<button class="reset" onclick="reset()">↺ Reset &amp; retake</button>
{FOOT}
<script>
var QS = {json.dumps(QUIZ, ensure_ascii=False)};
var KEY='quiz-cicd-school', answered={{}}, score=0;
var best = parseInt(localStorage.getItem(KEY)||'-1');
function render() {{
  var el = document.getElementById('quiz'); el.innerHTML='';
  QS.forEach(function(q,i) {{
    var card=document.createElement('div'); card.className='qcard';
    card.innerHTML='<h3>'+(i+1)+'. '+q.q+'</h3>';
    q.o.forEach(function(opt,j) {{
      var b=document.createElement('button'); b.className='opt'; b.textContent=opt;
      b.onclick=function() {{
        if (answered[i]!==undefined) return;
        answered[i]=j;
        if (j===q.c) {{ b.classList.add('right'); score++; }}
        else {{ b.classList.add('wrong'); card.querySelectorAll('.opt')[q.c].classList.add('right'); }}
        card.querySelector('.why').style.display='block';
        update();
      }};
      card.appendChild(b);
    }});
    var why=document.createElement('div'); why.className='why'; why.textContent='💡 '+q.w;
    card.appendChild(why);
    el.appendChild(card);
  }});
}}
function update() {{
  var done=Object.keys(answered).length;
  if (done===QS.length && score>best) {{ best=score; localStorage.setItem(KEY,best); }}
  document.getElementById('score').textContent=score+' / '+QS.length+(done===QS.length?' — done! 🎓':'')+' · best: '+(best<0?'—':best+'/'+QS.length);
}}
function reset() {{ answered={{}}; score=0; render(); update(); }}
render(); update();
</script>
</body></html>
'''
open(f"{OUT}/quiz.html","w",encoding="utf-8").write(q)

# ---------------- study plan ----------------
rows=[]
for wk, title, nums, milestone in WEEKS:
    rows.append(f'<section class="week" style="--c:{LESSONS[nums[0]-1][5]}">\n<h2><span class="wk">{wk}</span> {title}</h2>')
    for n in nums:
        num,slug,emo,t,ana,c=LESSONS[n-1]
        rows.append(f'<div class="lesson-row"><input data-l="l{num:02d}" id="sl{num:02d}" type="checkbox"/><label for="sl{num:02d}"><a href="{lesson_url(num,slug)}">{num:02d} · {emo} {t}</a> <span class="time">~40 min</span></label></div>')
    rows.append(f'<div class="milestone">🏁 <b>Checkpoint:</b> {milestone}</div>\n</section>')
sp=f'''{head("Study plan — 📮 CI/CD", "A 4-week study plan for the 📮 CI/CD school: sequence, time estimates, weekly milestones — progress saved in your browser.", css("study-plan.html"))}<p><a href="index.html">← Back to the course home</a></p>
<h1>🗓️ Study plan — 📮 CI/CD</h1>
<p class="sub">12 lessons in 4 weeks (~3 sessions/week: read ~15 min + lab ~25 min).
Tick lessons off — <b>progress saved in this browser</b>.</p>
<div class="progress-box"><div class="progress-inner"><span id="ptext">0 / 12</span><div class="bar"><div id="pbar"></div></div></div></div>
{chr(10).join(rows)}
<div id="done"><h2>🎓 12 / 12 — school complete!</h2>
<p class="sub" style="margin-top:8px">Next stop: <a href="https://baluraut.github.io/learn-argocd-school/">the ArgoCD school</a> — and tick this school off on <a href="{SCHOOL}">the grand path</a>.</p></div>
{FOOT}
<script>
(function() {{
  var KEY='plan-cicd-school', state={{}};
  try {{ state=JSON.parse(localStorage.getItem(KEY)||'{{}}') }} catch(e) {{}}
  var boxes=[].slice.call(document.querySelectorAll('input[data-l]'));
  function render() {{
    var done=boxes.filter(function(b) {{ return b.checked }}).length;
    document.getElementById('ptext').textContent=done+' / '+boxes.length;
    document.getElementById('pbar').style.width=(100*done/boxes.length)+'%';
    document.getElementById('done').style.display=done===boxes.length?'block':'none';
  }}
  boxes.forEach(function(b) {{
    b.checked=!!state[b.dataset.l];
    b.addEventListener('change',function() {{ state[b.dataset.l]=b.checked;
      localStorage.setItem(KEY,JSON.stringify(state)); render(); }});
  }});
  render();
}})();
</script>
</body></html>
'''
open(f"{OUT}/study-plan.html","w",encoding="utf-8").write(sp)
print("quiz + study-plan written")
