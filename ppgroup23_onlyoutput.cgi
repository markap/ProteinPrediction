#!/usr/bin/python

import cgi
import cgitb; cgitb.enable()
import subprocess
import os
import predictor

form = cgi.FieldStorage()

try:
  # Get filename here.
  fileitem = form['upload']
  fileprefix = '/tmp/'
  # Test if the file was uploaded
  if fileitem.filename:
    fn = os.path.basename(fileitem.filename.replace("\\", "/" ))
    open(fileprefix + fn, 'wb').write(fileitem.file.read())
    #p = subprocess.Popen(["python", "our-stand-alone-executable-file", fileprefix + fn], stdout=subprocess.PIPE)
    #p = subprocess.Popen(["python", "predictor.py", "-a", fileprefix + fn], stdout=subprocess.PIPE)
       #output, err = p.communicate()  
    
    output = "tada"

    print ("""Content-Type: text/html\n
     <html><head><title>PP1 - Group-23</title></head></html>
    	<body>
    %s
    </body>
    </html>"""
     % (output))
    #print fileprefix + fn
    predictor.predict(fileprefix + fn)
    #print "Content-Type: text/html"
    #predictor.predict("/mnt/home/student/ppgroup23/public_html/cgi-bin/tmp/tmps_independent.arff")


except:
  print "Content-type:text/html\r\n\r\n"
  print "<html>"
  print "<head>"
  print "<title>PP1 - Group-23</title>"
  print "</head>"
  print "<body>"
  print "<center><h2>Bioinformatics Application by Group-23</h2></br>"
  print "<h2>---------------------------------------</h2>"
  print "<form action=\"ppgroup23_onlyoutput.cgi\" method=\"post\" enctype=\"multipart/form-data\">"
  print "<input type=\"file\" name=\"upload\" required />"
  print "<input type=\"submit\" value=\"Submit\" name=\"Submit\" />"
  print "<h2>---------------------------------------</h2></br>"
  print "</form></center>"
  print "</body>"
  print "</html>"
