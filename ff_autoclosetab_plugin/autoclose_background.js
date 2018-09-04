var result_html = null;

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

browser.runtime.onMessage.addListener(function(message, sender, sendResponse)
{
	if(message.closeThis)
	{
		browser.tabs.remove(sender.tab.id);
		//browser.tabs.update(sender.tab.id, {url: "https://news.google.fr", loadReplace: true});
	}
});

/*
load('http://nepi-vtu16.neuilly.ratp/web/black_list.json', function(xhr)
{
	result_html = xhr.responseText;
});

browser.runtime.onMessage.addListener(function(message, sender, sendResponse)
{
	if (message.func == 'getBlacklist')
	{
		browser.tabs.sendMessage(sender.tab.id, result_html);
	}
}
*/