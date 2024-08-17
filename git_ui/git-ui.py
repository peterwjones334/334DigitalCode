import zipfile
import os

# Define the directory structure and files content
project_structure = {
    "index.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Git Command UI</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <h1>Git Command UI</h1>
        <div class="form-group">
            <label for="project-directory">Select Project Directory:</label>
            <input type="file" id="project-directory" webkitdirectory directory multiple>
        </div>
        <div class="form-group">
            <label for="git-command">Select Git Command:</label>
            <select id="git-command">
                <option value="status">git status</option>
                <option value="add">git add .</option>
                <option value="commit">git commit -m</option>
                <option value="push">git push</option>
            </select>
        </div>
        <div class="form-group" id="commit-message-group">
            <label for="commit-message">Commit Message:</label>
            <input type="text" id="commit-message" placeholder="Enter commit message">
        </div>
        <button id="execute-command">Execute Command</button>
        <pre id="output"></pre>
    </div>
    <script src="script.js"></script>
</body>
</html>""",
    "styles.css": """body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.container {
    background: #fff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    width: 400px;
}

h1 {
    text-align: center;
    margin-bottom: 20px;
}

.form-group {
    margin-bottom: 15px;
}

label {
    display: block;
    margin-bottom: 5px;
}

input[type="file"],
input[type="text"],
select {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
}

button {
    width: 100%;
    padding: 10px;
    background: #28a745;
    border: none;
    color: white;
    font-size: 16px;
    cursor: pointer;
    border-radius: 4px;
}

button:hover {
    background: #218838;
}

pre {
    background: #333;
    color: #fff;
    padding: 10px;
    border-radius: 4px;
    margin-top: 20px;
}""",
    "script.js": """document.getElementById('git-command').addEventListener('change', function() {
    const command = this.value;
    const commitMessageGroup = document.getElementById('commit-message-group');
    if (command === 'commit') {
        commitMessageGroup.style.display = 'block';
    } else {
        commitMessageGroup.style.display = 'none';
    }
});

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
});""",
    "server/server.js": """const express = require('express');
const bodyParser = require('body-parser');
const { exec } = require('child_process');
const path = require('path');

const app = express();
const port = 3000;

app.use(bodyParser.json());

app.post('/execute', (req, res) => {
    const { command, directory } = req.body;
    exec(command, { cwd: directory }, (error, stdout, stderr) => {
        if (error) {
            res.status(500).json({ error: stderr });
            return;
        }
        res.json({ output: stdout });
    });
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});"""
}

# Create the zip file
zip_file_path = "/mnt/data/git-command-ui.zip"
with zipfile.ZipFile(zip_file_path, 'w') as zipf:
    for file_name, file_content in project_structure.items():
        # Create directories if they do not exist
        directory = os.path.dirname(file_name)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        # Write the file content to the zip
        zipf.writestr(file_name, file_content)

zip_file_path
