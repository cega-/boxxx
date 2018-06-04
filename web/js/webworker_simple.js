// webworker.js
self.onmessage = event => { // listen for messages from the main thread
	console.log('Worker received event from main thread..');
	//const result = event.data.firstNum + event.data.secondNum;
	const result = {'toto': 'titi', 1: 'super'};
	self.postMessage(result);
};