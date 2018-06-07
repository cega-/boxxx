$(document).ready(function() {

	const worker = new Worker('/web/js/webworker_secouchermoinsbete_bundle.js'); // create our worker
	worker.postMessage({ firstNum: 4, secondNum: 6 }); // post a message to our worker

	worker.onmessage = event => { // listen for events from the worker
		//console.log(`Result is: ${event.data}`);
		console.log(event.data);
		var context = {secouchermoinsbete_content: event.data['content']};
		var template = Handlebars.templates['secouchermoinsbete'];
		var html = template(context);

		$('#widget_secouchermoinsbete').append(html);
	};
});