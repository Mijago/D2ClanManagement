A basic tool to handle multiple clans at once.
For D2Sanctuary, but usable from everyone.

This tool will still grow, don't worry.


1) Create a new Bungie.net app at bungie.net/en/Application. Give it the scope "manage clans" and set the redirect url to "https://localhost:8000". 
2) Install `python3 -m pip install requests`
3) Edit `config.py`
4) Run `01_auth_server.py`, navigate to https://localhost:8000 and log in with all your clan accounts
5) Run `02_refresh_auth_tokens.py` every time you want to use the tool.
6) Run `03_list_inactive_users.py`