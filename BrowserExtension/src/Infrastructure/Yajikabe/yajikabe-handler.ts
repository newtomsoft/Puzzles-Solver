import { BasePuzzleHandler } from '../Base/base-puzzle-handler.js';
import { YajikabeGridProvider } from './yajikabe-grid-provider.js';

export class YajikabeHandler extends BasePuzzleHandler {
    constructor() {
        super('yajikabe', 'yajikabe', new YajikabeGridProvider());
    }
}
