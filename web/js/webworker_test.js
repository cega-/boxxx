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

load('http://allorigins.me/get?url=' + encodeURIComponent('https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Accueil_principal') + '&callback=?', function(xhr) {
	
	var result_html = xhr.responseText;
	var content_day_article = '';
	html_content = JSON.parse(result_html.substring(27, result_html.length - 2))['contents'];

	const $ = cheerio.load(html_content)

	img_day_article = $('#Article_labellisé_du_jour').parent().next().find('img').attr('src');

	$('#Article_labellisé_du_jour').parent().parent().find('p').each(function(index, val){
		$(val).find('a').each(function(){
			ori_href = $( this ).attr('href');
			$( this ).attr('href', "https://fr.wikipedia.org" + ori_href);
		});
		content_day_article += '<p>'+$(val).html()+'</p>';
	});

	var know_more_article = '';
	ori_href = $('#Article_labellisé_du_jour').parent().parent().children('ul').find('a').attr('href');
	know_more_article = $('#Article_labellisé_du_jour').parent().parent().children('ul').find('a').attr('href', "https://fr.wikipedia.org" + ori_href);
	var href_view_more = know_more_article.attr('href');


	var content_news = '<ul>';
	$('#Actualités').parent().parent().children('ul').children('li').each(function(index, val){
		$(val).find('a').each(function(){
			ori_href = $( this ).attr('href');
			$( this ).attr('href', "https://fr.wikipedia.org" + ori_href);
		});
		content_news += '<li>'+$(val).html()+'</li>';
	});
	content_news += '</ul>';

//	console.log(content_news);


	var content_do_you_know = '<ul>';
	console.log($('[id^=Le_saviez-vous]'));
	$('[id^=Le_saviez-vous]').parent().parent().children('ul').children('li').each(function(index, val){
		$(val).find('a').each(function(){
			ori_href = $( this ).attr('href');
			$( this ).attr('href', "https://fr.wikipedia.org" + ori_href);
		});
		content_do_you_know += '<li>'+$(val).html()+'</li>';
	});
	content_do_you_know += '</ul>';

//	console.log(content_do_you_know);

	var content_ephemeris = '<ul>';
	var content_ephemeris_title = $('[id^=Éphéméride_du_]').text();
	$('[id^=Éphéméride_du_]').parent().parent().children('ul').children('li').each(function(index, val){
		$(val).find('a').each(function(){
			ori_href = $( this ).attr('href');
			$( this ).attr('href', "https://fr.wikipedia.org" + ori_href);
		});
		content_ephemeris += '<li>'+$(val).html()+'</li>';
	});
	content_ephemeris += '</ul>';

//	console.log(content_ephemeris);

	var picture_of_the_day = '';
	$('#Image_labellisée_du_jour').parent().parent().children('div').children('div').each(function(index, val){
		$(val).find('a').each(function(){
			ori_href = $( this ).attr('href');
			$( this ).attr('href', "https://fr.wikipedia.org" + ori_href);
		});
		picture_of_the_day += '<div>'+$(val).html()+'</div>';
	});

	console.log(picture_of_the_day);


//	console.log(content_day_article);
	const result = {'img_day_article': img_day_article, 'content_day_article': content_day_article, 'href_view_more': href_view_more};
	self.postMessage(result);
});