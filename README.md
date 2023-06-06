<img src="./assets/icon.png" width=200 align="right">

# Miirakuru

[![License](https://img.shields.io/github/license/nattadasu/miirakuru?logo=github)](LICENSE)

Easily sync your MAL to several supported sites via Discord, only for self-host!

## About

Miirakuru (Japanese: ミイラクル, wordplay of Miracle「ミラクル」and Mummy「ミイラ」) is a Discord bot that assist you in tracking your currently watching anime to MyAnimeList directly from Discord. It also able to sync to multiple platforms thanks to [AnimeAPI](https://github.com/nattadasu/animeApi).

Build with [interactions.py](https://pypi.org/project/discord-py-interactions/), this bot uses slash command (`/`) as main interface to the software instead of prefixed/text command.

Miirakuru **does not** have invitable link, and anyone who interested using it must self-host this bot instead.

## Set-Up

### Prerequisites

Before installing and running the software, you must have those required packages/apps to be installed first:

1. [Git](https://git-scm.com)
2. [Python 3.10](https://www.python.org) or greater

Additionally, you can install [`pipenv`](https://github.com/pypa/pipenv) as dependency manager instead of using `virtualenv` and `pip`.

## Cloning and Installing Required Packages

1. To make the software available on your machine, open Terminal and write as following:

   ```bash
   git clone https://github.com/nattadasu/miirakuru.git
   cd miirakuru
   ```
   
   Or, using [GitHub CLI](https://github.com/cli/cli):
   
   ```bash
   gh repo clone nattadasu/miirakuru
   cd miirakuru
   ```

2. Depending which dependency manager you use, install required packages
   * Using `pipenv`:

     ```ps1
     pipenv install
     ```

   * Using `virtualenv` and `pip`:
     ```ps1
     python -m venv venv
     # depending on what OS and shell:
     # bash:
     source ./venv/bin/activate
     # PowerShell, Windows:
     #   & ./venv/Scripts/activate.ps1
     # PowerShell, *nix:
     #   & ./venv/bin/activate.ps1
     pip install -U -r requirements.txt
     ```

3. Copy `.env.example` as `.env`, and fill all fields

4. Run the software
   * Using `pipenv`:
     ```bash
     pipenv run main.py
     ```
   * Using `virtualenv`:
     ```bash
     python main.py
     ```
