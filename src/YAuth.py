import webbrowser
import json
from rauth import OAuth1Service, OAuth1Session
from rauth.oauth import HmacSha1Signature
from rauth.service import PROCESS_TOKEN_ERROR
import sys

GET_TOKEN_URL = 'https://api.login.yahoo.com/oauth/v2/get_token/'
AUTHORIZATION_URL = 'https://api.login.yahoo.com/oauth/v2/request_auth/'
REQUEST_TOKEN_URL = 'https://api.login.yahoo.com/oauth/v2/get_request_token/'

BASE_URL = 'http://fantasysports.yahooapis.com/fantasy/v2/'
CALLBACK_URL = 'oob'

class YAuth:

	def __init__(self):
		self.creds = self.read_credentials()

	def read_credentials(self):
		f = open('credentials.json')
		return json.load(f)

	def update_credentials(self,req_tok="",req_tok_sec="",verifier="",access_token="",access_token_secret=""):
		f = open('credentials.json','w')
		if req_tok != "": self.creds['request_token'] = req_tok
		if req_tok_sec != "": self.creds['request_token_secret'] = req_tok_sec
		if verifier != "": self.creds['verifier'] = verifier
		if access_token != "": self.creds['access_token'] = access_token
		if access_token_secret != "": self.creds['access_token_secret'] = access_token_secret
		f.write(json.dumps(self.creds,sort_keys=True,indent=4,separators=(',', ': ')))

	def authorize(self):

		# Get a real consumer key & secret from https://dev.twitter.com/apps/new
		yahoo = OAuth1Service(
		    name='yahoo',
		    consumer_key=self.creds['consumer_key'],
		    consumer_secret=self.creds['consumer_secret'],
		    request_token_url=REQUEST_TOKEN_URL,
		    access_token_url=GET_TOKEN_URL,
		    authorize_url=AUTHORIZATION_URL,
		    base_url=BASE_URL,
		    signature_obj=HmacSha1Signature
		)
		print dir(yahoo)

		if 'verifier' not in self.creds:
			request_token, request_token_secret = \
				yahoo.get_request_token(params={'oauth_callback': CALLBACK_URL,})
			authorize_url = yahoo.get_authorize_url(request_token)
			webbrowser.open(authorize_url)
			verifier = raw_input("Input code given: ")
			access_token, access_token_secret = yahoo.get_access_token(
					request_token,
					request_token_secret,
					data={'oauth_verifier': verifier}
				)
			self.update_credentials(request_token,request_token_secret,verifier,access_token,access_token_secret)
		try:
			session = OAuth1Session(
					self.creds['consumer_key'],
					self.creds['consumer_secret'],
					access_token=self.creds['access_token'],
					access_token_secret=self.creds['access_token_secret']
				)
		except KeyError as e:
			print e
			if 'oauth_verifier_invalid' in e.message:
				pass
			elif "oauth_problem=token_rejected" in e.message:
				access_token, access_token_secret = yahoo.get_access_token(
							self.creds['request_token'], 
							self.creds['request_token_secret'],
							data={'oauth_token': self.creds['access_token']}
						)
				self.update_credentials(access_token=access_token,access_token_secret=access_token_secret)
				session = OAuth1Session(
					self.creds['consumer_key'],
					self.creds['consumer_secret'],
					access_token=access_token,
					access_token_secret=access_token_secret
				)
		return session
