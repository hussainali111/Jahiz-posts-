from engine import *
import sys
DUR=10.0; SIG=8.4
m=lambda n:440*2**((n-69)/12)
def vox(f,n,vowel='a'):
    # vocal-chop-ish: saw through two formant bandpasses (approx via lowpass/highpass mix)
    x=osc(f,n,'saw',.006,3)
    F={'a':(800,1150),'o':(500,900),'e':(400,2000)}[vowel]
    y=highpass(lowpass(x,F[0]*1.4),F[0]*.6)+.6*highpass(lowpass(x,F[1]*1.3),F[1]*.7)
    return y
def song(path,bpm=128):
    T=Track(DUR); b=60/bpm
    ch=[[57,60,64],[53,57,60],[48,52,55],[55,59,62]]; roots=[45,41,48,43]
    # catchy hook (8th notes, 2 bars) in A minor
    hook=[76,None,74,76,None,79,76,74, 72,None,72,74,None,76,72,69,
          76,None,74,76,None,79,81,79, 76,None,74,72,None,74,76,None]
    intro=2*b*2   # 1 bar intro (filtered), then drop
    nb=int(SIG/b)
    for i in range(nb):
        t=i*b; k=(i//4)%4; drop=t>=intro-1e-6
        if drop or i%2==0: T.add('drums',t,kick(.3,1.2)*(1.0 if drop else .6))
        if drop and i%2==1:
            T.add('drums',t,clap()*.8); n=int(.2*SR)
            T.add('drums',t,highpass(rng.standard_normal(n),1500)*env(n,.001,.06)*.35)
        for j in range(4):
            if drop or j%2: T.add('drums',t+j*b/4,hat(j==2)*(.2 if j==2 else .1),pan=(.35 if j%2 else -.2))
        # rolling bass 16ths w/ octave jump
        if drop:
            for j in range(4):
                n=int(b/4*SR*.9); f=m(roots[k]+(12 if j==3 else 0))
                T.add('bass',t+j*b/4,lowpass(osc(f,n,'saw',.012,3),700+300*(j==3))*env(n,.002,.08,.4,.01)*.55)
            n=int(b*SR); T.add('bass',t,osc(m(roots[k]-12),n,'sin')*env(n,.005,.25,.5,.02)*.5)
        # chord stabs (offbeats), wide
        n=int(b*.35*SR)
        for f in ch[k]:
            sig=lowpass(osc(m(f+12),n,'saw',.02,6),5000 if drop else 1200)*env(n,.003,.12)*.10
            T.add('pad',t+b/2,sig,pan=-.5); T.add('pad',t+b/2+.008,sig,pan=.5)
    # hook melody (vox chop + pluck) after drop
    for q,note in enumerate(hook*2):
        t=intro+q*b/2
        if t>SIG-.2: break
        if note is None: continue
        n=int(b/2*SR*.95)
        T.add('lead',t,vox(m(note),n,'a' if q%4<2 else 'o')*env(n,.004,.18,.3,.03)*.22,pan=.1)
        T.add('lead',t,lowpass(osc(m(note+12),n,'sq'),5000)*env(n,.002,.07)*.06,pan=-.2)
    # intro riser + uplifter into drop + downlifter
    T.add('fx',0,riser(intro)*.45)
    T.add('fx',intro,lowpass(rng.standard_normal(int(.8*SR)),5000)*np.exp(-np.arange(int(.8*SR))/SR/.25)*.3)
    T.add('fx',SIG-1.2,riser(1.2)*.55)
    signature(T,SIG); mixdown(T,path,SIG,b)
song(sys.argv[1])
