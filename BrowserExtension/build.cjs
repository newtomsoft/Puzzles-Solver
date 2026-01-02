const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const browser = process.argv.find(arg => arg.startsWith('--browser='))?.split('=')[1] || 'chrome';
const distDir = path.join(__dirname, 'dist', browser);

console.log(`Building for ${browser}...`);

// 1. Clean dist
if (!fs.existsSync(path.join(__dirname, 'dist'))) {
    fs.mkdirSync(path.join(__dirname, 'dist'));
}
if (fs.existsSync(distDir)) {
    fs.rmSync(distDir, { recursive: true, force: true });
}
fs.mkdirSync(distDir);

// 2. Run TSC
console.log(`Compiling TypeScript for ${browser}...`);
try {
    execSync(`npx tsc --outDir "${distDir}"`, { stdio: 'inherit' });
} catch (e) {
    console.error('TypeScript compilation failed.');
    process.exit(1);
}

// 3. Copy static assets
const assets = [
    'popup.html',
    'libs',
    'icons'
];

// Helper to copy file or directory
function copyRecursiveSync(src, dest) {
    const exists = fs.existsSync(src);
    const stats = exists && fs.statSync(src);
    if (stats && stats.isDirectory()) {
        if (!fs.existsSync(dest)) fs.mkdirSync(dest);
        fs.readdirSync(src).forEach(childItemName => {
            copyRecursiveSync(path.join(src, childItemName), path.join(dest, childItemName));
        });
    } else if (exists) {
        fs.copyFileSync(src, dest);
    } else {
        console.warn(`Warning: Asset ${src} not found.`);
    }
}

console.log('Copying assets...');
assets.forEach(asset => {
    const srcPath = path.join(__dirname, asset);
    const destPath = path.join(distDir, asset);
    if (fs.existsSync(srcPath)) {
        copyRecursiveSync(srcPath, destPath);
    } else {
        console.warn(`Warning: Asset ${srcPath} not found.`);
    }
});
// Special handling for manifest
const manifestSrc = path.join(__dirname, `manifest.${browser}.json`);
if (fs.existsSync(manifestSrc)) {
    fs.copyFileSync(manifestSrc, path.join(distDir, 'manifest.json'));
} else {
    // Fallback to default manifest.json if specific one doesn't exist
    fs.copyFileSync(path.join(__dirname, 'manifest.json'), path.join(distDir, 'manifest.json'));
}

console.log(`Build complete! Output in ./dist/${browser}`);
