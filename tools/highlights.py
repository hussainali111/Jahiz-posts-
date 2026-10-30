# Instagram highlight covers (1080x1920; everything inside the centre square that IG crops to a circle)
import os, sys
src=open('build.py').read()
exec(src[:src.index('BASE=')])
ICONS["phone"]='<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>'
ITEMS=[("ac","snow","تكييف"),("maintenance","wrench","صيانة"),("duct","wind","الدكت"),("tanks","drop","خزانات"),
       ("filters","filter","فلاتر"),("plumbing","pipe","سباكة"),("paint","roller","صباغة"),("tiles","tile","بلاط"),
       ("construction","hardhat","بناء"),("moving","truck","نقل"),("contact","phone","تواصل")]
FONT='<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@900&display=swap" rel="stylesheet">'
def page(inner,bg):
    return f'<!doctype html><html><head>{FONT}</head><body style="margin:0;width:1080px;height:1920px;position:relative;overflow:hidden;font-family:Cairo;background:{bg}">{inner}</body></html>'
def s1(icon,label):  # Sanad + service badge
    return page(f'''<div style="position:absolute;top:420px;left:0;width:1080px;height:1080px;background:radial-gradient(circle at 50% 50%,#fff 0,#f1f1f1 55%,#d9d9d9 100%)"></div>
<img src="sanad.png" style="position:absolute;left:120px;top:560px;width:700px">
<div style="position:absolute;right:120px;top:1010px;width:330px;height:330px;border-radius:50%;background:#D51115;border:16px solid #fff;box-shadow:0 18px 40px rgba(0,0,0,.35);display:flex;align-items:center;justify-content:center">{ic(icon,190,"#fff",2.4)}</div>''','#eee')
def s2(icon,label):  # bold split + label
    return page(f'''<div style="position:absolute;inset:0;background:linear-gradient(135deg,#E3191E 0,#D51115 50%,#3C3C3C 50%,#262626 100%)"></div>
<div style="position:absolute;left:290px;top:560px;width:500px;height:500px;border-radius:50%;background:#fff;box-shadow:0 24px 60px rgba(0,0,0,.45);display:flex;align-items:center;justify-content:center">{ic(icon,300,"#D51115",2.4)}</div>
<div style="position:absolute;top:1110px;left:0;right:0;text-align:center;color:#fff;font-size:150px;font-weight:900;line-height:1.2;text-shadow:0 8px 24px rgba(0,0,0,.4)">{label}</div>''','#D51115')
def s3(icon,label):  # dark glow
    return page(f'''<div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 46%,#D51115 0,#7a0a0c 30%,#2a2a2a 62%,#1c1c1c 100%)"></div>
<div style="position:absolute;left:215px;top:500px;width:650px;height:650px;border-radius:50%;border:10px solid rgba(255,255,255,.85);box-shadow:0 0 60px rgba(213,17,21,.8),inset 0 0 60px rgba(213,17,21,.6)"></div>
<div style="position:absolute;left:0;right:0;top:600px;display:flex;justify-content:center;filter:drop-shadow(0 0 22px rgba(255,255,255,.6))">{ic(icon,340,"#fff",2.4)}</div>
<div style="position:absolute;top:1170px;left:0;right:0;text-align:center"><span style="background:#D51115;color:#fff;font-size:96px;font-weight:900;padding:0 50px;border-radius:24px;box-shadow:0 10px 30px rgba(0,0,0,.5)">{label}</span></div>''','#1c1c1c')
STYLES={'s1':s1,'s2':s2,'s3':s3}
os.makedirs('out/highlights',exist_ok=True)
for st in sys.argv[1:]:
    for slug,icon,label in ITEMS:
        open(f'out/highlights/{st}-{slug}.html','w').write(STYLES[st](icon,label))
print(' '.join(s for s,_,_ in ITEMS))
