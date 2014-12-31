import webbrowser
import json
from rauth import OAuth1Service, OAuth1Session
from rauth.utils import parse_utf8_qsl
from rauth.oauth import HmacSha1Signature
import sys

GET_TOKEN_URL = 'https://api.login.yahoo.com/oauth/v2/get_token/'
AUTHORIZATION_URL = 'https://api.login.yahoo.com/oauth/v2/request_auth/'
REQUEST_TOKEN_URL = 'https://api.login.yahoo.com/oauth/v2/get_request_token/'

BASE_URL = 'http://fantasysports.yahooapis.com/fantasy/v2/'
CALLBACK_URL = 'oob'

class YAuth:

	def __init__(self):
		self.creds = self.read_credentials()
		self.srvc = None

	def read_credentials(self):
		f = open('credentials.json')
		return json.load(f)

	def update_credentials(self,access_token="",access_token_secret="",session_handle=""):
		f = open('credentials.json','w')
		if access_token != "": self.creds['access_token'] = access_token
		if access_token_secret != "": self.creds['access_token_secret'] = access_token_secret
		if session_handle != "": self.creds['session_handle'] = session_handle
		f.write(json.dumps(self.creds,sort_keys=True,indent=4,separators=(',', ': ')))
		f.close()

	def get_access_token(self):
		raw_token = self.srvc.get_raw_access_token(
				self.creds['request_token'],
				self.creds['request_token_secret'],
				data={'oauth_verifier': self.creds['verifier']}
			)
		token_data = parse_utf8_qsl(raw_token.content)
		access_token = token_data['oauth_token']
		access_token_secret = token_data['oauth_token_secret']
		session_handle = token_data['oauth_session_handle']
		self.update_credentials(
			access_token=access_token,
			access_token_secret=access_token_secret,
			session_handle=session_handle
		)
		session = self.srvc.get_session(
				(self.creds['access_token'],self.creds['access_token_secret'])
			)

	def renew_access_token(self):
		access_token, access_token_secret = self.srvc.get_access_token(
				self.creds['access_token'], 
				self.creds['access_token_secret'],
				data={'oauth_session_handle': self.creds['session_handle']}
			)
		self.update_credentials(
			access_token=access_token,
			access_token_secret=access_token_secret,
		)
		session = self.srvc.get_session(
				(self.creds['access_token'],self.creds['access_token_secret'])
			)
		return session

	def authorize(self):

		# Get a real consumer key & secret from https://dev.twitter.com/apps/new
		self.srvc = OAuth1Service(
		    name='yahoo',
		    consumer_key=self.creds['consumer_key'],
		    consumer_secret=self.creds['consumer_secret'],
		    request_token_url=REQUEST_TOKEN_URL,
		    access_token_url=GET_TOKEN_URL,
		    authorize_url=AUTHORIZATION_URL,
		    base_url=BASE_URL,
		    signature_obj=HmacSha1Signature
		)

		if 'session_handle' not in self.creds:
			request_token, request_token_secret = \
				self.srvc.get_request_token(params={'oauth_callback': CALLBACK_URL,})
			authorize_url = self.srvc.get_authorize_url(request_token)
			webbrowser.open(authorize_url)
			verifier = raw_input("Input code given: ")
			try:
				session = self.get_access_token()
			except KeyError as e:
				if 'oauth_verifier_invalid' in e.message:
					print "Verifier invalid."
				elif "oauth_problem=token_rejected" in e.message:
					print "Token rejected."
				elif "oauth_problem=token_expired" in e.message:
					print "Token expired."
				sys.exit(-1)
		else:
			try:
				session = self.renew_access_token()
			except KeyError as e:
				if 'oauth_verifier_invalid' in e.message:
					print "Verifier invalid."
				elif "oauth_problem=token_rejected" in e.message:
					print "Token rejected."
				elif "oauth_problem=token_expired" in e.message:
					print "Token expired."
				sys.exit(-1)
		return session
