import oauth2
import urllib.parse
import urllib.request
import webbrowser
import json
from http.server import BaseHTTPRequestHandler, HTTPServer


URL_USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
USER_INFO_SCOPE = 'email profile'


oauth = oauth2.OAuth2(redirect_uri='http://localhost:8000')

oauth.getAuth(scope = USER_INFO_SCOPE)

header = {'Authorization' : '%s %s'%(oauth.token_type,oauth.access_token)}

req = urllib.request.Request(URL_USER_INFO, headers = header)

with urllib.request.urlopen(req) as response:
    resp = response.read()
    print(resp)
