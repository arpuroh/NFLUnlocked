import os
import numpy as np, soundfile as sf, subprocess, json
sr=44100
subprocess.run(['ffmpeg','-v','error','-y','-i','voice.wav','-ar',str(sr),'-ac','1','voice44.wav'],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-i',os.environ.get('MUSIC','music.mp3'),'-ar',str(sr),'-ac','2','music44.wav'],check=True)
v,_=sf.read('voice44.wav'); m,_=sf.read('music44.wav')
N=len(v)+int(0.6*sr)
# loop the music bed with a short crossfade
xf=int(0.05*sr); out=m.copy()
while len(out)<N:
    a=out[-xf:]*np.linspace(1,0,xf)[:,None]+m[:xf]*np.linspace(0,1,xf)[:,None]
    out=np.concatenate([out[:-xf],a,m[xf:]])
m=out[:N]
v=np.pad(v,(0,N-len(v)))
# voice: normalise to -1 dBFS peak-ish, gentle compression
v=v/np.max(np.abs(v))*0.85
v=np.sign(v)*np.abs(v)**0.85*0.9
# duck envelope from voice RMS
hop=int(0.02*sr); rms=np.array([np.sqrt(np.mean(v[i:i+hop]**2)) for i in range(0,N,hop)])
act=(rms>0.02).astype(float)
# hold + smooth
from numpy.lib.stride_tricks import sliding_window_view
hold=np.convolve(act,np.ones(12),'same')>0
g=np.where(hold,0.16,0.38)
sm=np.convolve(g,np.ones(8)/8,'same')
env=np.interp(np.arange(N),np.arange(len(sm))*hop,sm)
mm=m/np.max(np.abs(m))
mix=mm*env[:,None]+v[:,None]*np.array([1,1])
fade=int(1.5*sr); mix[-fade:]*=np.linspace(1,0,fade)[:,None]
mix[:int(0.02*sr)]*=np.linspace(0,1,int(0.02*sr))[:,None]
mix/=np.max(np.abs(mix))*1.05
sf.write('mix.wav',mix,sr)
print(N/sr)
