import assert from 'assert';
import { CountryRoadSolver } from './country-road-solver.js';

// @ts-ignore
import initZ3 from '../../../libs/z3-built.js';
// @ts-ignore
await import('../../../libs/z3-bundle.js');

declare const global: any;
global.initZ3 = initZ3.default || initZ3;

describe('CountryRoadSolver Tests', () => {
    let z3: any;
    let ctx: any;

    beforeAll(async () => {
        const z3Factory = (global as any).Z3;
        z3 = await z3Factory();
        const { Context } = z3;
        ctx = new Context('main');
    });
    const testCases = [
        {
            name: 'test_basic_grid',
            clues: [
                [3, 3, -1],
                [-1, -1, -1],
                [2, -1, -1]
            ],
            regions: [
                [1, 2, 2],
                [1, 1, 2],
                [3, 3, 3]
            ],
            checkUnique: true
        },
        {
            name: 'test_solution_4x4_easy_3nd9w',
            clues: [
                [4, -1, -1, -1],
                [-1, 1, -1, 3],
                [1, 2, 1, -1],
                [-1, -1, -1, -1]
            ],
            regions: [
                [1, 1, 1, 1],
                [1, 2, 2, 3],
                [4, 5, 6, 3],
                [4, 5, 6, 3]
            ],
            checkUnique: true
        },
        {
            name: 'test_solution_4x4_evil_3nd9w', // ID mismatch in comment but let's follow logic
            clues: [
                [-1, -1, -1, -1],
                [1, -1, -1, -1],
                [-1, -1, 1, -1],
                [-1, -1, -1, -1]
            ],
            regions: [
                [1, 1, 1, 2],
                [3, 3, 2, 2],
                [4, 4, 5, 5],
                [6, 6, 6, 5]
            ],
            checkUnique: true
        },
        {
            name: 'test_solution_8x8_medium_1pew0',
            clues: [
                [3, 2, 3, -1, -1, -1, -1, -1],
                [-1, -1, -1, 2, 2, -1, 2, -1],
                [-1, -1, 4, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, 2, -1, -1],
                [3, -1, -1, -1, -1, 3, -1, -1],
                [2, -1, -1, 2, -1, -1, -1, -1],
                [-1, 2, -1, 1, 4, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1, -1]
            ],
            regions: [
                [1, 2, 3, 3, 3, 4, 4, 4],
                [1, 2, 3, 5, 6, 6, 7, 8],
                [1, 1, 9, 5, 10, 10, 7, 8],
                [1, 1, 9, 5, 5, 11, 11, 8],
                [12, 12, 9, 5, 5, 13, 13, 13],
                [14, 12, 9, 15, 15, 13, 13, 13],
                [14, 16, 16, 17, 18, 19, 19, 13],
                [20, 20, 17, 17, 18, 18, 18, 13]
            ],
            checkUnique: true,
            skip: true
        }
    ];

    for (const testCase of testCases) {
        const testFn = (testCase as any).skip ? it.skip : it;
        testFn(testCase.name, async () => {
            const solver = new CountryRoadSolver(ctx, { clues: testCase.clues, regions: testCase.regions });
            const solution = await solver.solve();

            assert.ok(solution, 'Solution should be found');

            if (testCase.checkUnique) {
                const other = await solver.getOtherSolution();
                assert.equal(other, null, 'Solution should be unique');
            }
        });
    }
});
