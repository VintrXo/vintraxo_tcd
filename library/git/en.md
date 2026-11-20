# @lesson git-intro
title: Git introduction
summary: What version control is, and why every programmer uses it.
---
**Git** is a version control system: it saves "snapshots" of your project whenever you ask, so you can go back to any earlier version, see who changed what and when, and work with a team on the same files without anyone wiping out someone else's work.

## Key ideas

- **Repository**: your project folder with its full history.
- **Commit**: a saved snapshot of the files, with a message explaining the change.
- **Branch**: a separate line of work where you experiment without touching the original.
- **Remote**: a copy of the repository on a server such as GitHub or GitLab.

:::info Git and GitHub
**Git** is the program on your computer. **GitHub** is a website that hosts repositories so you can share them. Alternatives include GitLab and Bitbucket.
:::

```quiz
? What is a commit in Git?
- A new file
* A saved snapshot of the project with a message
- A server on the internet

? GitHub is the same thing as the Git program.
= false
> Git is a program on your computer; GitHub is a website that hosts repositories.
```

# @lesson git-config
title: Installing and setting up
summary: Installing Git and setting your name and e-mail.
---
## Installing

- **Windows**: download *Git for Windows* from the official site git-scm.com.
- **Mac**: type `git --version` in the terminal and it offers to install it.
- **Linux**: `sudo apt install git` on Ubuntu.

Check the installation:

```bash
git --version
```

## Introduce yourself

Every commit records your name and e-mail, so set them once:

```bash
git config --global user.name "Sara Ahmed"
git config --global user.email "sara@example.com"
git config --global init.defaultBranch main
git config --list
```

```exercise bash
? Complete the command to set your e-mail
git config --global user.___ "me@example.com"
= email
```

```quiz
? What does the --global option do?
* Applies the setting to all your repositories
- Uploads the setting to GitHub
- Deletes the old setting

? Your name and e-mail are recorded in every commit.
= true
```

# @lesson git-init
title: Creating a repository
summary: git init, git status, and Git's three areas.
---
Go into your project folder and create a repository:

```bash
mkdir my-site
cd my-site
git init
git status
```

`git init` creates a hidden folder named `.git` that keeps the whole history, and `git status` tells you the state of your files at any time.

## The three areas

1. **Working folder**: your files as you edit them.
2. **Staging area**: what you chose to go into the next commit.
3. **Repository**: the saved commits.

Files move between them with commands: `git add` to staging, and `git commit` to the repository.

:::tip Use git status often
Before and after any command, `git status` shows you what changed and what is ready to be saved.
:::

```quiz
? Which command creates a new Git repository?
* git init
- git start
- git new

? The hidden .git folder keeps the repository's history.
= true
```

# @lesson git-commit
title: Saving: add and commit
summary: Staging files and saving commits with clear messages.
---
```bash
echo "<h1>Hello</h1>" > index.html
git status
git add index.html
git commit -m "Add the home page"
```

- `git add file` stages a file; `git add .` stages every change.
- `git commit -m "message"` saves the commit.

## A good commit message

- Short and clear: **what** changed and **why**.
- In the imperative: "Add the contact form" is better than "changed stuff".
- One commit per logical change, not one huge commit for everything.

:::warning Never commit passwords
Do not add files with passwords or keys to the repository. If one reaches GitHub, treat it as leaked and change it at once.
:::

```exercise bash
? Complete the command to stage every changed file
git add ___
= .
```

```quiz
? In what order do you save a change?
* git add, then git commit
- git commit, then git add
- Only git save

? git commit -m saves the commit with a message.
= true
```

# @lesson git-log-diff
title: History and differences
summary: git log, git diff and git show.
---
```bash
git log
git log --oneline
git log --oneline --graph --all
```

Every commit has an **id** (hash) such as `a1b2c3d`.

## What changed?

```bash
git diff              # changes not staged yet
git diff --staged     # what goes into the next commit
git show a1b2c3d      # details of one commit
```

```reference bash
git log | Commit history | git log -5
git log --oneline | One line per commit | git log --oneline
git log -- file | History of one file | git log -- index.html
git diff | Unstaged differences | git diff
git diff --staged | Staged differences | git diff --staged
git show | Details of a commit | git show HEAD
git blame | Who wrote each line | git blame index.html
```

