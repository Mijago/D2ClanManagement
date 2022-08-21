import http.server
import json
from http.server import BaseHTTPRequestHandler
import os, os.path
from bungieapi import BungieApi
from config import API_KEY, CLIENT_ID, CLIENT_SECRET

LOGIN_URL = "https://www.bungie.net/en/OAuth/Authorize?client_id=%s&response_type=code&reauth=true" % CLIENT_ID
api = BungieApi(API_KEY, CLIENT_ID, CLIENT_SECRET)


class ServerHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message):
        content = f"<html><body><h1>{message}</h1></body></html>"
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_GET(self):
        print("GET", self.path)

        if "?code=" not in self.path:
            self._set_headers()
            self.wfile.write(self._html(f"Could not read the auth code. <a href='{LOGIN_URL}'>Click here</a> to add a new account."))
            return

        code = self.path[self.path.index("?code=") + 6:]
        keys = api.generateKeysFromAuthCode(code)
        if keys is None:
            self._set_headers()
            self.wfile.write(self._html("Some error occured"))
            return

        # add key to file
        lst = {}
        if os.path.exists("users.json"):
            with open("users.json", "r") as f:
                lst = json.load(f)
        lst[keys["membership_id"]] = keys

        with open("users.json", "w") as f:
            json.dump(lst, f, indent=2)

        self._set_headers()
        self.wfile.write(self._html("Success :)"))
        return


    def do_HEAD(self):
        self._set_headers()


import http.server
import ssl

httpd = http.server.HTTPServer(('127.0.0.1', 8000), ServerHandler)
httpd.socket = ssl.wrap_socket(httpd.socket, keyfile='./ssl/key.pem', certfile='./ssl/cert.pem', server_side=True)
httpd.serve_forever()
