from engine import *
import sys
DUR=10.0; SIG=7.6
m=lambda n:440*2**((n-69)/12)
def piano(f,n):
    t=np.arange(n)/SR
    return sum(np.sin(2*np.pi*f*k*t)*np.exp(-t*(1.2+k*1.1))/k**1.4 for k in range(1,7))*np.minimum(1,t/.003)
def strings(f,n):
    x=lowpass(osc(f,n,'saw',.014,6),2600)
    t=np.arange(n)/SR; vib=1+.003*np.sin(2*np.pi*5.2*t)
    return x*env(n,.35,8,.85,.4)
def frame():
    n=int(.3*SR); t=np.arange(n)/SR; f=110+40*np.exp(-t/.02)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t/.12)*.7+lowpass(rng.standard_normal(n),1200)*np.exp(-t/.02)*.2
def song(path,bpm=118):
    T=Track(DUR); b=60/bpm
    # D major, warm progression: D - Bm - G - A
    ch=[[62,66,69],[59,62,66],[55,59,62],[57,61,64]]; roots=[50,47,43,45]
    # gentle, singable melody (oud-like pluck), ornament grace notes
    mel=[(0,74),(1,76),(1.5,78),(2,76),(3,74),
         (4,71),(5,74),(5.5,76),(6,74),(7,71),
         (8,67),(9,71),(9.5,74),(10,76),(11,78),
         (12,76),(13,74),(13.5,73),(14,74),(15,None)]
    for i in range(int(SIG/b)):
        t=i*b; k=(i//4)%4
        if i%4==0:
            n=int(4*b*SR)+int(.4*SR)
            for f in ch[k]: T.add('pad',t,strings(m(f),n)*.09,pan=(-.4 if f==ch[k][0] else .4))
            T.add('bass',t,lowpass(osc(m(roots[k]-12),n,'tri'),350)*env(n,.03,3,.6,.3)*.45)
        # piano broken chord 8ths
        for j in range(2):
            f=m(ch[k][(i*2+j)%3]+12); n=int(b*1.4*SR)
            T.add('lead',t+j*b/2,piano(f,n)*.09,pan=-.2)
        # very light frame drum + finger snap
        if i%2==0: T.add('perc',t,frame()*.35)
        for j in range(4):
            n=int(.05*SR); T.add('perc',t+j*b/4,highpass(rng.standard_normal(n),6500)*np.exp(-np.arange(n)/(.012*SR))*(.07 if j%2 else .04),pan=.35)
        if i%2==1:
            n=int(.08*SR); T.add('perc',t,highpass(rng.standard_normal(n),3000)*env(n,.001,.02)*.12,pan=.3)
    for beat,note in mel:
        t=beat*b
        if note is None or t>SIG-.3: continue
        T.add('lead',t,ks(m(note),.9,.5,.997)*.42,pan=.15)            # oud-like
        T.add('lead',t,osc(m(note+12),int(.6*SR),'sin')*env(int(.6*SR),.003,.3)*.06)  # bell shimmer
        if beat%2==0 and t>.2:                                      # grace note ornament
            T.add('lead',t-.06,ks(m(note+2),.15,.5,.99)*.18,pan=.15)
    T.add('fx',SIG-.8,riser(.8)*.15)
    # SONIC LOGO: "ار-تاح · اح-نا · نه-تم"  (syllable rhythm, D major)
    syl=[(0.00,69,.18),(0.18,74,.45),(0.70,78,.16),(0.86,76,.30),(1.25,73,.16),(1.41,74,1.0)]
    for o,n_,d in syl:
        t=SIG+o; f=m(n_)
        T.add('lead',t,ks(f,d+.5,.6,.997)*.55,pan=0)
        n=int((d+.4)*SR); T.add('lead',t,osc(f*2,n,'sin')*env(n,.002,.35)*.10)
        n=int((d+.3)*SR); T.add('lead',t,piano(f,n)*.18)
    # chords under each word: D | Bm->A | D (resolve)
    for o,chd,d in [(0.0,[62,66,69],.7),(0.70,[59,62,66],.55),(1.25,[57,61,64],.16),(1.41,[50,62,66,69,74],1.0)]:
        n=int((d+.6)*SR)
        for f in chd: T.add('pad',SIG+o,strings(m(f),n)*.09)
    for f in [m(86),m(90),m(93)]:
        n=int(1.3*SR); T.add('lead',SIG+1.41,osc(f,n,'sin')*env(n,.002,.6)*.10)
    T.add('perc',SIG+1.41,frame()*.45)
    mixdown(T,path)
song(sys.argv[1])
