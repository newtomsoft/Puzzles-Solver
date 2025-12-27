
// Masyu Solver using Z3 (Low Level API via Emscripten)
// Updated to use correct _Z3_ prefixes and manual constants

async function solveMasyu(gridData) {
    const rows = gridData.length;
    const cols = gridData[0].length;

    // Load Z3
    if (!window.initZ3) {
        console.error("Z3 not loaded");
        return null;
    }

    try {
        const Module = await window.initZ3({
            locateFile: f => f // Expect files in same dir
        });

        // Constants
        const L_TRUE = 1;
        const L_FALSE = -1;
        const L_UNDEF = 0;

        // API Mapping Helper
        // Emscripten exports C functions as _Name
        const api = {
            mk_config: Module._Z3_mk_config,
            del_config: Module._Z3_del_config,
            mk_context: Module._Z3_mk_context,
            del_context: Module._Z3_del_context,
            mk_params: Module._Z3_mk_params,
            del_params: Module._Z3_del_params,
            params_set_bool: Module._Z3_params_set_bool,
            mk_solver: Module._Z3_mk_solver,
            solver_inc_ref: Module._Z3_solver_inc_ref,
            solver_dec_ref: Module._Z3_solver_dec_ref,
            mk_int_sort: Module._Z3_mk_int_sort,
            mk_bool_sort: Module._Z3_mk_bool_sort,
            mk_string_symbol: Module._Z3_mk_string_symbol,
            mk_const: Module._Z3_mk_const,
            mk_int: Module._Z3_mk_int,
            mk_eq: Module._Z3_mk_eq,
            mk_not: Module._Z3_mk_not,
            mk_add: Module._Z3_mk_add,
            mk_mul: Module._Z3_mk_mul,
            mk_sub: Module._Z3_mk_sub,
            mk_le: Module._Z3_mk_le,
            mk_ge: Module._Z3_mk_ge,
            mk_lt: Module._Z3_mk_lt,
            mk_gt: Module._Z3_mk_gt,
            mk_and: Module._Z3_mk_and,
            mk_or: Module._Z3_mk_or,
            mk_implies: Module._Z3_mk_implies,
            mk_true: Module._Z3_mk_true,
            mk_false: Module._Z3_mk_false,
            solver_assert: Module._Z3_solver_assert,
            solver_check: Module._Z3_solver_check,
            solver_get_model: Module._Z3_solver_get_model,
            model_inc_ref: Module._Z3_model_inc_ref,
            model_dec_ref: Module._Z3_model_dec_ref,
            model_eval: Module._Z3_model_eval,
            is_eq_ast: Module._Z3_is_eq_ast,
            get_numeral_int: Module._Z3_get_numeral_int,

            // Memory management for arrays
            // We need to allocate arrays for mk_and, mk_or, mk_add
            // Emscripten provides stackAlloc, HEAP32, etc. or we can use malloc
        };

        // Initialize Context
        const cfg = api.mk_config();
        const ctx = api.mk_context(cfg);
        api.del_config(cfg);

        // Array Allocation Helper
        // Z3 array functions take (ctx, count, array_ptr)
        // We need to convert JS array of pointers to C array
        function allocPtrArray(pointers) {
            const bytes = pointers.length * 4;
            const ptr = Module._malloc(bytes);
            const heap = new Uint32Array(Module.HEAPU32.buffer, ptr, pointers.length);
            for (let i = 0; i < pointers.length; i++) {
                heap[i] = pointers[i];
            }
            return ptr;
        }

        function freePtrArray(ptr) {
            Module._free(ptr);
        }

        // Wrappers
        function mkInt(name) {
            // string symbol needs C string
            const nameLen = Module.lengthBytesUTF8(name) + 1;
            const namePtr = Module._malloc(nameLen);
            Module.stringToUTF8(name, namePtr, nameLen);
            const sym = api.mk_string_symbol(ctx, namePtr);
            Module._free(namePtr);

            const intSort = api.mk_int_sort(ctx);
            return api.mk_const(ctx, sym, intSort);
        }

        function mkIntVal(val) {
            const intSort = api.mk_int_sort(ctx);
            return api.mk_int(ctx, val, intSort);
        }

        function Eq(a, b) { return api.mk_eq(ctx, a, b); }
        function Or(list) {
            if (list.length === 0) return api.mk_false(ctx);
            if (list.length === 1) return list[0];
            const ptr = allocPtrArray(list);
            const res = api.mk_or(ctx, list.length, ptr);
            freePtrArray(ptr);
            return res;
        }
        function And(list) {
            if (list.length === 0) return api.mk_true(ctx);
            if (list.length === 1) return list[0];
            const ptr = allocPtrArray(list);
            const res = api.mk_and(ctx, list.length, ptr);
            freePtrArray(ptr);
            return res;
        }
        function Add(list) {
            if (list.length === 0) return mkIntVal(0);
            if (list.length === 1) return list[0];
            const ptr = allocPtrArray(list);
            const res = api.mk_add(ctx, list.length, ptr);
            freePtrArray(ptr);
            return res;
        }
        function Not(a) { return api.mk_not(ctx, a); }
        function Implies(a, b) { return api.mk_implies(ctx, a, b); }

        const zero = mkIntVal(0);
        const one = mkIntVal(1);
        const two = mkIntVal(2);

        const solver = api.mk_solver(ctx);
        api.solver_inc_ref(ctx, solver);

        // Variables
        const h = [];
        const v = [];

        for (let r = 0; r < rows; r++) {
            const rowH = [];
            for (let c = 0; c < cols - 1; c++) {
                const edge = mkInt(`h_${r}_${c}`);
                rowH.push(edge);
                api.solver_assert(ctx, solver, Or([Eq(edge, zero), Eq(edge, one)]));
            }
            h.push(rowH);
        }

        for (let r = 0; r < rows - 1; r++) {
            const rowV = [];
            for (let c = 0; c < cols; c++) {
                const edge = mkInt(`v_${r}_${c}`);
                rowV.push(edge);
                api.solver_assert(ctx, solver, Or([Eq(edge, zero), Eq(edge, one)]));
            }
            v.push(rowV);
        }

        function getEdges(r, c) {
            const edges = [];
            edges.push((r > 0) ? v[r - 1][c] : zero); // Up
            edges.push((r < rows - 1) ? v[r][c] : zero); // Down
            edges.push((c > 0) ? h[r][c - 1] : zero); // Left
            edges.push((c < cols - 1) ? h[r][c] : zero); // Right
            return edges;
        }

        // Constraints
        for (let r = 0; r < rows; r++) {
            for (let c = 0; c < cols; c++) {
                const edges = getEdges(r, c); // [up, down, left, right]
                const sumDeg = Add(edges);
                const cell = gridData[r][c];

                if (cell === 'w' || cell === 'b') {
                    api.solver_assert(ctx, solver, Eq(sumDeg, two));
                } else {
                    api.solver_assert(ctx, solver, Or([Eq(sumDeg, zero), Eq(sumDeg, two)]));
                }

                const [up, down, left, right] = edges;

                if (cell === 'b') {
                    // Must turn
                    api.solver_assert(ctx, solver, Not(And([Eq(up, one), Eq(down, one)])));
                    api.solver_assert(ctx, solver, Not(And([Eq(left, one), Eq(right, one)])));

                    // Extend legs
                    if (r > 1) api.solver_assert(ctx, solver, Implies(Eq(up, one), Eq(v[r - 2][c], one)));
                    if (r < rows - 2) api.solver_assert(ctx, solver, Implies(Eq(down, one), Eq(v[r + 1][c], one)));
                    if (c > 1) api.solver_assert(ctx, solver, Implies(Eq(left, one), Eq(h[r][c - 2], one)));
                    if (c < cols - 2) api.solver_assert(ctx, solver, Implies(Eq(right, one), Eq(h[r][c + 1], one)));
                }
                else if (cell === 'w') {
                    // Must straight
                    const isVert = And([Eq(up, one), Eq(down, one)]);
                    const isHorz = And([Eq(left, one), Eq(right, one)]);
                    api.solver_assert(ctx, solver, Or([isVert, isHorz]));

                    // Turn at neighbor
                    let turnUp = (r > 1) ? Eq(v[r - 2][c], zero) : api.mk_true(ctx);
                    let turnDown = (r < rows - 2) ? Eq(v[r + 1][c], zero) : api.mk_true(ctx);
                    api.solver_assert(ctx, solver, Implies(isVert, Or([turnUp, turnDown])));

                    let turnLeft = (c > 1) ? Eq(h[r][c - 2], zero) : api.mk_true(ctx);
                    let turnRight = (c < cols - 2) ? Eq(h[r][c + 1], zero) : api.mk_true(ctx);
                    api.solver_assert(ctx, solver, Implies(isHorz, Or([turnLeft, turnRight])));
                }
            }
        }

        // Loop
        while (api.solver_check(ctx, solver) === L_TRUE) {
            const model = api.solver_get_model(ctx, solver);
            api.model_inc_ref(ctx, model);

            // Read solution
            const hRes = [];
            const vRes = [];
            let hasEdges = false;

            const edgesList = [];

            // We need a pointer to store result of model_eval
            const astPtrBuf = Module._malloc(4);

            for (let r = 0; r < rows; r++) {
                const row = [];
                for (let c = 0; c < cols - 1; c++) {
                    const ast = h[r][c];
                    // model_eval returns bool success, and writes output to pointer
                    // Standard C: Z3_bool Z3_model_eval(Z3_context c, Z3_model m, Z3_ast t, Z3_bool model_completion, Z3_ast * v);
                    const success = api.model_eval(ctx, model, ast, 1, astPtrBuf);
                    let val = 0;
                    if (success) {
                        // Read the output AST
                        const valAst = Module.getValue(astPtrBuf, 'i32');
                        // Check if equal to One
                        if (api.is_eq_ast(ctx, valAst, one)) val = 1;
                    }
                    row.push(val);
                    if (val === 1) {
                        edgesList.push({r1:r, c1:c, r2:r, c2:c+1, ast: ast});
                        hasEdges = true;
                    }
                }
                hRes.push(row);
            }

            for (let r = 0; r < rows - 1; r++) {
                const row = [];
                for (let c = 0; c < cols; c++) {
                    const ast = v[r][c];
                    const success = api.model_eval(ctx, model, ast, 1, astPtrBuf);
                    let val = 0;
                    if (success) {
                        const valAst = Module.getValue(astPtrBuf, 'i32');
                        if (api.is_eq_ast(ctx, valAst, one)) val = 1;
                    }
                    row.push(val);
                    if (val === 1) {
                        edgesList.push({r1:r, c1:c, r2:r+1, c2:c, ast: ast});
                        hasEdges = true;
                    }
                }
                vRes.push(row);
            }

            Module._free(astPtrBuf);
            api.model_dec_ref(ctx, model);

            if (!hasEdges) {
                return { h: hRes, v: vRes };
            }

            // Connectivity
            const adj = new Map();
            const addAdj = (k1, k2) => {
                if(!adj.has(k1)) adj.set(k1, []);
                if(!adj.has(k2)) adj.set(k2, []);
                adj.get(k1).push(k2);
                adj.get(k2).push(k1);
            };

            for (const e of edgesList) {
                addAdj(`${e.r1},${e.c1}`, `${e.r2},${e.c2}`);
            }

            const nodes = Array.from(adj.keys());
            if (nodes.length === 0) return { h: hRes, v: vRes };

            const visited = new Set();
            const q = [nodes[0]];
            visited.add(nodes[0]);

            while (q.length > 0) {
                const curr = q.pop();
                for (const n of (adj.get(curr)||[])) {
                    if (!visited.has(n)) {
                        visited.add(n);
                        q.push(n);
                    }
                }
            }

            if (visited.size === nodes.length) {
                api.solver_dec_ref(ctx, solver);
                api.del_context(ctx);
                return { h: hRes, v: vRes };
            }

            // Subtour elimination
            const componentEdges = [];
            for(const e of edgesList) {
                const k1 = `${e.r1},${e.c1}`;
                const k2 = `${e.r2},${e.c2}`;
                if (visited.has(k1) && visited.has(k2)) {
                    componentEdges.push(Eq(e.ast, one));
                }
            }

            if (componentEdges.length > 0) {
                api.solver_assert(ctx, solver, Not(And(componentEdges)));
            } else {
                break;
            }
        }

        api.solver_dec_ref(ctx, solver);
        api.del_context(ctx);
        return null;

    } catch (e) {
        console.error("Z3 Error", e);
        return null;
    }
}

window.solveMasyu = solveMasyu;
