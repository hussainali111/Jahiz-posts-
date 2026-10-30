from engine import *
import engine, sys
DUR=10.0; SIG=8.4
m=lambda n:440*2**((n-69)/12)
def piano(f,n):
    t=np.arange(n)/SR
    x=sum(np.sin(2*np.pi*f*k*t)*np.exp(-t*(1.5+k*1.2))/k**1.3 for k in range(1,7))
    return x*np.minimum(1,t/.003)
def pluck(f,n): return lowpass(osc(f,n,'saw',.01,3),3500)*env(n,.002,.12)
def shaker():
    n=int(.08*SR); t=np.arange(n)/SR
    return highpass(rng.standard_normal(n),6000)*np.sin(np.pi*t/.08)**2
def song(path,bpm=118):
    T=Track(DUR); b=60/bpm
    ch=[[57,60,64,69],[53,57,60,65],[48,52,55,60],[55,59,62,67]]; roots=[45,41,48,43]
    hook=[76,None,74,76,79,None,76,74, 72,None,74,76,74,72,69,None,
          76,None,74,76,79,81,79,76, 74,None,72,74,76,None,None,None]
    for i in range(int(SIG/b)):
        t=i*b; k=(i//4)%4
        if i%2==0: T.add('drums',t,kick(.25,.6)*.35)       # soft kick on 1 & 3 only
        if i%2==1 and i>=4:                                  # light snap
            n=int(.1*SR); T.add('drums',t,highpass(rng.standard_normal(n),2500)*env(n,.001,.03)*.12)
        for j in range(2): T.add('perc',t+j*b/2+b/4,shaker()*.10,pan=.4)
        if i%4==0:
            n=int(4*b*SR)
            for f in ch[k]: T.add('pad',t,lowpass(osc(m(f),n,'saw',.012,5),2200)*env(n,.15,4,.7,.3)*.08)
            T.add('bass',t,lowpass(osc(m(roots[k]-12),n,'tri'),400)*env(n,.02,3,.6,.2)*.45)
        # piano chords on beat, bright
        n=int(b*1.2*SR)
        for f in ch[k][1:]: T.add('lead',t,piano(m(f+12),n)*.10,pan=-.15)
    # main melody: pluck + soft bell doubling
    for q,note in enumerate(hook):
        t=q*b/2
        if t>SIG-.2: break
        if note is None: continue
        n=int(b*.9*SR)
        T.add('lead',t,pluck(m(note),n)*.22,pan=.15)
        T.add('lead',t,osc(m(note+12),n,'sin')*env(n,.002,.25)*.07)
    T.add('fx',SIG-1.0,riser(1.0)*.3)
    # gentler signature
    engine.kick_bak=engine.kick
    for i,f in enumerate([440,554.37,659.25]):
        n=int(1.1*SR); T.add('lead',SIG+.11*i,pluck(f,n)*.35+osc(f*2,n,'sin')*env(n,.002,.4)*.1,pan=-.3+.3*i)
    for f in [880,1318.5,1760]:
        n=int(1.6*SR); T.add('lead',SIG+.33,osc(f,n,'sin')*env(n,.002,.55)*.16)
    for f in [110,220,277.18,329.63,440]:
        n=int(1.6*SR); T.add('pad',SIG+.33,lowpass(osc(f,n,'saw',.01,4),2500)*env(n,.02,.7)*.10)
    T.add('drums',SIG,kick(.4,.7)*.45)
    mixdown(T,path)
song(sys.argv[1])
