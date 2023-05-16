// only following file extensions are processed
const languages = { 'py': 'Python', 'java': 'Java', 'js': 'JavaScript', 'cpp': 'C++' };
const fs = require('fs');
const { execSync } = require('child_process');
const files = '${{ steps.diff.outputs.files }}'.split('\n');
console.log('*** files: ' + `${files}`);
for (const file of files) {
    const headExist = fs.existsSync(`head/${file}`) ? true : false;
    console.log('*** ' + `${file}` + ' exist in head is: ' + `${headExist}`)
    const baseExist = fs.existsSync(`base/${file}`) ? true : false;
    console.log('*** ' + `${file}` + ' exist in base is: ' + `${baseExist}`)
    if (fs.existsSync(`head/${file}`)) {  // check if file exists in head
        console.log('*** processing file ' + `${file}` + '.');
        const fileModified = (fs.existsSync(`base/${file}`)) ? true : false // check if file is new
        const fileExtension = file.split('.').pop();  // get file extension 
        if (languages.hasOwnProperty(fileExtension)) { // check if source code
            language = languages[fileExtension]
            const headContent = fs.existsSync(`head/${file}`) ? fs.readFileSync(`head/${file}`, 'utf8') : '';
            if (fileModified == true) {
                const baseContent = fs.existsSync(`base/${file}`) ? fs.readFileSync(`base/${file}`, 'utf8') : '';
                const diff = execSync(`diff -u base/${file} head/${file}`, { encoding: 'utf8' });
                const result = execSync(`OPENAI_API_KEY='${OPENAI_API_KEY}' python3 head/chatgpt_agent.py MODIFIED '${baseContent}' '${diff}' '${language}'`, { encoding: 'utf8' });
            } else { // file added
                const result = execSync(`OPENAI_API_KEY='${OPENAI_API_KEY}' python3 head/chatgpt_agent.py ADDED '${headContent}' '' '${language}'`, { encoding: 'utf8' });
            }
            github.issues.createComment({
                issue_number: context.issue.number,
                owner: context.repo.owner,
                repo: context.repo.repo,
                body: `Results for ${file}:\n\n${result}`
            });
            console.log('*** comments for ' + `${file}` + ' created.');
        }
    } else {
        console.log('*** no comments for ' + `${file}` + ' created.');
    }
}