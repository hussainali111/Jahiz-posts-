# Instagram highlight covers (1080x1920, icon centered for the circle crop)
import os
src=open('build.py').read()
exec(src[:src.index('BASE=')])
ICONS["phone"]='<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>'
ITEMS=[("ac","snow","تكييف مركزي"),("maintenance","wrench","صيانة"),("duct","wind","الدكت"),("tanks","drop","الخزانات"),
       ("filters","filter","فلاتر المياه"),("plumbing","pipe","سباكة"),("paint","roller","صباغة وجبس"),("tiles","tile","بلاط"),
       ("construction","hardhat","بناء"),("moving","truck","فك ونقل"),("contact","phone","تواصل")]
os.makedirs('out/highlights',exist_ok=True)
for slug,icon,label in ITEMS:
    open(f'out/highlights/{slug}.html','w').write(f'''<!doctype html><html><body style="margin:0;width:1080px;height:1920px;background:radial-gradient(circle at 50% 45%,#E8252A 0,#D51115 35%,#A80D10 100%);display:flex;align-items:center;justify-content:center">
<div style="width:760px;height:760px;border-radius:50%;border:22px solid rgba(255,255,255,.9);display:flex;align-items:center;justify-content:center">{ic(icon,460,"#fff",2.3)}</div></body></html>''')
print(' '.join(s for s,_,_ in ITEMS))
for s,_,l in ITEMS: print(s,l)
