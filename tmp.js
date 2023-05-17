const languages = { 'py': 'Python', 'java': 'Java', 'js': 'JavaScript', 'cpp': 'C++' };
const fs = require('fs');
const { execFileSync } = require('child_process');
const files = '${{ steps.diff.outputs.files }}'.split('\n');
const comments = [];

for (const file of files) {
    const headFilePath = `head/${file}`;
    const baseFilePath = `base/${file}`;
    const fileExistsInHead = fs.existsSync(headFilePath);
    const fileModified = fs.existsSync(baseFilePath);

    if (fileExistsInHead) {
        console.log(`+++ processing file ${file}.`);

        const fileExtension = file.split('.').pop();
        if (languages.hasOwnProperty(fileExtension)) {
            const language = languages[fileExtension];
            const headContent = fs.readFileSync(headFilePath, 'utf8');
            let result = "";

            if (fileModified) {
                const baseContent = fs.existsSync(baseFilePath) ? fs.readFileSync(baseFilePath, 'utf8') : '';

                try {
                    const diff = execFileSync('diff', ['-u', baseFilePath, headFilePath], { encoding: 'utf8' });
                    result = execFileSync('python3', ['head/chatgpt_agent.py', 'MODIFIED', baseContent, diff, language], {
                        encoding: 'utf8',
                        env: {
                            OPENAI_API_KEY: process.env.OPENAI_API_KEY
                        }
                    });
                } catch (err) {
                    console.error(`Error: ${err}`);
                }
            } else {
                try {
                    result = execFileSync('python3', ['head/chatgpt_agent.py', 'ADDED', headContent, '', language], {
                        encoding: 'utf8',
                        env: {
                            OPENAI_API_KEY: process.env.OPENAI_API_KEY
                        }
                    });
                } catch (err) {
                    console.error(`Error: ${err}`);
                }
            }

            console.log(`+++ result: ${result}`);

            await github.rest.issues.createComment({
                issue_number: context.issue.number,
                owner: context.repo.owner,
                repo: context.repo.repo,
                body: `Results for ${file}:\n\n${result}`
            });

            console.log(`*** comments for ${file} created.`);

            comments.push(`ChatGPT code comment on file: ${file}:\n\n${result}`);
        }
    } else {
        console.log(`*** no comments for ${file} created.`);
    }
}