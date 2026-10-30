import numpy as np, wave
SR=44100
rng=np.random.default_rng(11)
class Track:
    def __init__(s,dur): s.N=int(SR*dur); s.bus={}
    def add(s,bus,t0,sig,pan=0.0):
        if bus not in s.bus: s.bus[bus]=np.zeros((s.N,2))
        st=int(t0*SR); n=min(len(sig),s.N-st)
        if n<=0 or st<0: return
        l=np.cos((pan+1)*np.pi/4); r=np.sin((pan+1)*np.pi/4)
        s.bus[bus][st:st+n,0]+=sig[:n]*l*1.41; s.bus[bus][st:st+n,1]+=sig[:n]*r*1.41
def env(n,a=.005,d=.2,sus=0.0,rel=.05):
    t=np.arange(n)/SR; e=np.minimum(1,t/max(a,1e-4))
    dec=sus+(1-sus)*np.exp(-t/d); e=e*dec
    rl=int(rel*SR)
    if rl>0 and rl<n: e[-rl:]*=np.linspace(1,0,rl)
    return e
def osc(f,n,kind='saw',detune=0,voices=1):
    t=np.arange(n)/SR; out=np.zeros(n)
    for v in range(voices):
        ff=f*(1+detune*(v-(voices-1)/2)/max(voices-1,1)) if voices>1 else f
        ph=rng.random()*2*np.pi
        if kind=='saw': out+=2*((ff*t+ph/6.283)%1)-1
        elif kind=='sq': out+=np.sign(np.sin(2*np.pi*ff*t+ph))
        elif kind=='tri': out+=2*np.abs(2*((ff*t+ph/6.283)%1)-1)-1
        else: out+=np.sin(2*np.pi*ff*t+ph)
    return out/voices
def lowpass(x,fc):
    X=np.fft.rfft(x,axis=0); f=np.fft.rfftfreq(len(x),1/SR)
    H=1/np.sqrt(1+(f/fc)**4)
    return np.fft.irfft(X*(H if x.ndim==1 else H[:,None]),n=len(x),axis=0)
def highpass(x,fc):
    X=np.fft.rfft(x,axis=0); f=np.fft.rfftfreq(len(x),1/SR)
    H=1/np.sqrt(1+(fc/np.maximum(f,1))**4)
    return np.fft.irfft(X*(H if x.ndim==1 else H[:,None]),n=len(x),axis=0)
def reverb(x,decay=1.6,mix=.25):
    n=int(decay*SR); t=np.arange(n)/SR
    out=np.zeros_like(x)
    for c in range(2):
        ir=rng.standard_normal(n)*np.exp(-t*6.9/decay); ir[:int(.01*SR)]=0
        ir=lowpass(ir,6000); ir/=np.sqrt(np.sum(ir**2))
        L=len(x)+n; F=1<<int(np.ceil(np.log2(L)))
        y=np.fft.irfft(np.fft.rfft(x[:,c],F)*np.fft.rfft(ir,F),F)[:len(x)]
        out[:,c]=y
    return x*(1-mix)+out*mix
def kick(len_=.35,punch=1.0):
    n=int(len_*SR); t=np.arange(n)/SR; f=42+140*np.exp(-t/.03)
    s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t/.16)
    click=rng.standard_normal(n)*np.exp(-t/.002)*.3
    return np.tanh((s+click)*1.5*punch)
def clap():
    n=int(.25*SR); t=np.arange(n)/SR; e=np.zeros(n)
    for d in (0,.008,.016,.024): e+=np.exp(-np.maximum(t-d,0)/.012)*(t>=d)
    e+=np.exp(-t/.09)*.6
    return highpass(rng.standard_normal(n),900)*e*.5
def hat(open_=False):
    n=int((.18 if open_ else .05)*SR); t=np.arange(n)/SR
    return highpass(rng.standard_normal(n),7000)*np.exp(-t/(.06 if open_ else .012))
def ks(f,dur,bright=.5,decay=.996):
    n=int(dur*SR); p=max(2,int(SR/f)); buf=rng.uniform(-1,1,p)
    buf=lowpass(buf,1500+bright*8000) if p>64 else buf
    out=np.zeros(n); i=0
    b=buf.copy()
    for k in range(n):
        out[k]=b[k%p]
        b[k%p]=decay*0.5*(b[k%p]+b[(k+1)%p])
    return out
def dum():
    n=int(.4*SR); t=np.arange(n)/SR; f=95+60*np.exp(-t/.02)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t/.15)+lowpass(rng.standard_normal(n),400)*np.exp(-t/.02)*.4
def tak():
    n=int(.15*SR); t=np.arange(n)/SR
    return (np.sin(2*np.pi*650*t)*np.exp(-t/.03)*.6+highpass(rng.standard_normal(n),2500)*np.exp(-t/.015)*.7)
def riser(dur):
    n=int(dur*SR); t=np.arange(n)/SR; x=t/dur
    return highpass(rng.standard_normal(n),800)*x**2*.5+np.sin(2*np.pi*np.cumsum(200+1400*x**2)/SR)*x*.2
def signature(T,t0):
    # shared Jahiz sign-off: impact + A C# E rise + bell
    T.add('drums',t0,kick(.7,1.4)*1.0)
    T.add('fx',t0,lowpass(rng.standard_normal(int(1.2*SR)),3000)*np.exp(-np.arange(int(1.2*SR))/SR/.35)*.35)
    for i,f in enumerate([440,554.37,659.25]):
        n=int(1.1*SR); T.add('lead',t0+.11*i,osc(f,n,'saw',.008,3)*env(n,.005,.35)*.32,pan=-.3+.3*i)
    for f in [880,1318.5,1760]:
        n=int(1.6*SR); T.add('lead',t0+.33,osc(f,n,'sin')*env(n,.002,.55)*.18)
    for f in [110,220,277.18,329.63,440]:
        n=int(1.6*SR); T.add('pad',t0+.33,lowpass(osc(f,n,'saw',.01,4),2500)*env(n,.02,.7)*.12)
def mixdown(T,path,sidechain_beats=None,beat=None,dur=10):
    out=np.zeros((T.N,2))
    gains={'drums':1.0,'bass':.9,'pad':.7,'lead':.8,'perc':.9,'fx':.7}
    for k,v in T.bus.items():
        x=v
        if k in('pad','bass','lead') and sidechain_beats is not None:
            t=np.arange(T.N)/SR; ph=(t%beat)/beat; duck=1-.6*np.exp(-ph*6); duck[t>=sidechain_beats]=1
            x=x*duck[:,None]
        if k in ('pad','lead','perc','fx'): x=reverb(x,1.8,.28)
        out+=x*gains.get(k,1)
    out=np.tanh(out*1.1)
    fo=int(.3*SR); out[-fo:]*=np.linspace(1,0,fo)[:,None]
    out/=np.max(np.abs(out)); out*=.89
    w=wave.open(path,'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
