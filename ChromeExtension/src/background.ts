import {ApplicationPuzzleTapa} from "./PuzzleTapa";
import {ApplicationPuzzleBinairoPlus} from "./PuzzleBinairoPlus";
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
        case 'www.puzzle-binairo.com':
            chrome.scripting.executeScript({
                target: {tabId: tab.id!},
                func: ApplicationPuzzleBinairoPlus,
            }).then();
            break;
        case 'www.puzzles-mobile.com':
            chrome.scripting.executeScript({
                target: {tabId: tab.id!},
                func: ApplicationPuzzleBinairoPlus,
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

