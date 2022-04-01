1) Use Python 3.9 or lower. Bug in 3.10.
2) Install `python3 -m pip install requests`
3) Edit `config.py`
4) Run `01_auth_server.py`, navigate to https://localhost:8000 and log in with all your clan accounts
5) Run `02_refresh_auth_tokens.py` every time you want to use the tool.
6) Run `03_list_inactive_users.py`