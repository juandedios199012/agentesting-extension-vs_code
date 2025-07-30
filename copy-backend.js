const fs = require('fs');
const path = require('path');

function copyDir(src, dest) {
    if (!fs.existsSync(dest)) {
        fs.mkdirSync(dest, { recursive: true });
    }
    
    const items = fs.readdirSync(src);
    
    for (const item of items) {
        const srcPath = path.join(src, item);
        const destPath = path.join(dest, item);
        
        // Skip __pycache__ directories
        if (item === '__pycache__') {
            continue;
        }
        
        const stat = fs.statSync(srcPath);
        
        if (stat.isDirectory()) {
            copyDir(srcPath, destPath);
        } else {
            fs.copyFileSync(srcPath, destPath);
        }
    }
}

// Copy agent-backend to out/agent-backend
const srcDir = path.join(__dirname, 'agent-backend');
const destDir = path.join(__dirname, 'out', 'agent-backend');

console.log('Copying agent-backend files...');
copyDir(srcDir, destDir);
console.log('Agent-backend files copied successfully!');
