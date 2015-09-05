import urllib.parse
import urllib.request
import webbrowser
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

with open('config.json') as data_file:
    config =  json.load(data_file)

class OAuth2:
    def __init__(self, base_url = None, redirect_uri = None, client_id = None, client_secret = None):

        if base_url is not None:
            self.base_url = base_url
        else:
            self.base_url = config['BASE_URL']

        if redirect_uri is not None:
            self.redirect_uri = redirect_uri
        else:
            self.redirect_uri = config['REDIRECT_URI']

        if client_id is not None:
            self.client_id = client_id
        else:
            self.client_id = config['CLIENT_ID']

        if client_secret is not None:
            self.client_secret = client_secret
        else:
            self.client_secret = config['CLIENT_SECRET']


    def getAuth(self,scope=None):

        auth_values = { 'client_id' : self.client_id,
                        'redirect_uri' : self.redirect_uri,
                        'scope' : 'email',
                        'response_type' : 'code'}

        if scope is not None:
            auth_values['scope'] = scope

        url_values =  urllib.parse.urlencode(auth_values)
        full_url = config['BASE_URL'] + config['AUTH_URL'] + '?' + url_values

        webbrowser.open(full_url)

        if self.redirect_uri != config['REDIRECT_URI']:
            self.listenAuth()
        else:
            self.code = input('What was the returned code?')

    def getToken(self):

        if  not hasattr(self, 'code'):
            return

        url_auth = config['BASE_URL'] + config['TOKEN_URL']
        auth_values = {'code' : self.code,
                        'client_id' : self.client_id,
                        'client_secret' : self.client_secret,
                        'redirect_uri' : self.redirect_uri,
                        'grant_type' : 'authorization_code'}

        encoded_values =  urllib.parse.urlencode(auth_values)
        binary_values = encoded_values.encode('utf-8')

        req = urllib.request.Request(url_auth,binary_values)

        response = urllib.request.urlopen(req)

        json_resp = json.loads(response.read().decode('utf-8'))

        self.id_token = json_resp['id_token']
        self.access_token = json_resp['access_token']
        self.refresh_token = json_resp['refresh_token']
        self.token_type = json_resp['token_type']

    def refreshToken(self):
        pass

    def listenAuth(self):
        http_listener = HttpListener
        http_listener.oauth2 = self
        httpd = HTTPServer(('',8000), HttpListener)
        httpd.handle_request()

class HttpListener (BaseHTTPRequestHandler):
    def do_GET(self):
        path = urllib.parse.urlparse(self.path)

        qry = path.query.split('=')
        if hasattr(self, 'oauth2') and len(qry) == 2:
            self.oauth2.code = qry[1]
            self.oauth2.getToken()
            self.send_response(200)
        else:
            self.send_response(400)
