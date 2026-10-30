import json,sys,os
ICONS={
"wrench":'<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/>',
"snow":'<path d="M12 2v20M3.3 7l17.4 10M3.3 17L20.7 7M9 4l3 2 3-2M9 20l3-2 3 2"/>',
"bolt":'<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
"clock":'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
"drop":'<path d="M12 2.7l5.7 5.7a8 8 0 1 1-11.4 0z"/>',
"shield":'<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
"heart":'<path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.5-7 10-7 10z"/>',
"sparkle":'<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 17l.7 1.6 1.6.7-1.6.7L19 21.6l-.7-1.6-1.6-.7 1.6-.7z"/>',
"filter":'<path d="M3 4h18l-7 8v6l-4 2v-8z"/>',
"money":'<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="3"/><path d="M6 9v.01M18 15v.01"/>',
"roller":'<rect x="3" y="3" width="14" height="6" rx="1.5"/><path d="M17 6h3v6h-8v3"/><rect x="10" y="15" width="4" height="6" rx="1"/>',
"home":'<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
"tile":'<rect x="3" y="3" width="18" height="18" rx="1.5"/><path d="M3 12h18M12 3v18"/>',
"pipe":'<path d="M3 7h8v5H3z"/><path d="M11 9h4a4 4 0 0 1 4 4v3"/><path d="M16 16h6v5h-6z"/>',
"truck":'<path d="M2 7h11v9H2z"/><path d="M13 10h4l4 4v2h-8z"/><circle cx="6" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>',
"building":'<path d="M4 21V5l8-3v19"/><path d="M12 21h8V9l-8-3"/><path d="M7 8h2M7 12h2M7 16h2M15 12h2M15 16h2"/>',
}
def ic(n,size,color="#D51115",w=1.8):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">{ICONS[n]}</svg>'
PHONE='<svg width="56" height="56" viewBox="0 0 24 24"><circle cx="12" cy="12" r="12" fill="#D51115"/><path d="M8.6 6.5c.4-.4 1-.4 1.3 0l1.3 1.7c.3.4.3.9 0 1.2l-.8.9c.6 1.3 1.6 2.3 2.9 2.9l.9-.8c.3-.3.8-.3 1.2 0l1.7 1.3c.4.3.4.9 0 1.3l-.9.9c-.6.6-1.5.8-2.3.5-3-1.1-5.3-3.4-6.4-6.4-.3-.8-.1-1.7.5-2.3z" fill="#fff"/></svg>'
IG='<svg width="54" height="54" viewBox="0 0 24 24" fill="none" stroke="#D51115" stroke-width="2.2"><rect x="2.5" y="2.5" width="19" height="19" rx="5.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="17.5" cy="6.5" r="1" fill="#D51115"/></svg>'
SHIELD='<svg width="88" height="100" viewBox="0 0 24 27"><path d="M12 1l10 4v8c0 6.5-4.5 10.5-10 12C6.5 23.5 2 19.5 2 13V5z" fill="#D51115"/><circle cx="12" cy="13" r="5.5" fill="none" stroke="#fff" stroke-width="1.6"/><path d="M9.6 13l1.7 1.7 3.2-3.4" fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round"/></svg>'
BASE='''<!doctype html><html dir="rtl" lang="ar"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@500;700;800;900&display=swap" rel="stylesheet">
<style>
:root{--red:#D51115;--gray:#3C3C3C}
*{margin:0;padding:0;box-sizing:border-box}html{width:1080px;height:1920px;overflow:hidden}
body{width:1080px;height:1920px;font-family:Cairo,sans-serif;background:#fff;color:var(--gray);position:relative;overflow:hidden}
.grid{position:absolute;inset:0;background-image:linear-gradient(#e9e9e9 1px,transparent 1px),linear-gradient(90deg,#e9e9e9 1px,transparent 1px);background-size:60px 60px;opacity:.55}
.brand{text-align:center}
.brand img{width:230px;display:block;margin:0 auto}
.brand .t{font-size:19px;font-weight:800;margin-top:4px;white-space:nowrap}
.brand .y{font-size:22px;font-weight:800;color:var(--red);margin-top:2px}
.brand .y:before,.brand .y:after{content:"";display:inline-block;width:34px;height:2px;background:var(--gray);vertical-align:middle;margin:0 10px}
.ring{width:440px;height:440px;border-radius:50%;background:#f4f4f4;border:6px solid var(--red);display:flex;align-items:center;justify-content:center;position:relative}
.ring .b{position:absolute;width:110px;height:110px;border-radius:50%;background:var(--gray);display:flex;align-items:center;justify-content:center;box-shadow:0 10px 24px rgba(0,0,0,.18)}
.ring .b1{top:-20px;left:10px}.ring .b2{bottom:10px;left:-30px}.ring .b3{bottom:-10px;right:20px}
.slogan{position:absolute;left:0;right:0;text-align:center}
.slogan span{display:inline-block;background:var(--red);color:#fff;font-weight:900;font-size:52px;padding:8px 46px;border-radius:60px}
%CSS%
</style></head><body><div class="grid"></div>%BODY%</body></html>'''
def hero(r,scale=1.0):
    b=''.join(f'<div class="b b{i+1}">{ic(n,62,"#fff",1.9)}</div>' for i,n in enumerate(r["heroB"]))
    return f'<div class="ring" style="transform:scale({scale})">{ic(r["hero"],250,"#D51115",1.5)}{b}</div>'
