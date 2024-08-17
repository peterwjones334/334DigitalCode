document.getElementById('execute-command').addEventListener('click', function() {
    const directory = document.getElementById('project-directory').files[0].path;
    const command = document.getElementById('git-command').value;
    let fullCommand = '';

    switch (command) {
        case 'status':
            fullCommand = 'git status';
            break;
        case 'add':
            fullCommand = 'git add .';
            break;
        case 'commit':
            const commitMessage = document.getElementById('commit-message').value;
            fullCommand = `git commit -m "${commitMessage}"`;
            break;
        case 'push':
            fullCommand = 'git push';
            break;
    }

    const outputElement = document.getElementById('output');
    outputElement.textContent = `Executing: ${fullCommand} in ${directory}`;

    fetch('http://localhost:3000/execute', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ command: fullCommand, directory: directory })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            outputElement.textContent += `\n\nError:\n${data.error}`;
        } else {
            outputElement.textContent += `\n\nOutput:\n${data.output}`;
        }
    })
    .catch(error => {
        outputElement.textContent += `\n\nError:\n${error}`;
    });
});