```quiz
? Which command shows each commit on one line?
- git log --short
* git log --oneline
- git show --all

? git diff --staged shows the changes ready for the next commit.
= true
```

# @lesson git-undo
title: Undoing things
summary: restore, reset, revert and amend.
---
## Before committing

```bash
git restore index.html           # throw away your edits to the file
git restore --staged index.html  # take the file out of staging
```

## Changing the last commit

```bash
git commit --amend -m "A clearer message"
```

## Undoing a shared commit

`git revert` creates a new commit that reverses an old one, so history is not erased:

```bash
git revert a1b2c3d
```

## reset

`git reset` moves the branch back to an earlier commit:

```bash
git reset --soft HEAD~1   # undo the last commit, keep the changes staged
git reset --hard HEAD~1   # undo the last commit and erase the changes
```

:::danger Careful with reset --hard
It erases changes for good. And never `reset` commits you have shared with others; use `revert` instead.
:::

```quiz
? Which command undoes a shared commit without erasing history?
- git reset --hard
* git revert
- git restore

? git commit --amend changes the last commit.
= true
```

# @lesson git-ignore
title: The .gitignore file
summary: Keeping out the files that do not belong in the repository.
---
Some files should never be saved: temporary files, libraries that can be downloaded again, settings with passwords. Write their patterns in a `.gitignore` file at the project root:

```text
# libraries
node_modules/
__pycache__/

# environment files and secrets
.env
*.key

# system and editor files
.DS_Store
.vscode/

# log files
*.log
```

- `*` matches any characters: `*.log` is every log file.
- A trailing `/` means a folder.
- `!` makes an exception: `!important.log`.

:::warning A file already committed
`.gitignore` does not affect a file already in the repository. Take it out first: `git rm --cached .env`.
:::

```exercise bash
? Complete the pattern to ignore every log file
___.log
= *
```

```quiz
? Where does the .gitignore file usually go?
* At the project root
- Inside the .git folder
- Only on GitHub

? .gitignore automatically removes a file that was already committed.
= false
```

# @lesson git-branches
title: Branches
summary: Creating branches and moving between them.
---
A **branch** lets you work on a new feature without touching the stable version in `main`:

```bash
git branch                    # list branches
git switch -c contact-form    # create a branch and move to it
# ... edit and commit ...
git add .
git commit -m "Add the contact form"
git switch main               # back to the main branch
```

```reference bash
git branch | List branches | git branch
git branch name | Create a branch | git branch fix-login
git switch name | Move to a branch | git switch fix-login
git switch -c name | Create and move | git switch -c new-page
git branch -d name | Delete a merged branch | git branch -d fix-login
git branch -m new | Rename the branch | git branch -m main
```

:::tip One branch per task
Give each feature or fix a branch with a clear name such as `fix-login-error`; that way `main` is always ready to deploy.
:::

```exercise bash
? Create a branch called new-page and move to it
git switch ___ new-page
= -c
```

```quiz
? Which command moves you to an existing branch?
* git switch
- git move
- git go

? Working in a new branch does not change main until you merge it.
= true
```

# @lesson git-merge
title: Merging
summary: Merging a branch into main, fast-forward and merge commits.
---
When the feature is done, merge its branch into `main`:

```bash
git switch main
git merge contact-form
git branch -d contact-form
```

## Two kinds of merge

- **Fast-forward**: if `main` has not changed since the branch was created, `main` simply moves up to the branch's last commit.
- **Merge commit**: if both branches changed, Git creates a new commit that joins them.

```bash
git log --oneline --graph --all
```

shows the branches and merges as a graph.

```quiz
? Where are you when you type git merge contact-form?
* On the branch you want to merge into (such as main)
- On the branch contact-form
- It does not matter

? A fast-forward merge does not create a merge commit.
= true
```

# @lesson git-conflicts
title: Resolving conflicts
summary: Why conflicts happen and how to resolve them step by step.
---
A **conflict** happens when two branches change the same line in two different ways, and Git cannot tell which one to keep:

