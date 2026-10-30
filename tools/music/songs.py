from engine import *
import sys
DUR=10.0; SIG=8.4
def modern(path):
    T=Track(DUR); bpm=124; b=60/bpm
    ch=[[57,60,64],[53,57,60],[48,52,55,60],[55,59,62]]; roots=[45,41,48,43]
    m=lambda n:440*2**((n-69)/12)
    for i in range(int(SIG/b)):
        t=i*b; k=(i//4)%4
        T.add('drums',t,kick()*.95)
        if i%2: T.add('drums',t,clap()*.7)
        for j in range(4): T.add('drums',t+j*b/4,hat(j==2)*(.22 if j==2 else .12),pan=.3)
        n=int(b/2*SR)
        for j in (0,1): T.add('bass',t+j*b/2,lowpass(osc(m(roots[k]),n,'saw',.01,2),900)*env(n,.003,.15,.3,.02)*.5)
        if i%4==0:
            n=int(4*b*SR)
            for f in ch[k]: T.add('pad',t,lowpass(osc(m(f+12),n,'saw',.012,5),3000)*env(n,.05,4,.6,.2)*.13)
        for j in range(4):
            f=m(ch[k][(i*4+j)%len(ch[k])]+24); n=int(.18*SR)
            T.add('lead',t+j*b/4,lowpass(osc(f,n,'sq'),4000)*env(n,.002,.06)*.12,pan=(-.4 if j%2 else .4))
    T.add('fx',SIG-1.6,riser(1.6)*.6)
    signature(T,SIG); mixdown(T,path,SIG,b)
def khaleeji(path):
    T=Track(DUR); bpm=104; b=60/bpm
    m=lambda n:440*2**((n-69)/12)
    # D hijaz: D Eb F# G A Bb C
    sc=[62,63,66,67,69,70,72,74]
    mel=[0,1,2,3,4,3,2,1, 2,3,4,5,4,3,2,0, 4,5,6,7,6,5,4,3, 2,1,2,3,2,1,0,0]
    for i in range(int(SIG/b)):
        t=i*b
        # khaleeji-ish groove: dum . tak dum | tak . tak .
        pat=[('d',0),('t',.5),('d',.75)] if i%2==0 else [('t',0),('t',.5),('t',.75)]
        for kind,o in pat: T.add('perc',t+o*b,(dum()*.9 if kind=='d' else tak()*.55),pan=(-.2 if kind=='t' else 0))
        if i%2==1: T.add('perc',t+.5*b,clap()*.6,pan=.25); T.add('perc',t+.53*b,clap()*.45,pan=-.25)
        T.add('drums',t,kick(.3,.8)*.55)
        for j in range(2): T.add('drums',t+j*b/2+b/4,hat()*.10,pan=.4)
        n=int(b*SR); T.add('bass',t,lowpass(osc(m(38 if (i//4)%2==0 else 43),n,'tri'),600)*env(n,.005,.3,.4)*.55)
    for q,deg in enumerate(mel):
        t=q*b/2
        if t>SIG-.3: break
        T.add('lead',t,ks(m(sc[deg]),.6,.45)*.55,pan=-.15)
        if q%4==0: T.add('lead',t,ks(m(sc[deg]-12),.8,.3)*.35,pan=.2)
    n=int(SIG*SR); T.add('pad',0,lowpass(osc(m(50),n,'saw',.01,4)+osc(m(57),n,'saw',.01,4),1200)*env(n,1.0,30,1,.5)*.06)
    T.add('fx',SIG-1.4,riser(1.4)*.5)
    signature(T,SIG); mixdown(T,path)
def cinematic(path):
    T=Track(DUR); bpm=90; b=60/bpm
    m=lambda n:440*2**((n-69)/12)
    ch=[[45,57,60,64],[41,53,57,60],[48,55,60,64],[43,55,59,62]]
    for k in range(4):
        t=k*2*b*1.0
        if t>SIG: break
        n=int(2*b*SR)+int(.5*SR)
        for f in ch[k]: T.add('pad',t,lowpass(osc(m(f),n,'saw',.015,6),1800+600*k)*env(n,.25,6,.8,.3)*.11)
    # ostinato strings 8ths
    seq=[69,72,76,72]
    for i in range(int(SIG/(b/2))):
        t=i*b/2; f=m(seq[i%4]-(0 if t<4 else -2)); n=int(.22*SR)
        T.add('lead',t,lowpass(osc(f,n,'saw',.01,3),3500)*env(n,.01,.12)*.13,pan=(.3 if i%2 else -.3))
    # taiko-ish hits
    for i in range(int(SIG/b)):
        t=i*b
        if i%4 in (0,3): T.add('drums',t,kick(.6,1.2)*.9)
        if i%4==2: T.add('perc',t,dum()*.9)
        if i>=8: T.add('perc',t+b/2,tak()*.4)
    T.add('fx',SIG-2.0,riser(2.0)*.7)
    signature(T,SIG); mixdown(T,path)
{'modern':modern,'khaleeji':khaleeji,'cinematic':cinematic}[sys.argv[1]](sys.argv[2])
