const puppeteer = require('puppeteer');
// const cheerio = require('cheerio');
// let xlsx = require("json-as-xlsx")
// const timers = require("timers");
// const { DOMParser } = require('xmldom');
// const { log } = require('console');

// const TARGET_URL = 'https://apcohandlooms.com/product-category/sarees/' // Saree

// const TARGET_URL = 'https://apcohandlooms.com/product-category/apparels/dress-material/' //Kurta Sets

// const TARGET_URL = 'https://apcohandlooms.com/product-category/mens-wear/cotton-dhotis/' //cotton Dhotis
// const TARGET_URL = 'https://apcohandlooms.com/product-category/mens-wear/cotton-lungies/' // cotton Lungis
// const TARGET_URL = 'https://apcohandlooms.com/product-category/mens-wear/shirts/' // Shirt
// const TARGET_URL = 'https://apcohandlooms.com/product-category/mens-wear/kurtas/' //KUrta
// const TARGET_URL = 'https://apcohandlooms.com/product-category/home-decor/bed-sheets/' // BedSheet
// const TARGET_URL = 'https://apcohandlooms.com/product-category/home-decor/cotton-blankets/' // Blankets
const TARGET_URL = 'https://www.dropbox.com/s/ce0ubbg20ekwleu/N02A8777.JPG?e=1&dl=0' // Towel



async function main() {
    const browser = await puppeteer.launch({headless: false});
    let catalogue = [];
    // get page count
    const tab = await browser.newPage();
    await tab.setViewport({ width: 1920, height: 1080});
    await tab.goto(TARGET_URL);
    await tab.goto(TARGET_URL);
    

    setTimeout(() => {
        // m17.5 6.5-11 11m11 0-11-11
        
       

         tab.waitForSelector('path[d="m17.5 6.5-11 11m11 0-11-11"]');

        // Click the element
         tab.click('path[d="m17.5 6.5-11 11m11 0-11-11"]');

         



        setTimeout(()=>{
            setTimeout(()=>{
                tab.screenshot({path : 'example.png' , fullPage : true});
                setTimeout(()=>{
                    tab.screenshot({path : 'example.png' , fullPage : true});

                    const html = tab.content();
                    console.log('HTML value:', html);
                    
               const srcValue =  tab.$eval('img._fullSizeImg_1vnnd_16', (img) => img.getAttribute('src'));
      
                console.log('src value:', srcValue);
                console.log("STEP -- > 4");
                },5000);
                console.log("STEP -- > 3");
                // tab.waitForSelector('#accept_all_cookies_button');

                // // Click the button
                //  tab.click('#accept_all_cookies_button');
       
            },2000);
            tab.$eval(' .dig-Button.dig-Button--transparent.In-Theme-Provider', button => {
                button.click();
              });

              console.log("STEP -- > 2");
        },2000);
        
        // browser.close();
    }, 6000);
    console.log("STEP -- > 1");
    

// Use page.$eval to extract the src attribute directly


// // Close the browser

}

main();