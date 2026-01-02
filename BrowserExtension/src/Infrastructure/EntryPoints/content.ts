const hasCanvas = !!document.querySelector('canvas');
const hasGpl = Array.from(document.scripts).some(s => s.textContent && s.textContent.includes('gpl'));

if (hasCanvas && hasGpl) {
    const title = document.querySelector('h1');
    if (title) {
        const btn = document.createElement('button');
        btn.textContent = 'Solve Puzzle';
        btn.style.marginLeft = '10px';
        btn.onclick = async () => {
            btn.textContent = 'Solving...';
            try {
                const html = document.documentElement.outerHTML;
                const response = await chrome.runtime.sendMessage({ action: 'SOLVE', html, url: window.location.href });
                if (response.success) {
                    btn.textContent = 'Solved!';
                    drawSolution(response.solutionPath, response.blackCells, response.rows);
                } else {
                    btn.textContent = 'Failed';
                    alert('Solver failed: ' + response.error);
                }
            } catch (e: any) {
                btn.textContent = 'Error';
                console.error(e);
                alert('Error: ' + e.message);
            }
        };
        title.appendChild(btn);
    }
}

function drawSolution(path: any[], blackCells: any[], rows: number) {
    const script = document.createElement('script');
    script.textContent = `
        (${playLogic.toString()})(${JSON.stringify(path)}, ${JSON.stringify(blackCells)}, ${rows});
    `;
    document.head.appendChild(script);
    script.remove();
}

const playLogic = async (p: any[], bl: any[], size: number) => {
    const canvas = document.querySelector('canvas');
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const cellW = rect.width / size;
    const cellH = rect.height / size;
    const sim = (x: number, y: number, type: string, buttons: number = 0) => {
        const common = { bubbles: true, cancelable: true, clientX: x, clientY: y, screenX: x, screenY: y, button: 0, buttons: buttons, view: window };
        canvas.dispatchEvent(new PointerEvent(type.replace('mouse', 'pointer'), { ...common, pointerId: 1, isPrimary: true, pressure: buttons ? 0.5 : 0 }));
        canvas.dispatchEvent(new MouseEvent(type, common));
    };

    for (const b of bl) {
        const x = rect.left + cellW / 2 + b.c * cellW;
        const y = rect.top + cellH / 2 + b.r * cellH;
        sim(x, y, 'mousedown', 1);
        sim(x, y, 'mouseup', 0);
        await new Promise(r => setTimeout(r, 100));
    }

    if (p.length > 1) {
        const start = p[0];
        sim(rect.left + cellW / 2 + start.c * cellW, rect.top + cellH / 2 + start.r * cellH, 'mousedown', 1);
        for (let i = 0; i < p.length - 1; i++) {
            const next = p[i + 1];
            sim(rect.left + cellW / 2 + next.c * cellW, rect.top + cellH / 2 + next.r * cellH, 'mousemove', 1);
            await new Promise(r => setTimeout(r, 60));
        }
        const end = p[p.length - 1];
        sim(rect.left + cellW / 2 + end.c * cellW, rect.top + cellH / 2 + end.r * cellH, 'mouseup', 0);
    }
};
