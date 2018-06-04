// webworker.js
const cheerio = require('cheerio')


function load(url, callback) {
	var xhr;

	if(typeof XMLHttpRequest !== 'undefined') xhr = new XMLHttpRequest();
	else {
		var versions = ["MSXML2.XmlHttp.5.0", 
			 	"MSXML2.XmlHttp.4.0",
			 	"MSXML2.XmlHttp.3.0", 
			 	"MSXML2.XmlHttp.2.0",
			 	"Microsoft.XmlHttp"]

		for(var i = 0, len = versions.length; i < len; i++) {
		try {
			xhr = new ActiveXObject(versions[i]);
			break;
		}
			catch(e){}
		} // end for
	}
		
	xhr.onreadystatechange = ensureReadiness;
		
	function ensureReadiness() {
		if(xhr.readyState < 4) {
			return;
		}
			
		if(xhr.status !== 200) {
			return;
		}

		// all is well	
		if(xhr.readyState === 4) {
			callback(xhr);
		}			
	}
		
	xhr.open('GET', url, true);
	xhr.send('');
}
	
//and here is how you use it to load a json file with ajax



self.onmessage = event => { // listen for messages from the main thread
	console.log('Worker received event from main thread..');
	const result = event.data.firstNum + event.data.secondNum;
var result_html = '';
load('http://www.google.com', function(xhr) {	
	result_html = xhr.responseText;	
});

const $ = cheerio.load(result_html)

console.log('*****');
console.log($.html());
console.log('*****');

var companiesList = [];

// For each .item, we add all the structure of a company to the companiesList array
// Don't try to understand what follows because we will do it differently.
$('p').each(function(index, element){
	companiesList[index] = {};
	console.log(element);
});



	self.postMessage(result);
};