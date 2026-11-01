"""Tank-cleaning price-tier reel: 1 / 2 / 3 tanks with big prices.
Usage: python3 tanks.py P1 P2 P3 [slug]"""
import sys
sys.argv_saved = sys.argv[:]
sys.argv = [sys.argv[0], '/dev/null']
import io, contextlib, json
_orig_load = json.load
json.load = lambda f: []
with contextlib.redirect_stdout(io.StringIO()):
    import build as B
json.load = _orig_load
sys.argv = sys.argv_saved

P = sys.argv[1:4] if len(sys.argv) >= 4 else ['XX', 'XX', 'XX']
SLUG = sys.argv[4] if len(sys.argv) > 4 else 'tanks-prices'
VAT = sys.argv[5] if len(sys.argv) > 5 else 'شامل الضريبة'

COLORS = [('#29B6F6', '#0277BD')] * 3

def tank(i, c, w=96):
    a, b = c
    gid = f'g{i}{w}'
    return f'''<svg width="{w}" height="{int(w*1.35)}" viewBox="0 0 100 135">
<defs><linearGradient id="{gid}" x1="0" x2="1"><stop offset="0" stop-color="{b}"/><stop offset=".35" stop-color="{a}"/><stop offset=".6" stop-color="#E3F6FF"/><stop offset="1" stop-color="{b}"/></linearGradient></defs>
<ellipse cx="50" cy="128" rx="44" ry="6" fill="rgba(0,0,0,.12)"/>
<path d="M10 28 Q10 18 50 18 Q90 18 90 28 L90 118 Q90 128 50 128 Q10 128 10 118 Z" fill="url(#{gid})"/>
<ellipse cx="50" cy="26" rx="40" ry="9" fill="{a}" stroke="{b}" stroke-width="2"/>
<rect x="38" y="8" width="24" height="14" rx="4" fill="{b}"/>
<path d="M10 55 Q50 65 90 55 M10 85 Q50 95 90 85" stroke="{b}" stroke-width="3" fill="none" opacity=".55"/>
<path d="M50 72 l7 9 a9 9 0 1 1 -14 0z" fill="#fff" opacity=".9"/>
</svg>'''

def tanks_row(n, w=96):
    c = COLORS[n - 1]
    return ''.join(f'<span class="tk" style="--d:{k}">{tank(n*10+k, c, w)}</span>' for k in range(n))

FIT = "<script>window.fit=()=>{for(const p of document.querySelectorAll('.tier .pr')){const n=p.querySelector('.n');let s=110;while(p.scrollWidth>p.clientWidth&&s>50){s-=4;n.style.fontSize=s+'px'}}};</script>"
LABELS = ['خزان واحد', 'خزانين', '٣ خزانات']

def tier(n, p, w):
    return f'''<div class="tier t{n}"><div class="tks">{tanks_row(n, w)}</div>
<div class="lb">{LABELS[n-1]}</div>
<div class="pr"><div class="n">{p}</div><div class="cur">د.ب</div></div></div>'''

CSS_COMMON = '''
.tier{position:absolute;left:50px;right:50px;height:230px;background:#fff;border:4px solid var(--red);border-radius:30px;display:flex;align-items:center;padding:0 30px;box-shadow:0 12px 28px rgba(0,0,0,.08)}
.tier .tks{flex:0 0 300px;display:flex;justify-content:center;align-items:flex-end;gap:6px}
.tier .lb{flex:1;min-width:0;font-size:58px;font-weight:900;color:var(--gray);text-align:center;white-space:nowrap}
.tier .pr{flex:none;width:330px;min-width:0;overflow:hidden;padding:0 14px;height:190px;border-radius:24px;background:var(--red);color:#fff;display:flex;align-items:center;justify-content:center;gap:10px;direction:ltr;box-shadow:0 10px 24px rgba(213,17,21,.4)}
.tier .pr .n{font-size:110px;white-space:nowrap;font-weight:900;line-height:1}
.tier .pr .cur{font-size:36px;font-weight:900;margin-top:36px}
.vat{position:absolute;left:0;right:0;text-align:center;font-size:34px;font-weight:800;color:var(--red)}
'''

