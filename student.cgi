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

model = """Content-Type: text/html

<html>
  <body>
	<h1>Notes</h1> 
<ul>
<form action="student.cgi" method="post" >
<input name="token" type="hidden" value="%(token)s" />
<input name="UUID" type="hidden" value="%(uuid)s" />
<textarea id="body" name="body" class="data" rows="12" cols="80">%(body)s</textarea><br/>
<input class="button" type="submit" value="Submit Form" />
</form>

  </body>

</html>"""

form = cgi.FieldStorage()
token = form.getvalue("token", None)
uuid = form.getvalue("UUID", None)
body  = form.getvalue("body", None)

# If the session verification code is not set, redirect to the SLC Sandbox authorization endpoint
if token is None:
    url = config.AUTHORIZATION_ENDPOINT + '?client_id=' + config.CLIENT_ID + '&redirect_uri=' + config.REDIRECT_URI
    sys.stdout.write("Status: 302 Moved\n"
                     "Location: "+url+"\n\n")
    sys.exit()

if body is None:
  
    url = 'https://api.sandbox.slcedu.org/api/rest/v1/students/%s/custom' % uuid

    headers = { 'Content-Type': 'application/vnd.slc+json',
                'Accept': 'application/vnd.slc+json',
                'Authorization': 'bearer %s' % token}
    try:
        result = urllib2.urlopen( urllib2.Request(url, None, headers) )
    except urllib2.HTTPError, e:
        if e.code == 401:
            sys.stdout.write("Status: 302 Moved\n" + 
                             "Location: "+config.REDIRECT_URI+"\n\n")
            sys.exit()
        elif e.code == 404:
            body = ''
        else: raise
    else:

        # de-serialize the result into an object
        result = json.load(result)
        body = result['body']

    sys.stdout.write(model % locals()) 

else:
  
    url = 'https://api.sandbox.slcedu.org/api/rest/v1/students/%s/custom' % uuid

    bodyjson = json.dumps({'body': body})

    headers = { 'Content-Type': 'application/json',
                'Accept': 'application/vnd.slc+json',
                'Authorization': 'bearer %s' % token}
    outf = open("/tmp/outf", "w")
    try:
        result = urllib2.urlopen( urllib2.Request(url, bodyjson, headers) )
    except urllib2.HTTPError, e:
        if e.code == 401:
            sys.stdout.write("Status: 302 Moved\n" + 
                             "Location: "+config.REDIRECT_URI+"\n\n")
            sys.exit()
        if e.code == 404:
            sys.stdout.write("Content-Type: text/plain\n\n" + "Oh dear, that didn't work out so well")
            sys.stdout.write('bodyjson: %s\n' % bodyjson)
            sys.stdout.write('url: %s\n' % url)
            sys.stdout.write('token: %s\n' % token)
            sys.stdout.write('uuid: %s\n' % uuid)
            sys.exit()
        else: raise

    sys.stdout.write("Content-Type: text/plain\n\n" + "Text worked.")
    sys.exit()

