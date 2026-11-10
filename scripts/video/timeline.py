import json, numpy as np, soundfile as sf
V=json.load(open('vo.json'))
MIN={'title':2.2,'streak':2.6,'low':3.4,'chart':3.8,'ranks':4.6,'high':2.8,'love':2.0,'emmett':3.4,'median':3.2,'outro':4.2}
GAP={'roast':0.06}
tl=[];t=0;sr=24000
for name,lines in V:
    at=0.08; L=[]
    for txt,f,ln in lines:
        L.append({'text':txt,'file':f,'at':round(at,3),'len':round(ln,3)}); at+=ln+GAP.get(name,0.09)
    dur=max(MIN.get(name,0),at+0.16)
    tl.append({'name':name,'dur':round(dur,3),'lines':L}); t+=dur
json.dump(tl,open('tl.json','w'))
N=int((t+0.5)*sr); voice=np.zeros(N); acc=0
for s in tl:
    for l in s['lines']:
        a,_=sf.read(l['file']); i=int((acc+l['at'])*sr); voice[i:i+len(a)]+=a[:N-i]
    acc+=s['dur']
sf.write('voice.wav',voice,sr)
print('total',round(t,2),[ (s['name'],s['dur']) for s in tl])
