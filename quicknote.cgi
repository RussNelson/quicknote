#!/usr/bin/python
""" Add some text to a student's record. If no token=, go get one. If no student=, give them a list with links.
    To get a token, visit the token URL with the client id and secret.
"""

import urllib2
import cgi
import sys
import json
import config

form = cgi.FieldStorage()
code = form.getvalue("code", None)

# If the session verification code is not set, redirect to the SLC Sandbox authorization endpoint
if code is None:
    url = config.AUTHORIZATION_ENDPOINT + '?client_id=' + config.CLIENT_ID + '&redirect_uri=' + config.REDIRECT_URI
    open("/tmp/outf", "a").write("redirect %s\n" % url)
    sys.stdout.write("Status: 302 Moved\n"
                     "Location: "+url+"\n\n")
    sys.exit()
  
url = '%s?client_id=%s&client_secret=%s&grant_type=authorization_code&redirect_uri=%s&code=%s' % (config.TOKEN_ENDPOINT, config.CLIENT_ID, config.CLIENT_SECRET, config.REDIRECT_URI, code)

headers = { 'Content-Type': 'application/vnd.slc+json',
            'Accept': 'application/vnd.slc+json' }
#curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
open("/tmp/outf", "a").write("urllib %s\n" % url)
result = urllib2.urlopen( urllib2.Request(url, None, headers) )

# de-serialize the result into an object
result = json.load(result)

url = 'start.cgi?token=' + result['access_token']

sys.stdout.write("Status: 302 Moved\n"
                 "Location: "+url+"\n\n")

