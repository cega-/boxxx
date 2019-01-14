$(document).ready(function() {

	const worker = new Worker('/web/js/webworker_mon_poeme_proverbe_bundle.js'); // create our worker
	worker.postMessage({ firstNum: 4, secondNum: 6 }); // post a message to our worker

	worker.onmessage = event => { // listen for events from the worker
		//console.log(`Result is: ${event.data}`);
		console.log(event.data);
		var context = {mon_poeme_proverbe_content: event.data['content'], mon_poeme_proverbe_origin: event.data['origin']};
		var template = Handlebars.templates['mon_poeme_proverbe'];
		var html = template(context);

		$('#widget_main_quote').append(html);
	};
});