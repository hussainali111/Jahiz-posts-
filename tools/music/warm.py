from engine import *
import sys
DUR=10.0; SIG=8.4
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
def song(path,bpm=100):
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
        if i%2==1:
            n=int(.08*SR); T.add('perc',t,highpass(rng.standard_normal(n),3000)*env(n,.001,.02)*.12,pan=.3)
    for beat,note in mel:
        t=beat*b
        if note is None or t>SIG-.3: continue
        T.add('lead',t,ks(m(note),.9,.5,.997)*.42,pan=.15)            # oud-like
        T.add('lead',t,osc(m(note+12),int(.6*SR),'sin')*env(int(.6*SR),.003,.3)*.06)  # bell shimmer
        if beat%2==0 and t>.2:                                      # grace note ornament
            T.add('lead',t-.06,ks(m(note+2),.15,.5,.99)*.18,pan=.15)
    T.add('fx',SIG-1.0,riser(1.0)*.2)
    # warm signature: D major sign-off (same 3-note rise shape as brand sting)
    for i,f in enumerate([m(74),m(78),m(81)]):
        T.add('lead',SIG+.12*i,ks(f,1.2,.6,.997)*.45,pan=-.3+.3*i)
    for f in [m(86),m(90),m(93)]:
        n=int(1.5*SR); T.add('lead',SIG+.36,osc(f,n,'sin')*env(n,.002,.6)*.12)
    for f in [m(50),m(62),m(66),m(69),m(74)]:
        n=int(1.6*SR); T.add('pad',SIG+.36,strings(f,n)*.10)
    T.add('perc',SIG,frame()*.5)
    mixdown(T,path)
song(sys.argv[1])
