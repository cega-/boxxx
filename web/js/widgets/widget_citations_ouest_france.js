$(document).ready(function() {

	console.log('\\\\\\\\\\\\///////////////////****************');

	const worker = new Worker('/web/js/webworker_citations_ouest_france_bundle.js'); // create our worker
	worker.postMessage({ firstNum: 4, secondNum: 6 }); // post a message to our worker

	worker.onmessage = event => { // listen for events from the worker
		//console.log(`Result is: ${event.data}`);
		console.log(event.data);
		var context = {citations_ouest_france_content: event.data['content'], citations_ouest_france_author: event.data['author']};
		var template = Handlebars.templates['citations_ouest_france'];
		var html = template(context);

		$('#widget_quote').append(html);
	};
});