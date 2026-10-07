const fs = require('fs');
const path = require('path');
const {chromium} = require('C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
const server=require('./preview.cjs').createPreviewServer();
await new Promise(resolve=>server.listen(8123,'127.0.0.1',resolve));
const browser = await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
const page = await browser.newPage();
await page.route('https://fonts.googleapis.com/**',route=>route.abort());
await page.route('https://fonts.gstatic.com/**',route=>route.abort());
if(process.argv.includes('--focused')){
  await page.goto('http://127.0.0.1:8123/blog.html');await page.locator('.search-bar').fill('battery');
  const first=page.locator('.search-results a').first();const target=await first.getAttribute('href');await first.focus();
  await Promise.all([page.waitForURL(target,{waitUntil:'domcontentloaded'}),page.keyboard.press('Enter')]);
  const checks=JSON.parse(fs.readFileSync('qa/acceptance-results.json'));
  checks.find(c=>c.name==='Writing search link navigates').passed=page.url()===target;
  fs.writeFileSync('qa/acceptance-results.json',JSON.stringify(checks,null,2));
  console.log('Keyboard search navigated:',page.url());
  const response=await page.goto('http://127.0.0.1:8123/nested/not-found');console.log('Preview 404:',response.status());
  const prior=JSON.parse(fs.readFileSync('qa/browser-results.json'));
  for(const width of [1440,1024,768,375,320,667]){
    await page.setViewportSize({width,height:900});await page.goto('http://127.0.0.1:8123/project-hess.html');
    await page.evaluate(async()=>{document.querySelectorAll('img').forEach(i=>i.loading='eager');await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));});
    const row=prior.find(r=>r.file==='project-hess.html'&&r.width===width);
    row.overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);
    row.broken=await page.evaluate(()=>[...document.images].filter(i=>i.getAttribute('src')&&!i.naturalWidth).map(i=>i.src));
    if([1440,375].includes(width))await page.screenshot({path:`qa/project-hess-${width}.png`,fullPage:true});
  }
  fs.writeFileSync('qa/browser-results.json',JSON.stringify(prior,null,2));console.log('HESS diagram and media checked at six widths.');
  await page.unroute('https://fonts.googleapis.com/**');await page.unroute('https://fonts.gstatic.com/**');
  for(const file of ['index.html','Projects.html','project-hess.html','How_to_survive.html','Photography.html']){
    await page.setViewportSize({width:1440,height:1000});await page.goto('http://127.0.0.1:8123/'+file);
    await page.evaluate(async()=>{document.querySelectorAll('img').forEach(i=>i.loading='eager');document.querySelectorAll('.reveal').forEach(e=>e.classList.add('show'));await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));await document.fonts.ready;});
    for(const width of [1440,375]){await page.setViewportSize({width,height:1000});await page.screenshot({path:`qa/${file.replace('.html','')}-${width}.png`,fullPage:true});}
  }
  await browser.close();server.close();return;
}
const results=[];
const acceptance=process.argv.includes('--acceptance');
for(const width of [1440,1024,768,375,320,667]) {
  await page.setViewportSize({width,height:width===667?375:900});
  for(const file of fs.readdirSync('.').filter(x=>x.endsWith('.html')&&(!acceptance||x==='VAnity_cards.html'))) {
    const errors=[]; const onError=e=>errors.push(e.message);page.on('pageerror',onError);
    await page.goto('http://127.0.0.1:8123/'+file,{waitUntil:'domcontentloaded'});
    if(file==='test.html')await page.waitForURL('**/blog.html',{waitUntil:'domcontentloaded'});
    await page.waitForTimeout(100);
    const info=await page.evaluate(()=>({
      overflow:document.documentElement.scrollWidth>innerWidth+1,
      wide:[...document.querySelectorAll('main *')].filter(e=>e.getBoundingClientRect().right>innerWidth+2).slice(0,8).map(e=>e.tagName+'.'+e.className),
      h1:document.querySelectorAll('h1').length,
      broken:[...document.images].filter(i=>i.getAttribute('src')&&i.complete&&!i.naturalWidth).map(i=>i.getAttribute('src')),
      nav:!!document.querySelector('.site-nav'),
      main:!!document.querySelector('#main')
    }));
    results.push({file,width,...info,errors});page.off('pageerror',onError);
    if(!acceptance)fs.writeFileSync('qa/browser-results.json',JSON.stringify(results,null,2));
    if(['index.html','Projects.html','about.html','blog.html','project-hess.html','Battery_Data_driven.html','Digitwin.html','Contact.html'].includes(file)&&[1440,375].includes(width)){
      await page.evaluate(()=>document.querySelectorAll('img').forEach(i=>i.loading='eager'));
      await page.evaluate(async()=>{
        document.querySelectorAll('.reveal').forEach(el=>el.classList.add('show'));
        await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));
      });
      await page.screenshot({path:path.join('qa',file.replace('.html','')+'-'+width+'.png'),fullPage:true,timeout:10000});
    }
  }
}
if(acceptance){
  const prior=JSON.parse(fs.readFileSync('qa/browser-results.json'));
  fs.writeFileSync('qa/browser-results.json',JSON.stringify(prior.filter(r=>r.file!=='VAnity_cards.html').concat(results),null,2));
  const checks=[];
  const assert=(name,ok)=>{checks.push({name,passed:!!ok});};
  await page.setViewportSize({width:375,height:812});
  await page.goto('http://127.0.0.1:8123/index.html');
  await page.locator('.menu').click();assert('Mobile menu opens',await page.locator('.menu').getAttribute('aria-expanded')==='true');
  await page.keyboard.press('Escape');assert('Escape closes menu and returns focus',await page.locator('.menu').getAttribute('aria-expanded')==='false'&&await page.locator('.menu').evaluate(e=>e===document.activeElement));
  await page.keyboard.press('Tab');
  await page.locator('.menu').click();await page.locator('#site-links a[href="/Projects.html"]').click();assert('Mobile project navigation',page.url().endsWith('/Projects.html'));
  await page.goto('http://127.0.0.1:8123/blog.html');await page.locator('.search-bar').fill('battery');
  assert('Writing search returns keyboard links',await page.locator('.search-results a').count()>0);
  const resultLink=page.locator('.search-results a').first();const resultURL=await resultLink.getAttribute('href');await resultLink.focus();await Promise.all([page.waitForURL(resultURL,{waitUntil:'domcontentloaded'}),page.keyboard.press('Enter')]);assert('Writing search link navigates',page.url()===resultURL);
  await page.goto('http://127.0.0.1:8123/Data_science.html');await page.locator('details.lib-card summary').first().click();assert('Tool examples open without custom scripts',await page.locator('details.lib-card').first().getAttribute('open')!==null);
  await page.goto('http://127.0.0.1:8123/SGPT.html');const before=await page.locator('.bilingual-text').first().textContent();await page.locator('#languageToggle').click();assert('Shona translation toggle',before!==await page.locator('.bilingual-text').first().textContent());
  await page.goto('http://127.0.0.1:8123/VAnity_cards.html');await page.locator('#nextBtn').click();assert('Existing vanity-card navigation',await page.locator('#current').textContent()==='2');
  const response=await page.goto('http://127.0.0.1:8123/missing/nested-page');assert('Custom 404 response',response.status()===404&&await page.locator('h1').textContent()==='Nothing here.');await page.locator('.button').click();assert('404 returns home from nested URLs',page.url().endsWith('/index.html'));
  const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:375,height:812}});const plain=await nojs.newPage();
  await plain.route('https://fonts.googleapis.com/**',r=>r.abort());await plain.route('https://fonts.gstatic.com/**',r=>r.abort());
  for(const file of fs.readdirSync('.').filter(x=>x.endsWith('.html')&&x!=='test.html')){
    await plain.goto('http://127.0.0.1:8123/'+file,{waitUntil:'domcontentloaded'});
    assert('No-JS content and navigation: '+file,await plain.locator('h1').isVisible()&&await plain.locator('#site-links').isVisible());
  }
  await nojs.close();
  await page.emulateMedia({reducedMotion:'reduce'});
  for(const file of ['index.html','blog.html','Projects.html','Uninspired1.html','VAnity_cards.html']){
    await page.goto('http://127.0.0.1:8123/'+file,{waitUntil:'domcontentloaded'});
    assert('Reduced-motion visible content: '+file,await page.locator('h1').evaluate(e=>getComputedStyle(e).opacity==='1')&&await page.evaluate(()=>[...document.querySelectorAll('.reveal')].every(e=>getComputedStyle(e).opacity==='1')));
  }
  const visual=await browser.newPage({viewport:{width:1440,height:1000}});
  for(const file of ['index.html','Projects.html','blog.html','about.html','project-hess.html','Battery_Data_driven.html','Digitwin.html','Contact.html']){
    await visual.goto('http://127.0.0.1:8123/'+file,{waitUntil:'load'});
    await visual.evaluate(async()=>{document.querySelectorAll('img').forEach(i=>i.loading='eager');document.querySelectorAll('.reveal').forEach(e=>e.classList.add('show'));await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));await document.fonts.ready;});
    assert('Decoded images: '+file,await visual.evaluate(()=>[...document.images].every(i=>!i.getAttribute('src')||i.naturalWidth>0)));
    for(const width of [1440,375]){
      await visual.setViewportSize({width,height:1000});
      assert('Loaded-font layout: '+file+' / '+width,await visual.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
      await visual.screenshot({path:'qa/'+file.replace('.html','')+'-'+width+'.png',fullPage:true});
    }
  }
  fs.writeFileSync('qa/acceptance-results.json',JSON.stringify(checks,null,2));console.log('Acceptance:',checks.length,'checks;',checks.filter(c=>!c.passed));
  const links=JSON.parse(fs.readFileSync('qa/static-results.json')).external_links;let cursor=0;const external=[];
  await Promise.all(Array.from({length:8},async()=>{while(cursor<links.length){const url=links[cursor++];try{const response=await browser.contexts()[0].request.get(url,{timeout:10000});external.push({url,status:response.status(),final_url:response.url()});await response.dispose();}catch(e){external.push({url,error:e.message.split('\n')[0]});}}}));
  fs.writeFileSync('qa/external-results.json',JSON.stringify(external,null,2));console.log('External links:',external.length,'checked;',external.filter(e=>e.error||e.status>=400).length,'require manual review.');
}
if(!acceptance)fs.writeFileSync('qa/browser-results.json',JSON.stringify(results,null,2));
console.log(JSON.stringify(results.filter(r=>r.overflow||r.errors.length||r.broken.length||r.h1!==1||!r.nav||!r.main),null,2));
await browser.close();
server.close();
})();
