import oauth2
import requests
import json


class OAuthEchoClient(object):

	def __init__(self, base_url=None, callback_url=None, oauth_realm=None, consumer_key=None, consumer_secret=None, access_key=None, access_secret=None, API_key=None):
		self.base_url = base_url
		self.callback_url = callback_url
		self.oauth_realm = realm
		self.consumer = oauth2.Consumer(consumer_key, consumer_secret)
		self.access_token = None
		if access_key:
			self.access_token = oauth2.Token(access_key, access_secret)
		self.signature_method = oauth2.SignatureMethod_HMAC_SHA1()
		self.API_key = API_key
		self.session = requests.session()

	def post(self, url, data=None, **params):
		oauth_request = oauth2.Request.from_consumer_and_token(
			self.consumer,
			self.access_token,
			http_url = self.callback_url
		)
		oauth_request.sign_request(self.signature_method, self.consumer, self.access_token)
		oauth_request.set_parameter('key', self.API_key)
		for key, val in params.iteritems():
			oauth_request.set_parameter(key, val)
		oauth_headers = oauth_request.to_header(realm=self.oauth_realm)
		headers = {}
		headers['X-Verify-Credentials-Authorization'] = oauth_headers['Authorization']
		headers['X-Auth-Service-Provider']= self.callback_url
		response = self.session.post(url, data=data, params=params, headers=headers)
		response.raise_for_status()
		return response.content