```text
<<<<<<< HEAD
<h1>Welcome</h1>
=======
<h1>Hello, visitors</h1>
>>>>>>> new-title
```

- Between `<<<<<<< HEAD` and `=======` is your current version.
- Between `=======` and `>>>>>>>` is the other branch's version.

## Steps to resolve

1. Open the file and pick the right version, or combine them.
2. Delete the `<<<<<<<`, `=======` and `>>>>>>>` markers.
3. Save, then:

```bash
git add index.html
git commit
```

To cancel and go back to before the merge: `git merge --abort`.

:::tip Fewer conflicts
Merge `main` into your branch often, keep branches short-lived, and talk with your team about the files you are working on.
:::

```quiz
? What do you do after fixing the conflicted file?
- git merge again
* git add, then git commit
- git reset --hard

? git merge --abort cancels the merge and takes you back to before it.
= true
```

# @lesson git-remote
title: GitHub and remote repositories
summary: clone, push, pull and fetch.
---
## Copying an existing repository

```bash
git clone https://github.com/user/project.git
```

## Linking your local repository to GitHub

After creating an empty repository on GitHub:

```bash
git remote add origin https://github.com/user/my-site.git
git push -u origin main
```

## Daily syncing

```bash
git pull           # fetch others' changes and merge them
git push           # upload your commits
git fetch          # fetch changes without merging
```

```reference bash
git clone | Copy a repository | git clone URL
git remote -v | List remotes | git remote -v
git remote add | Add a remote | git remote add origin URL
git push | Upload commits | git push origin main
git pull | Fetch and merge | git pull
git fetch | Fetch without merging | git fetch origin
```

:::info The name origin
`origin` is the usual name for the main remote repository. You can name it as you like, but this name is the convention.
:::

```exercise bash
? Upload your commits to the main branch on origin
git ___ origin main
= push
```

```quiz
? What is the difference between git fetch and git pull?
* fetch only downloads; pull downloads and merges
- There is no difference
- pull uploads and fetch downloads

? git clone copies a remote repository to your computer.
= true
```

# @lesson git-workflow
title: Working in a team
summary: Branches, pull requests and code review.
---
The common workflow on GitHub:

1. Update `main`: `git switch main`, then `git pull`.
2. Create a branch for the task: `git switch -c fix-cart-total`.
3. Work and save small, clear commits.
4. Upload the branch: `git push -u origin fix-cart-total`.
5. Open a **Pull Request** on GitHub.
6. Your colleagues review the code and comment; you change it and push again.
7. Once approved, the request is merged into `main` and you delete the branch.

## Fork

For a project you cannot write to (an open-source project, for example): copy it to your account with **Fork**, work on it, then open a pull request to the original project.

:::tip Code review
A small pull request is reviewed quickly and carefully. In its description, say what changed, why, and how to try it.
:::

```quiz
? What is a Pull Request?
- A command that fetches changes
* A request to merge your branch after review
- A backup

? You use a Fork to contribute to a project you cannot write to.
= true
```

# @lesson git-reference
title: Git reference
summary: The most important commands with an example for each.
type: Reference
---
Search the table for any command.

```reference bash
git init | Create a repository | git init
git clone | Copy a repository | git clone URL
git status | State of the files | git status
git add | Stage changes | git add .
git commit | Save a commit | git commit -m "message"
git log | History | git log --oneline
git diff | Differences | git diff --staged
git show | Details of a commit | git show HEAD
git restore | Throw away edits | git restore file
git reset | Move the branch back | git reset --soft HEAD~1
git revert | Reverse a commit | git revert a1b2c3d
git branch | Branches | git branch -d old
git switch | Move between branches | git switch -c new
git merge | Merge | git merge feature
git stash | Put work aside | git stash / git stash pop
git remote | Remote repositories | git remote -v
git push | Upload | git push -u origin main
git pull | Fetch and merge | git pull
git fetch | Fetch only | git fetch
git tag | Tag a release | git tag v1.0.0
git config | Settings | git config --global user.name "…"
```

:::tip What next?
Create a repository for one of your projects from the earlier courses, push it to GitHub, and try a branch and a pull request.
:::
