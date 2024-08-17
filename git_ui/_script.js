document.getElementById('git-command').addEventListener('change', function() {
    const command = this.value;
    const commitMessageGroup = document.getElementById('commit-message-group');
    if (command === 'commit') {
        commitMessageGroup.style.display = 'block';
    } else {
        commitMessageGroup.style.display = 'none';
    }
});

document.getElementById('execute-command').addEventListener('click', function() {
    const directory = document.getElementById('project-directory').files[0];
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
    outputElement.textContent = `Executing: ${fullCommand} in ${directory.path}`;

    // Placeholder for executing the command
    // Here you would use a backend service to execute the Git command and return the output
    // Example: fetch('/execute', { method: 'POST', body: JSON.stringify({ command: fullCommand, directory: directory.path }) });

    // Simulating output for demonstration purposes
    setTimeout(() => {
        outputElement.textContent += `\n\nOutput:\nCommand executed successfully!`;
    }, 2000);
});
