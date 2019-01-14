$(document).ready(function() {

	const worker = new Worker('/web/js/webworker_france24_infocontinu_bundle.js'); // create our worker
	worker.postMessage({ firstNum: 4, secondNum: 6 }); // post a message to our worker

	worker.onmessage = event => { // listen for events from the worker
		//console.log(`Result is: ${event.data}`);
		console.log(event.data);
		var context = {france24_infocontinu_content: event.data['content'], france24_infocontinu_time: event.data['time']};
		var template = Handlebars.templates['france24_infocontinu'];
		var html = template(context);

		$('#widget_breaking_news').append(html);
	};
});