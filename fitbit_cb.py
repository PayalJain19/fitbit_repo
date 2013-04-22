from django.http import HttpResponse, HttpResponseRedirect
from sqlalchemy.sql.expression import and_
import datetime
import json
import oauth2 as oauth
import requests
import urlparse
onsumer_key = 'consumer key'
consumer_secret = 'consumer secret'
SERVER = 'api.fitbit.com'
request_token_url = 'http://%s/oauth/request_token' % SERVER
access_token_url = 'http://%s/oauth/access_token' % SERVER
authorize_url = 'http://www.fitbit.com/oauth/authorize'

class FitbitAuthenticationCBHandler(BaseHandler):
    allowed_methods = 'GET'
    
   def setCookie(self, response, key, value):
        max_age = 1 * 60 * 60  # one hour
        expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
        response.set_cookie(key, value, max_age=max_age, expires=expires, domain=None, secure=False)
        logger.debug(response)
    def read(self, request, *args, **kwargs):
        query_string = request.META.get('QUERY_STRING')
        query_dict = parse_qs(query_string);
        
        if 'oauth_verifier' in query_dict:
            oauth_verifier = query_dict.get('oauth_verifier')[0]

        
        consumer = oauth.Consumer(consumer_key, consumer_secret)
        client = oauth.Client(consumer)
        
        if oauth_verifier:
            token = oauth.Token(request.COOKIES.get('roauth_token'),
                                request.COOKIES.get('roauth_token_secret'))
            user_hash = request.COOKIES.get('userid')
            token.set_verifier(oauth_verifier)
            client = oauth.Client(consumer, token)
            try:
                resp, content = client.request(access_token_url, "POST")
                access_data = dict(urlparse.parse_qsl(content))
               
            except:
                response = HttpResponse("", status=302)
                response['Location'] = client_url.encode('utf-8')
                return response
            logger.debug(client_url)            
            response = HttpResponse("", status=302)
            response['Location'] = client_url.encode('utf-8')
            return response
        
        else:
            
            logger.debug('Failed to retrieve OAUTH_VERIFIER:' + client_url)
            response = HttpResponse("", status=302)
            response['Location'] = client_url.encode('utf-8')
            return response
