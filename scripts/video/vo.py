import os
TTS=os.environ.get('KOKORO_DIR','/tmp/kokoro')+'/'
import json, soundfile as sf, numpy as np, sys
from kokoro_onnx import Kokoro
k=Kokoro(TTS+'kokoro.onnx',TTS+'voices-v1.0.bin')
S=json.load(open('script.json')); out=[]
for si,(name,lines) in enumerate(S):
    sc=[]
    for li,t in enumerate(lines):
        a,sr=k.create(t,voice='am_michael',speed=1.28,lang='en-us')
        # trim silence
        idx=np.where(np.abs(a)>0.01)[0]; a=a[max(0,idx[0]-240):idx[-1]+1200]
        f=f'vo/{si:02d}_{li}.wav'; sf.write(f,a,sr); sc.append([t,f,len(a)/sr])
    out.append([name,sc]); print(name,[round(x[2],2) for x in sc])
json.dump(out,open('vo.json','w'))
