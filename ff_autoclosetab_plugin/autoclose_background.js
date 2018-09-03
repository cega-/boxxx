browser.runtime.onMessage.addListener(function(message, sender, sendResponse)
{
	if(message.closeThis) browser.tabs.remove(sender.tab.id);
});