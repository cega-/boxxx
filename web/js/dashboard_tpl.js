$(document).ready(function() {

	const worker = new Worker('/web/js/bundle.js'); // create our worker
	worker.postMessage({ firstNum: 4, secondNum: 6 }); // post a message to our worker

	worker.onmessage = event => { // listen for events from the worker
		//console.log(`Result is: ${event.data}`);
		console.log(event.data);
		var context = {title: "My New Post", body: event.data['content']};
		var template = Handlebars.templates['test'];
		var html = template(context);

		console.log(html);
	};

	

});