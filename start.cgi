#!/usr/bin/python
""" Add some text to a student's record. If no token=, go get one. If no student=, give them a list with links.
    To get a token, visit the token URL with the client id and secret.
"""

import urllib2
import cgi
import sys
import json
from types import *
import config

model = open("model.html").read().split("|")

form = cgi.FieldStorage()
token = form.getvalue("token", None)

# If the session verification code is not set, redirect to the SLC Sandbox authorization endpoint
if token is None:
    url = config.AUTHORIZATION_ENDPOINT + '?client_id=' + config.CLIENT_ID + '&redirect_uri=' + config.REDIRECT_URI
    sys.stdout.write("Status: 302 Moved\n"
                     "Location: "+url+"\n\n")
    sys.exit()
  
url = 'https://api.sandbox.slcedu.org/api/rest/v1/students'

headers = { 'Content-Type': 'application/vnd.slc+json',
            'Accept': 'application/vnd.slc+json',
            'Authorization': 'bearer %s' % token}
#curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
open("/tmp/outf", "a").write("urllib start %s\n" % url)
try:
    result = urllib2.urlopen( urllib2.Request(url, None, headers) )
except urllib2.HTTPError, e:
    if e.code != 401: raise
    sys.stdout.write("Status: 302 Moved\n" + 
                     "Location: "+config.REDIRECT_URI+"\n\n")
    sys.exit()

# de-serialize the result into an object
result = json.load(result)

sys.stdout.write(model[0])
result.sort(lambda x,y: cmp(x['name']['lastSurname'], y['name']['lastSurname']))
for student in result:
    sys.stdout.write(model[1] % ( token, student['id'], student['name']['firstName'], student['name']['lastSurname']))
sys.stdout.write(model[2])
