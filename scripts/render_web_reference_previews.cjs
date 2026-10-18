/* Optional renderer: requires Playwright and its Chromium browser; makes no network requests. */
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require('playwright');
const root=path.resolve(__dirname,'..'), output=path.join(root,'docs/images');
const pages=['home','benchmark','monitoring','follow-up','changes','decisions','report-back','data-qa'];
(async()=>{
  const browser=await chromium.launch({headless:true,...(process.env.CHROMIUM_EXECUTABLE_PATH?{executablePath:process.env.CHROMIUM_EXECUTABLE_PATH}:{})});
  try{
    const page=await browser.newPage({viewport:{width:1440,height:1040},deviceScaleFactor:1});
    await page.route('**/*',route=>route.request().url().startsWith('file:')?route.continue():route.abort());
    for(const key of pages){
      await page.goto(pathToFileURL(path.join(output,'northstar-web-reference.html')).href+'#'+key);
      await page.locator('#'+key).waitFor({state:'visible'});
      await page.evaluate(()=>window.scrollTo(0,0));
      await page.screenshot({path:path.join(output,`northstar-web-${key}.png`),fullPage:true});
    }
    // Mobile smoke check: cards fit; wide data tables scroll within their card.
    await page.setViewportSize({width:390,height:844});
    for(const key of pages){
      await page.goto(pathToFileURL(path.join(output,'northstar-web-reference.html')).href+'#'+key);
      const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth);
      if(overflow)throw Error(`Page overflow at 390px: ${key}`);
    }
    console.log('Rendered eight synthetic pages at 1440px; all eight fit at 390px.');
  }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
