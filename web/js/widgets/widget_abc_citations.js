$(document).ready(function() {

	const worker = new Worker('/web/js/webworker_abc_citations_bundle.js'); // create our worker
	worker.postMessage({ firstNum: 4, secondNum: 6 }); // post a message to our worker

	worker.onmessage = event => { // listen for events from the worker
		//console.log(`Result is: ${event.data}`);
		console.log(event.data);
		var context = {abc_citations_content: event.data['content'], abc_citations_author: event.data['author']};
		var template = Handlebars.templates['abc_citations'];
		var html = template(context);

		$('#widget_main_quote').append(html);
	};
});