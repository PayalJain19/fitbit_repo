from django.http import HttpResponse, HttpResponseRedirect
from sqlalchemy.sql.expression import and_
import datetime
import json
import oauth2 as oauth
import requests
import urlparse

consumer_key ='Your app's consumer key'
consumer_secret = 'Your app's consumer secret'
SERVER = 'api.fitbit.com'

request_token_url = 'http://%s/oauth/request_token' % SERVER
access_token_url = 'http://%s/oauth/access_token' % SERVER
authorize_url = 'http://www.fitbit.com/oauth/authorize'


class FitbitAuthenticationHandler():
    allowed_methods = 'GET'
    def setCookie(self, response, key, value):
        max_age = 1 * 60 * 60  # one hour
        expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
        response.set_cookie(key, value, max_age=max_age, expires=expires, domain=None, secure=False)
    
    def read(self, request, *args, **kwargs):
        
        consumer = oauth.Consumer(consumer_key, consumer_secret)
        client = oauth.Client(consumer)

        try:
            resp, content = client.request(request_token_url, "GET")
            request_token = dict(urlparse.parse_qsl(content))
            roauth_token = request_token['oauth_token']
            roauth_token_secret = request_token['oauth_token_secret']
            new_authorize_url = authorize_url + '?oauth_token=' + request_token['oauth_token']+'&oauth_callback=https://friday-dev-unstable.dexetraapi.com/api/fitbitoauthcb/'
            response = HttpResponseRedirect(new_authorize_url)

            self.setCookie(response, 'roauth_token', roauth_token)
						self.setCookie(response, 'roauth_token_secret', roauth_token_secret)
            
        except Exception:
            logger.exception('error in getting code')
           
            response = HttpResponse("", status=302)
            response['Location'] = client_url.encode('utf-8')
            
        finally:
								return response
          
