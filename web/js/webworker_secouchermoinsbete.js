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
var href = '';
var content = '';

load('http://allorigins.me/get?url=' + encodeURIComponent('http://secouchermoinsbete.fr/') + '&callback=?', function(xhr) {
	
	var result_html = xhr.responseText;
	html_content = JSON.parse(result_html.substring(27, result_html.length - 2))['contents'];

	const $ = cheerio.load(html_content)

	content = $('.summary').first().children('a').text();
	href = $('.summary').first().children('a').attr('href');

	const result = {'href': href, 'content': content};
	self.postMessage(result);
});

