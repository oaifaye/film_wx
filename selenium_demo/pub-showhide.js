var tags=document.getElementsByTagName('input');for(var i=0;i < tags.length; i++){
if(tags[i].type = 'button' || tags[i].type = 'submit')tags[i].style.display= 'block';}



page.onNavigationRequested = function(url, type, willNavigate, main) {page.browserLog.push('url:'+url+'==='+willNavigate)}
      console.log('Trying to navigate to: ' + url);
      console.log('Caused by: ' + type);
      console.log('Will actually navigate: ' + willNavigate);
      console.log('Sent from the page\'s main frame: ' + main);
}