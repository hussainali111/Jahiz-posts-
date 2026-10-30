import numpy as np, wave, sys
sr=44100; dur=10.0; bpm=124; beat=60/bpm
N=int(sr*dur); t=np.arange(N)/sr; out=np.zeros(N)
rng=np.random.default_rng(7)
def add(st,sig):
    st=int(st); n=min(len(sig),N-st)
    if n>0 and st>=0: out[st:st+n]+=sig[:n]
def tone(f,d,a=0.005,r=0.2,kind='saw'):
    n=int(d*sr); tt=np.arange(n)/sr
    if kind=='saw': w=sum(np.sin(2*np.pi*f*k*tt)/k for k in range(1,8))
    elif kind=='sq': w=sum(np.sin(2*np.pi*f*k*tt)/k for k in range(1,8,2))
    else: w=np.sin(2*np.pi*f*tt)
    e=np.minimum(1,tt/a)*np.exp(-tt/r); return w*e
chords=[[220,261.63,329.63],[174.61,220,261.63],[261.63,329.63,392],[196,246.94,293.66]]
roots=[110,87.31,130.81,98]
bar=4*beat; body_end=8.4  # music body, then signature
nbeats=int(body_end/beat)
for b in range(nbeats):
    s=b*beat*sr; k=(b//4)%4
    # kick every beat
    m=int(.25*sr); tm=np.arange(m)/sr; f=45+110*np.exp(-tm/.025)
    add(s,0.75*np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-tm/.11))
    # clap on 2 and 4
    if b%2==1:
        m=int(.18*sr); n=rng.standard_normal(m); tm=np.arange(m)/sr
        add(s,0.28*n*np.exp(-tm/.05))
    # 16th hats
    for j in range(4):
        m=int(.04*sr); add(s+j*beat/4*sr,(0.07 if j%2 else 0.04)*rng.standard_normal(m)*np.exp(-np.arange(m)/(.01*sr)))
    # driving 8th bass
    for j in range(2):
        add(s+j*beat/2*sr,0.22*tone(roots[k],beat/2*0.9,r=.12,kind='sq'))
    # stab chords on offbeat
    for f0 in chords[k]:
        add(s+beat/2*sr,0.035*tone(f0*2,beat*0.4,r=.08))
    # arp 16ths
    for j in range(4):
        f0=chords[k][(b*4+j)%3]*4
        add(s+j*beat/4*sr,0.05*tone(f0,.12,r=.05,kind='sin'))
# riser before signature
rs=int((body_end-1.6)*sr); rn=int(1.6*sr); tm=np.arange(rn)/sr
add(rs,0.12*rng.standard_normal(rn)*(tm/1.6)**2)
add(rs,0.08*np.sin(2*np.pi*np.cumsum(300+900*(tm/1.6)**2)/sr)*(tm/1.6))
# SIGNATURE: "جا-هز" two-note hit + bright 3-note motif + bell
sig=body_end
m=int(.5*sr); tm=np.arange(m)/sr; f=40+120*np.exp(-tm/.03)
add(sig*sr,1.0*np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-tm/.25))       # impact
for i,f0 in enumerate([440,554.37,659.25]):                            # A C# E ascending
    add((sig+0.12*i)*sr,0.16*tone(f0,0.9,r=.35,kind='saw'))
for f0 in [880,1318.5]:                                                 # bell
    add((sig+0.36)*sr,0.12*tone(f0,1.2,r=.5,kind='sin'))
for f0 in [220,277.18,329.63,440]:                                      # final chord pad
    add((sig+0.36)*sr,0.05*tone(f0,1.2,a=.02,r=.6,kind='saw'))
fo=int(.25*sr); out[-fo:]*=np.linspace(1,0,fo)
out=np.tanh(out*1.3); out=out/np.max(np.abs(out))*0.85
w=wave.open(sys.argv[1],'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
