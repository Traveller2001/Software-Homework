const querystring = require('querystring');
const https = require('https');
const cheerio = require('cheerio');//第三方
const zlib = require('zlib');
module.exports = {
		getCover: function(file, req, response){}//处理的操作全放在这里
    }

var website = "https://open.163.com/newview/movie/courseintro?newurl=%2Fspecial%2Fcuvocw%2Fyinyuemeixue.html";
var flag = -1;
if(website.indexOf("https://www.bilibili.com") != -1){
    flag=1;
}
else if(website.indexOf("https://www.icourse163.org") != -1){
    flag=2;
}
else if(website.indexOf("https://coursehome.zhihuishu.com") != -1){
    flag=3;
}
else if(website.indexOf("https://open.163.com/newview/movie/courseintro") != -1){
    flag=4;
}
else if(website.indexOf("https://open.163.com/newview/movie/free?pid") != -1){
    flag=5;
}

if(flag==1)
{
    
    
    https.get(website,function(res){
   
    let html = '';
    var output;
    if(res.headers['content-encoding'] == 'gzip'){//处理gzip格式的网页
        var gzip=zlib.createGunzip();
        res.pipe(gzip);
        output=gzip;
    }else{
        output = res;
    }
    
    output.on('data',function(data){
        data = data.toString('utf-8');
        html += data;
    })
    // 拼接完成

    output.on('end',function(){
        const $ = cheerio.load(html);
     
        const title = $("meta[property='og:title']").attr('content');
        const photo = $("meta[property='og:image']").attr('content');

        console.log(title,photo);
                 
    })
})
}


else if(flag==2)
{
    
const https = require('https');
const cheerio = require('cheerio');
const fs = require('fs');

https.get(website,function(res){
   
    let html = '';
  
    res.on('data',function(chunk){
        html += chunk;
    })
    // 拼接完成
    res.on('end',function(){
        const $ = cheerio.load(html);
     
        const title = $('title').text();
        const photo = $('div.m-recimg').children(0).attr('src');   

        console.log(title,photo);
          
          
    })
})

}

else if(flag==3)
{
    
const https = require('https');
const cheerio = require('cheerio');
const fs = require('fs');

https.get(website,function(res){
   
    let html = '';
  
    res.on('data',function(chunk){
        html += chunk;
    })
    // 拼接完成
    res.on('end',function(){
        const $ = cheerio.load(html);
     
        const title = $('div.course-name').text();
        const photo = $('div.course-img').children(0).attr('src');   

        console.log(title,photo);
          
          
    })
})

}

else if(flag==4)
{
    
const https = require('https');
const cheerio = require('cheerio');
const fs = require('fs');

https.get(website,function(res){
   
    let html = '';
  
    res.on('data',function(chunk){
        html += chunk;
    })
    // 拼接完成
    res.on('end',function(){
        const $ = cheerio.load(html);
     
        const title = $('div.content-title').text();
        const photo = $('div.content-left').children(0).attr('src');
           
        console.log(title,photo);
          
    })
})

}


else if (flag==5)
{
    
const https = require('https');
const cheerio = require('cheerio');
const fs = require('fs');

https.get(website,function(res){
   
    let html = '';
  
    res.on('data',function(chunk){
        html += chunk;
    })
    // 拼接完成
    res.on('end',function(){
        const $ = cheerio.load(html);
     
        const title = $('title').text();
           
        console.log(title);
          
          
    })
})

}

else
{
    console.log("链接不合法！")
}