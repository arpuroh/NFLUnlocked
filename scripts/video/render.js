const {chromium}=require('playwright');const {spawn}=require('child_process');const fs=require('fs');
(async()=>{
 const mode=process.argv[2]||'preview';
 const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1920}});
 await pg.goto('file://'+__dirname+'/reel.html');
 await pg.evaluate(async()=>{await document.fonts.load('900 100px Arc');await document.fonts.load('700 100px Arc');await document.fonts.ready;});
 const TL=JSON.parse(fs.readFileSync(__dirname+'/tl.json'));const total=await pg.evaluate(tl=>setTL(tl),TL);const cuts=await pg.evaluate(()=>CUTS);
 fs.writeFileSync('cuts.json',JSON.stringify({total,cuts}));
 if(mode==='preview'){
  const ts=process.argv.slice(3).map(Number);
  for(const t of ts){const d=await pg.evaluate(t=>render(t),t);fs.writeFileSync(`pv_${t}.jpg`,Buffer.from(d.split(',')[1],'base64'));}
 } else {
  const fps=30,n=Math.round(total*fps);
  const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-c:v','mjpeg','-framerate','30','-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','23','-preset','medium','silent.mp4']);
  for(let i=0;i<n;i++){const d=await pg.evaluate(t=>render(t),i/fps);const buf=Buffer.from(d.split(',')[1],'base64');if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));}
  ff.stdin.end();await new Promise(r=>ff.on('close',r));
 }
 console.log('total',total);await b.close();})();
