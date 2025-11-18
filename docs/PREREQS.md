# Pre-requisites

Have the below installed and verified working (instructions for Windows ↓ Use a privileged power shell terminal).


**GitBash (you probably have this already)**

```
winget install --id Git.Git -e --source winget
```

**VS Code (you probably have this already, too)**

```
winget install --id Microsoft.VisualStudioCode -e
```

**GitHub CLI ("gh"), set up for ssh, not https!**

```
winget install --id GitHub.cli   
gh auth login
```

(Can also use `choco install gh`). During login, choose `SSH` when asked about Git operations. It will walk you through setting up keys etc.

**node.js LTS**

```
winget install OpenJS.NodeJS.LTS -e   
```

(Or manually via https://nodejs.org). During setup, leave "Add to PATH" checked.
   
Restart VS Code and any open shells. We need node, as Claude Code is a Node.js CLI application. 

**Anthropic Claude VS Code extension**

Via VS Code's extension panel.
    
Click the Claude logo to open, then: /login -- select claude.ai account, not API. You need a file open in VS Code for the Anthropic icon to be visible.

**uv**

```
winget install --id=astral-sh.uv -e
```
    
**Python**

```
uv python install 3.12
```

You can also install system-wide via `winget`, but if you already use Python for other things, it may get confusing
    
**Docker**

```
winget install Docker.DockerDesktop 
```

(or manual download via https://docker.com)
    
NB: Reportedly, on Windows 10, Docker Desktop requires WSL2 backend and Hyper-V support; confirm both are enabled:

``` 
wsl --install
```    
then restart. Also reportedly, virtualisation may need to be switched on in the bios.

**Optional: OpenAI Codex VS Code extension**

Via VS Code's extension panel.

**Verification**

```
PS C:\Users\stefan.DYALOG> git --version
git version 2.51.2.windows.1

PS C:\Users\stefan.DYALOG> gh --version
gh version 2.81.0 (2025-10-01)
https://github.com/cli/cli/releases/tag/v2.81.0

PS C:\Users\stefan.DYALOG> uv --version
uv 0.9.5 (d5f39331a 2025-10-21)

PS C:\Users\stefan.DYALOG> python --version
Python 3.12.0 

PS C:\Users\stefan.DYALOG> docker --version
Docker version 27.2.0, build 3ab4256

PS C:\Users\stefan.DYALOG> node --version
v24.10.0
```