REEL_CSS='''
.stage{position:absolute;top:250px;left:0;width:1080px;height:1350px}
.hook{position:absolute;top:100px;left:40px;right:40px;text-align:center;font-size:58px;font-weight:900;color:var(--gray)}
.brand{position:absolute;top:30px;left:50px;width:300px}
.head{position:absolute;top:40px;right:60px;width:660px;text-align:right}
.head .k{font-weight:900;color:var(--red);line-height:1.15;white-space:nowrap;font-size:84px}
.head .bb{border-right:6px solid var(--red);padding-right:24px;margin-top:10px}
.head .bb div{font-size:56px;font-weight:900;line-height:1.3;white-space:nowrap}
.head .bb div+div{color:var(--red)}
.sub{position:absolute;top:400px;right:60px;width:640px;font-size:30px;font-weight:700;line-height:1.6;text-align:right}
.sub em{font-style:normal;color:var(--red)}
.line{position:absolute;top:515px;right:60px;width:560px;height:3px;background:var(--red);transform-origin:right}
.line:after{content:"";position:absolute;left:-6px;top:-5px;width:13px;height:13px;border-radius:50%;background:var(--red)}
.herobox{position:absolute;left:40px;top:560px}
.icons{position:absolute;top:560px;right:40px;width:520px;display:flex;flex-direction:column;gap:22px}
.ic{display:flex;align-items:center;gap:24px}
.ic .c{flex:0 0 120px;height:120px;border:4px solid var(--red);border-radius:50%;display:flex;align-items:center;justify-content:center;background:#fff}
.ic p{font-size:34px;font-weight:800;line-height:1.3}
.ic p br{display:none}
.cta{position:absolute;top:1060px;left:60px;right:60px;border:3px solid var(--red);border-radius:18px;background:#fff;display:flex;align-items:center;gap:28px;padding:20px 36px}
.cta .tx div:first-child{font-size:40px;font-weight:900}
.cta .tx div:last-child{font-size:40px;font-weight:900;color:var(--red)}
.contact{position:absolute;top:1250px;left:60px;right:60px;border-top:2px solid #ddd;padding-top:26px;display:flex;justify-content:center;align-items:center;gap:50px}
.contact .i{display:flex;align-items:center;gap:16px;font-size:46px;font-weight:800;direction:ltr}
.contact .sep{width:3px;height:56px;background:var(--red)}
.slogan{bottom:110px}
@keyframes fadeUp{from{opacity:0;transform:translateY(60px)}to{opacity:1;transform:none}}
@keyframes slideR{from{opacity:0;transform:translateX(120px)}to{opacity:1;transform:none}}
@keyframes pop{0%{opacity:0;transform:scale(.3)}70%{opacity:1;transform:scale(1.12)}100%{transform:scale(1)}}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-14px)}}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.04)}}
.hook{animation:fadeUp .6s both 0s}
.brand{animation:fadeUp .6s ease-out both .1s}
.head .k{animation:slideR .7s cubic-bezier(.2,.8,.2,1) both .4s}
.head .bb{animation:slideR .7s cubic-bezier(.2,.8,.2,1) both 1.0s}
.sub{animation:fadeUp .6s ease-out both 1.6s}
.line{animation:grow .6s ease-out both 2.0s}
.herobox{animation:pop .7s ease-out both 2.2s}
.ring .b1{animation:float 2.4s ease-in-out infinite 0s}.ring .b2{animation:float 2.4s ease-in-out infinite .8s}.ring .b3{animation:float 2.4s ease-in-out infinite 1.6s}
.ic:nth-child(1){animation:pop .5s ease-out both 3.0s}
.ic:nth-child(2){animation:pop .5s ease-out both 3.4s}
.ic:nth-child(3){animation:pop .5s ease-out both 3.8s}
.cta{animation:fadeUp .6s ease-out both 4.5s, pulse 1.2s ease-in-out 5.3s infinite}
.contact{animation:fadeUp .6s ease-out both 5.0s}
.slogan{animation:pop .6s ease-out both 5.6s}
'''
COVER_CSS='''
.brand{position:absolute;top:120px;left:0;right:0}
.brand img{width:300px}
.tag{position:absolute;top:470px;left:0;right:0;text-align:center}
.tag span{display:inline-block;background:var(--red);color:#fff;font-size:44px;font-weight:900;padding:6px 40px;border-radius:12px}
.big{position:absolute;top:580px;left:50px;right:50px;text-align:center;font-size:118px;font-weight:900;line-height:1.2;color:var(--gray)}
.big .r{color:var(--red)}
.herobox{position:absolute;top:960px;left:0;right:0;display:flex;justify-content:center}
.slogan{top:1500px}
.ph{position:absolute;top:1640px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:16px;font-size:54px;font-weight:900;direction:ltr}
'''
def reel_html(r):
    icons=''.join(f'<div class="ic"><div class="c">{ic(n,64)}</div><p>{t.replace("<br>"," ")}</p></div>' for n,t in r["icons"])
    body=f'''<div class="hook">{r["hook"]}</div><div class="stage">
<div class="brand"><img src="logo.png"><div class="t">للتكييف والمقاولات والصيانة</div><div class="y">منذ 2005</div></div>
<div class="head"><div class="k">{r["head"]}</div><div class="bb"><div>{r["b1"]}</div><div>{r["b2"]}</div></div></div>
<div class="sub">{r["small"]}</div><div class="line"></div>
<div class="herobox">{hero(r,0.95)}</div>
<div class="icons">{icons}</div>
<div class="cta">{SHIELD}<div class="tx"><div>{r["cta1"]}</div><div>{r["cta2"]}</div></div></div>
<div class="contact"><div class="i">{PHONE}39226646</div><div class="sep"></div><div class="i">{IG}@Jahiz.bh</div></div>
</div><div class="slogan"><span>ارتاح احنا نهتم 🤝</span></div>
<script>window.fit=()=>{{for(const el of document.querySelectorAll('.head .k,.head .bb div')){{let s=parseFloat(getComputedStyle(el).fontSize);while(el.scrollWidth>(el.classList.contains('k')?660:630)&&s>30){{s-=2;el.style.fontSize=s+'px'}}}}}};</script>'''
    return BASE.replace('%CSS%',REEL_CSS).replace('%BODY%',body)
def cover_html(r):
    hook=r["hook"].rsplit(' ',1)[0] if r["hook"].split()[-1][0]>' ' and not r["hook"].split()[-1][0].isalpha() else r["hook"]
    body=f'''<div class="brand"><img src="logo.png"><div class="t">للتكييف والمقاولات والصيانة</div><div class="y">منذ 2005</div></div>
<div class="tag"><span>{r["tag"]}</span></div>
<div class="big">{r["b1"].rstrip('…')}<br><span class="r">{r["b2"]}</span></div>
<div class="herobox">{hero(r,1.0)}</div>
<div class="slogan"><span>ارتاح احنا نهتم 🤝</span></div>
<div class="ph">{PHONE}39226646</div>
<script>window.fit=()=>{{const el=document.querySelector('.big');let s=118;while(el.scrollHeight>380&&s>60){{s-=4;el.style.fontSize=s+'px'}}}};</script>'''
    return BASE.replace('%CSS%',COVER_CSS).replace('%BODY%',body)
data=json.load(open('reels.json'))
os.makedirs('out',exist_ok=True)
for r in data:
    open(f'out/{r["slug"]}.html','w').write(reel_html(r))
    open(f'out/{r["slug"]}-cover.html','w').write(cover_html(r))
print(len(data))