REEL_CSS = CSS_COMMON + '''
.hook{position:absolute;top:95px;left:40px;right:40px;text-align:center;font-size:58px;font-weight:900}
.brand{position:absolute;top:220px;left:50px;width:300px}
.head{position:absolute;top:230px;right:60px;width:640px;text-align:right}
.head .k{font-size:80px;font-weight:900;color:var(--red);line-height:1.15;white-space:nowrap}
.head .s{font-size:46px;font-weight:900;border-right:6px solid var(--red);padding-right:22px;margin-top:8px}
.nw{position:absolute;top:478px;left:50px;right:50px;text-align:center;background:var(--gray);color:#fff;font-size:56px;font-weight:900;border-radius:20px;padding:6px 0;white-space:nowrap}
.nw b{color:#FF4D50}
.nw{animation:pop .6s ease-out both 1.1s}
.t1{top:590px}.t2{top:840px}.t3{top:1090px}
.vat{top:1328px}
.sanad{position:absolute;top:1360px;left:40px;height:250px;filter:drop-shadow(0 10px 12px rgba(0,0,0,.25))}
.cta{position:absolute;top:1385px;left:300px;right:50px;border:3px solid var(--red);border-radius:18px;background:#fff;padding:16px 30px;text-align:center}
.cta div:first-child{font-size:40px;font-weight:900}.cta div:last-child{font-size:40px;font-weight:900;color:var(--red)}
.contact{position:absolute;top:1575px;left:60px;right:60px;border-top:2px solid #ddd;padding-top:22px;display:flex;justify-content:center;align-items:center;gap:50px}
.contact .i{display:flex;align-items:center;gap:16px;font-size:46px;font-weight:800;direction:ltr}
.contact .sep{width:3px;height:56px;background:var(--red)}
.slogan{bottom:110px}
@keyframes fadeUp{from{opacity:0;transform:translateY(60px)}to{opacity:1;transform:none}}
@keyframes slideR{from{opacity:0;transform:translateX(120px)}to{opacity:1;transform:none}}
@keyframes slideL{from{opacity:0;transform:translateX(-200px)}to{opacity:1;transform:none}}
@keyframes pop{0%{opacity:0;transform:scale(.3)}70%{opacity:1;transform:scale(1.12)}100%{transform:scale(1)}}
@keyframes drop{0%{opacity:0;transform:translateY(-90px)}70%{opacity:1;transform:translateY(8px)}100%{transform:none}}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.05)}}
@keyframes sanadIn{0%{opacity:0;transform:translateY(120px) scale(.6)}60%{opacity:1;transform:translateY(-18px) scale(1.06)}100%{transform:none}}
@keyframes sway{0%,100%{transform:rotate(0)}25%{transform:rotate(-4deg)}75%{transform:rotate(4deg)}}
.hook{animation:fadeUp .6s both 0s}.brand{animation:fadeUp .6s both .1s}
.head .k{animation:slideR .7s cubic-bezier(.2,.8,.2,1) both .4s}.head .s{animation:slideR .7s cubic-bezier(.2,.8,.2,1) both .9s}
.t1{animation:slideL .6s cubic-bezier(.2,.8,.2,1) both 1.4s}.t2{animation:slideL .6s cubic-bezier(.2,.8,.2,1) both 2.3s}.t3{animation:slideL .6s cubic-bezier(.2,.8,.2,1) both 3.2s}
.t1 .tk{animation:drop .5s ease-out both calc(1.8s + var(--d)*.15s)}.t2 .tk{animation:drop .5s ease-out both calc(2.7s + var(--d)*.15s)}.t3 .tk{animation:drop .5s ease-out both calc(3.6s + var(--d)*.15s)}
.tk{display:inline-block}
.t1 .pr{animation:pop .5s ease-out both 1.9s, pulse 1.2s ease-in-out 2.5s infinite}
.t2 .pr{animation:pop .5s ease-out both 2.8s, pulse 1.2s ease-in-out 3.4s infinite}
.t3 .pr{animation:pop .5s ease-out both 3.7s, pulse 1.2s ease-in-out 4.3s infinite}
.vat{animation:fadeUp .5s both 4.2s}
.sanad{transform-origin:50% 100%;animation:sanadIn .7s cubic-bezier(.2,.8,.2,1) both 4.6s, sway 1.6s ease-in-out 5.4s infinite}
.cta{animation:fadeUp .6s both 4.8s}.contact{animation:fadeUp .6s both 5.2s}
.slogan.sw{animation:fadeUp .3s ease-out both 7.45s}
.slogan b{display:inline-block;font-weight:900}
.slogan .w1{animation:pop .35s ease-out both 7.6s}.slogan .w2{animation:pop .35s ease-out both 8.3s}.slogan .w3{animation:pop .35s ease-out both 8.85s}.slogan .w4{animation:pop .4s ease-out both 9.0s}
'''

