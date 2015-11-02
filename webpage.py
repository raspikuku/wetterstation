#! /usr/bin/env python

import cgi, sys
#import string,cgi,time
#from os import curdir, sep
from pprint import pprint
from urlparse import urlparse, parse_qs
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json

class MyHandler(BaseHTTPRequestHandler):
    def xxx__init__(self, request, client_address, server):
        self.read_config()
        super(MyHandler, self).__init__(request, client_address, server)

    def do_GET(self):
        self.read_config()
        #oConfig = open('config.json', 'r')
        #self.config = json.loads(oConfig.read())
        
        file = open('current_weather.json', 'r')
        oTemplate = open('webpage/template.html', 'r')
        template = oTemplate.read()

        json_string = file.read()
        
        parsed_json = json.loads(json_string)

        template = template.replace('{{datetime}}', parsed_json['datetime']) 
        template = template.replace('{{temp}}', parsed_json['temp']) 
        template = template.replace('{{humid}}', parsed_json['humid']) 
        template = template.replace('{{press}}', parsed_json['press']) 
        template = template.replace('{{light}}', parsed_json['light']) 
        template = template.replace('{{title}}', self.config['site_title']) 
        template = template.replace('{{subtitle}}', self.config['site_subtitle']) 

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(template)
        return

    def get_template(self):     
        return

    def do_POST(self):
        global rootnode
        try:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            #if ctype == 'multipart/form-data':
            query=cgi.parse_multipart(self.rfile, pdict)
            #form = cgi.FieldStorage() 
            #pprint(form)
            #alarm_status = form.getfirst("alarm_status", 0)
            #print'alarm', alarm_status
            aaa = query.get('alarm_status')
            #print aaa[0]
            if type(aaa) is list :
                print 'is al list'
            
            if type(aaa) is list and aaa[0] == 'on':
                print 'alarm on'
            else:
                print 'alarm off'
            
            pprint(query)
            self.send_response(301)
            
            self.end_headers()
            #upfilecontent = query.get('upfile')
            #print "filecontent", upfilecontent[0]
            self.wfile.write("<HTML>POST OK.<BR><BR>");
            #self.wfile.write(upfilecontent[0]);
            
        except :
            e = sys.exc_info()[0]
            print( "<p>Error: %s</p>" % e )
            #pass

    def read_config(self):
        with open('config.json', 'r') as infile:
            self.config = json.loads(infile.read())

    def write_config(self):
        with open('config.json', 'w') as outfile:
            json.dump(self.config, outfile, sort_keys=True, indent=4, ensure_ascii=False)


def main():
    try:
        server = HTTPServer(('', 80), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()


