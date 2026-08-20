const fs = require('fs');

function buildPage(contentFile, outputFile) {
    const header = fs.readFileSync('partials/header.html', 'utf8');
    const footer = fs.readFileSync('partials/footer.html', 'utf8');
    const content = fs.readFileSync(contentFile, 'utf8');
    const result = header.replace('{{title}}', 'Your Page Title') + content + footer;
    fs.writeFileSync(outputFile, result);
}

buildPage('content-index.html', 'index.html');
buildPage('content-about.html', 'about.html');
// etc.