COVER_CSS = CSS_COMMON + '''
.brand{position:absolute;top:90px;left:0;right:0}.brand img{width:260px}
.tag{position:absolute;top:400px;left:0;right:0;text-align:center}
.tag span{display:inline-block;background:var(--red);color:#fff;font-size:44px;font-weight:900;padding:6px 40px;border-radius:12px}
.big{position:absolute;top:500px;left:30px;right:30px;text-align:center;white-space:nowrap;font-size:72px;font-weight:900;line-height:1.15}
.big .r{color:var(--red)}
.t1{top:660px}.t2{top:920px}.t3{top:1180px}
.vat{top:1430px}
.slogan{top:1530px}
.ph{position:absolute;top:1690px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:16px;font-size:54px;font-weight:900;direction:ltr}
'''

def reel():
    body = f'''<div class="hook">متى آخر مرة نظّفت خزانك؟ 💧</div>
<div class="brand"><img src="logo.png"><div class="t">للتكييف والمقاولات والصيانة</div><div class="y">منذ 2005</div></div>
<div class="head"><div class="k">تنظيف الخزانات</div><div class="s">تنظيف + تعقيم كامل</div></div>
<div class="nw">🚫 <b>بدون دخول العمال</b> في الخزان</div>
{tier(1,P[0],90)}{tier(2,P[1],90)}{tier(3,P[2],90)}
<div class="vat">الأسعار {VAT}</div>
<img class="sanad" src="sanad.png">
<div class="cta"><div>نظّف خزانك كل 6 شهور</div><div>احجز موعدك الحين!</div></div>
<div class="contact"><div class="i">{B.PHONE}39226646</div><div class="sep"></div><div class="i">{B.IG}@Jahiz.bh</div></div>
%FIT%<div class="slogan sw"><span><b class="w1">ارتاح</b> <b class="w2">احنا</b> <b class="w3">نهتم</b> <b class="w4">🤝</b></span></div>'''
    return B.BASE.replace('%CSS%', REEL_CSS).replace('%BODY%', body.replace('%FIT%', FIT))

def cover():
    body = f'''<div class="brand"><img src="logo.png"><div class="t">للتكييف والمقاولات والصيانة</div><div class="y">منذ 2005</div></div>
<div class="tag"><span>تنظيف وتعقيم الخزانات</span></div>
<div class="big"><span class="r">بدون دخول</span> العمال في الخزان</div>
{tier(1,P[0],90)}{tier(2,P[1],90)}{tier(3,P[2],90)}
<div class="vat">الأسعار {VAT}</div>
<div class="slogan"><span>ارتاح احنا نهتم 🤝</span></div>
<div class="ph">{B.PHONE}39226646</div>%FIT%'''
    return B.BASE.replace('%CSS%', COVER_CSS).replace('%BODY%', body.replace('%FIT%', FIT))

open(f'out/{SLUG}.html', 'w').write(reel())
open(f'out/{SLUG}-cover.html', 'w').write(cover())
print(SLUG)
