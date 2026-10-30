const {chromium}=require('playwright');const fs=require('fs');
const slugs=process.argv.slice(2);const only=process.env.ONLY_STILL;
(async()=>{const b=await chromium.launch();
for(const s of slugs){const p=await b.newPage({viewport:{width:1080,height:1920}});
 // cover
 await p.goto('file://'+process.cwd()+'/out/'+s+'-cover.html');await p.waitForLoadState('networkidle');await p.evaluate(()=>document.fonts.ready);await p.evaluate(()=>window.fit&&window.fit());
 await p.screenshot({path:`out/${s}-cover.png`});
 await p.goto('file://'+process.cwd()+'/out/'+s+'.html');await p.waitForLoadState('networkidle');await p.evaluate(()=>document.fonts.ready);await p.evaluate(()=>window.fit&&window.fit());
 await p.evaluate(()=>document.getAnimations().forEach(a=>a.pause()));
 if(only){await p.evaluate(()=>document.getAnimations().forEach(a=>a.currentTime=8000));await p.screenshot({path:`out/${s}-final.png`});await p.close();continue;}
 fs.mkdirSync(`out/f-${s}`,{recursive:true});
 for(let i=0;i<300;i++){await p.evaluate(t=>document.getAnimations().forEach(a=>a.currentTime=t),i*1000/30);
  await p.screenshot({path:`out/f-${s}/${String(i).padStart(4,'0')}.png`});}
 await p.close();}
await b.close();})();
