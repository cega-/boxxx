$(document).ready(function() {

	const worker = new Worker('/web/js/webworker_test_bundle.js'); // create our worker
	worker.postMessage({ firstNum: 4, secondNum: 6 }); // post a message to our worker

	worker.onmessage = event => { // listen for events from the worker
		//console.log(`Result is: ${event.data}`);
		console.log(event.data);
		var content_day_article = event.data['content_day_article'];

		var context = {test_content: event.data['content_day_article']};
		var template = Handlebars.templates['test_template'];
		var html = template(context);

		console.log(html)

		$('#widget_test').append(html);

	};
});