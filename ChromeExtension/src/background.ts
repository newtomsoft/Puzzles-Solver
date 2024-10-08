import {ApplicationPuzzleTapa} from "./PuzzleTapa";
import {NotSupportedWebsite} from "./notSupportedWebsite";

chrome.action.onClicked.addListener((tab) => {
    const url = new URL(tab.url!);
    console.log(url.hostname);
    switch (url.hostname) {
        case 'www.puzzle-tapa.com':
            chrome.scripting.executeScript({
                target: {tabId: tab.id!},
                func: ApplicationPuzzleTapa,
            }).then();
            break;
        default:
            chrome.scripting.executeScript({
                target: {tabId: tab.id!},
                func: NotSupportedWebsite,
                args: [url.href]
            }).then();
    }
});

