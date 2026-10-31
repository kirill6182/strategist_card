"""Тёмная RPG-тема с неоновыми акцентами (cyan / violet)."""

CSS = """
<style>
:root{--cyan:#22d3ee;--violet:#a78bfa;--panel:#121829;--line:#24304d;--muted:#8b93a7;--bad:#fb7185;}
.stApp{background:radial-gradient(1200px 600px at 10% -10%,#1a1440 0%,transparent 60%),#0b0f1a;}
.block-container{max-width:1100px;padding-top:2rem;}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;}
.panel-title{font-size:1.15rem;font-weight:700;margin:1.6rem 0 .6rem;color:var(--cyan);
  text-shadow:0 0 12px rgba(34,211,238,.45);letter-spacing:.02em;}
.badge{display:inline-block;padding:.25rem .8rem;border:1px solid var(--violet);color:var(--violet);
  border-radius:999px;font-weight:600;box-shadow:0 0 12px rgba(167,139,250,.35);}
.lvl{font-size:1.6rem;font-weight:800;color:var(--cyan);text-shadow:0 0 14px rgba(34,211,238,.6);}
.xp-track{height:14px;background:#0e1424;border:1px solid var(--line);border-radius:999px;overflow:hidden;}
.xp-fill{height:100%;background:linear-gradient(90deg,var(--cyan),var(--violet));
  box-shadow:0 0 14px var(--cyan);transition:width .6s ease;}
.xp-label{color:var(--muted);font-size:.8rem;margin-top:.25rem;}
.stat-card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:.8rem 1rem;
  margin-bottom:.4rem;transition:border-color .3s,box-shadow .3s;}
.stat-card:hover{border-color:var(--cyan);box-shadow:0 0 16px rgba(34,211,238,.25);}
.stat-top{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:.5rem;}
.stat-name{font-weight:600;}
.stat-val{font-size:1.4rem;font-weight:800;color:var(--cyan);}
.stat-val small{font-size:.75rem;color:var(--muted);}
.segs{display:grid;grid-template-columns:repeat(10,1fr);gap:3px;}
.seg{height:10px;border-radius:2px;background:#1b2440;transition:background .35s,box-shadow .35s;}
.seg.on{background:linear-gradient(180deg,var(--cyan),var(--violet));box-shadow:0 0 8px rgba(34,211,238,.6);}
.tip{position:relative;}
.tip:hover::after{content:attr(data-tip);position:absolute;left:0;top:105%;z-index:99;width:max-content;
  max-width:260px;background:#1b2440;border:1px solid var(--cyan);border-radius:8px;padding:.5rem .7rem;
  font-size:.8rem;color:#e5e7eb;box-shadow:0 8px 24px rgba(0,0,0,.5);}
.effect{background:var(--panel);border-left:3px solid var(--cyan);border-radius:8px;padding:.5rem .8rem;}
.effect.debuffs{border-left-color:var(--bad);}
.effect span{display:block;color:var(--muted);font-size:.82rem;}
.trait{background:var(--panel);border-radius:8px;padding:.45rem .8rem;border:1px solid var(--line);}
.empty{text-align:center;color:var(--muted);border:1px dashed var(--line);border-radius:12px;padding:1.2rem .6rem;}
.empty .ico{font-size:1.8rem;display:block;margin-bottom:.3rem;}
.diary{width:100%;border-collapse:collapse;font-size:.9rem;}
.diary th{color:var(--violet);text-align:left;border-bottom:1px solid var(--line);padding:.4rem .5rem;}
.diary td{border-bottom:1px solid #182038;padding:.45rem .5rem;vertical-align:top;}
.diary tr:hover td{background:rgba(34,211,238,.05);}
.diary .dl{overflow-x:auto;}
.stButton>button,.stDownloadButton>button{border:1px solid var(--line);transition:all .25s;}
.stButton>button:hover,.stDownloadButton>button:hover{border-color:var(--cyan);color:var(--cyan);
  box-shadow:0 0 12px rgba(34,211,238,.35);}
#MainMenu,footer{visibility:hidden;}
</style>
"""
