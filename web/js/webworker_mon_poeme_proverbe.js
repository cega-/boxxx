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

var html_content = '';
var origin = '';
var content = '';

load('https://cors-anywhere.herokuapp.com/https://www.mon-poeme.fr/proverbe-du-jour/', function(xhr) {
	
	var result_html = xhr.responseText;

	//html_content = JSON.parse(result_html.substring(27, result_html.length - 2))['contents'];
	html_content = result_html.substring(27, result_html.length - 2);
	console.log(html_content);

	const $ = cheerio.load(html_content)

	content = $('.post p q').first().text();
	origin = $('.post p a').first().text();

	const result = {'origin': origin, 'content': content};

	self.postMessage(result);
});