function match_complex_tag(l_complex, page_text_content, weight)
{
	var global_weight = 0;

	for (var i = 0; i <= l_complex.length - 1; i++)
	{
		var s_regexp = '';
		var complex_tag = l_complex[i].split(/[ \-]/);
		for (var j = 0; j <= complex_tag.length - 2; j++)
		{
			s_regexp += complex_tag[j]+'[ \-_]?';
		}
		s_regexp += complex_tag[j];
		var reg = new RegExp(s_regexp, 'igm');
		var match_tab = page_text_content.match(reg);
		if (match_tab)
		{	
			console.log(match_tab);
			global_weight += match_tab.length * weight
		}
	}

	return global_weight;
}

function match_simple_tag(l_simple, page_text_content, weight)
{
	var global_weight = 0;

	for (var i = 0; i <= l_simple.length - 1; i++)
	{
		var simple_tag = l_simple[i];
		var reg = new RegExp(simple_tag, 'igm');
		var match_tab = page_text_content.match(reg);
		if (match_tab)
		{
			console.log(match_tab);
			global_weight += match_tab.length * weight
		}
	}
	return global_weight;
}

var page_weight = 0;
var page_text_content = document.body.textContent.replace(/\s{2,}|\n/gi, ' ');

page_weight += match_complex_tag(l_100_complex, page_text_content, 100);
page_weight += match_complex_tag(l_50_complex, page_text_content, 50);
page_weight += match_simple_tag(l_100, page_text_content, 100);
page_weight += match_simple_tag(l_50, page_text_content, 50);

console.log(page_weight);

l_page_word = page_text_content.split(' ');
const l_page_word_filter = l_page_word.filter(word => word.length > 3);

if (page_weight > l_page_word_filter.length)
{
	browser.runtime.sendMessage({closeThis: true});
}