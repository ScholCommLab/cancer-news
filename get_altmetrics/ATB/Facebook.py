# -*- coding: utf-8 -*-
"""Facebook

This is a wrapper module for the facebook python SKD (https://github.com/mobolic/facebook-sdk)

author: Asura Enkhbayar <asura.enkhbayar@gmail.com>
"""

import ast
import requests
from facebook import GraphAPI

# Retrieve App Access Token
class Facebook(GraphAPI):
    def __init__(self, app_id, app_secret):
        payload = {'grant_type': 'client_credentials', 'client_id': app_id, 'client_secret': app_secret}
        try:
            response = requests.post('https://graph.facebook.com/oauth/access_token?', params = payload)
        except requests.exceptions.RequestException:  # This is the correct syntax
            raise Exception()
        
        response = ast.literal_eval(response.text)['access_token']
        print("Generated access token: " + response)
        super(Facebook, self).__init__(response)
