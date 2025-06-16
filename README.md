
# 👨‍💻 Alien Invasion Game — Setup Guide (WSL + Amazon Q CLI)

## 🤖 What is Amazon Q?

**Amazon Q** is an AI-powered developer assistant from AWS that helps you write, understand, and improve code using natural language. You can generate complete functions, debug logic, explain code, and automate AWS infrastructure — all from your terminal or IDE.

### 🔑 Key Features:
- 🧠 Natural language code generation
- 🛠️ Real-time code explanation and debugging
- 🚀 Generate AWS infrastructure as code (IaC)
- 💬 Available via CLI, IDEs (VS Code, JetBrains), and AWS Console

> 💡 It’s like having an AI pair programmer that works with your tools and cloud environment.


This guide helps you:
- Run Ubuntu via WSL
- Set up Amazon Q CLI
- Use Q commands to build your Python game
- Push code to GitHub

---

## 🧑‍💻 Step 1: Install WSL & Amazon Q CLI on Windows

Follow this official AWS guide to install everything you need:

🔗 [The Essential Guide to Installing Amazon Q Developer CLI on Windows](https://community.aws/content/2v5PptEEYT2y0lRmZbFQtECA66M/the-essential-guide-to-installing-amazon-q-developer-cli-on-windows?trk=e07eca93-fa2f-4351-b567-f293b83eb635&sc_channel=el_)

---

## 📦 2. Basic Linux Commands in WSL

| Task              | Command Example       |
| ----------------- | --------------------- |
| View current path | `pwd`                 |
| List files        | `ls`                  |
| Create folder     | `mkdir project`       |
| Move a file       | `mv file.py project/` |
| Remove a file     | `rm filename.py`      |
| Remove folder     | `rm -r folder_name/`  |
| Edit file (nano)  | `nano filename.py`    |

---

## 🤖 3. Amazon Q CLI Commands

### ✅ Setup & Login

Install Amazon Q CLI if not done:
[Install Docs →](https://docs.aws.amazon.com/amazonq/latest/q-cli/q-cli-install.html)

Then in Ubuntu:

```bash
q login
```

Log in using your AWS credentials or browser.

### 🧠 Basic Q Commands

| Command        | Purpose                          |
| -------------- | -------------------------------- |
| `q init`       | Initialize a Q workspace         |
| `q code "..."` | Generate code from prompt        |
| `q ask "..."`  | Ask a question about your code   |
| `q explain`    | Summarize a code block           |
| `q update`     | Update Q CLI to latest version   |
| `q --help`     | See all commands                 |
| `Ctrl + C`     | Exit Q command or stop operation |

> ℹ️ `q quit` does **not exist**, just use `Ctrl + C` to stop or logout manually.

---

## 💡 4. Example Prompt with Q

Generate a Pygame-based shooting game:

```bash
q code "Create a Python Pygame game with:
- Arrow key movement
- Spacebar shooting
- New Game, High Score, Exit menu
- Lives system with 3 hearts
- Win at 250 points"
```

---

## 🧪 5. GitHub: Push Your Code

```bash
# Initialize git
git init

# Add and commit files
git add .
git commit -m "Initial game version"

# Link remote repo
git remote add origin https://github.com/your-username/repo-name.git

# Push
git push -u origin main
```

---

## 🚀 Run the Game Locally

```bash
# Make sure pygame is installed
pip install pygame

# Run the game
python3 alien_invasion.py
```

---

## 🎯 Summary

| Tool     | Purpose                              |
| -------- | ------------------------------------ |
| WSL      | Run Linux in Windows                 |
| Amazon Q | Generate and understand code with AI |
| GitHub   | Version control and backup           |
| Pygame   | Game framework for Python            |

---

## 🙌 Happy Hacking!

Use this setup to build and manage cool Python games faster with the power of Linux + Git + AI!



