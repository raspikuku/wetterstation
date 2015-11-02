#! /usr/bin/env python

import cgi
import sys
import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from pprint import pprint


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.read_config()

        template = self.get_template()

        template = template.replace('{{message}}', '')

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(template)
        return

    def do_POST(self):
        self.read_config()
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        query = cgi.parse_multipart(self.rfile, pdict)
        alarm_status = query.get('alarm_status')

        pprint(query)
        pprint(alarm_status)

        if type(alarm_status) is list and alarm_status[0] == 'on':
            print 'alarm on'
            self.config['temp_alarm_status'] = 1
            self.write_config()
        else:
            print 'alarm off'
            self.config['temp_alarm_status'] = 0
            self.write_config()

        self.config['temp_alarm_value'] = int(query.get('temp_value'))

        template = self.get_template()

        template = template.replace('{{message}}', '<p>Changes have been saved.</p>')

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(template)

    def get_template(self):
        with open('../current_weather.json', 'r') as infile:
            weather = json.loads(infile.read())

        with open('template.html', 'r') as infile:
            template = infile.read()

        if self.config['temp_alarm_status'] == 1:
            alarm_status = 'checked'
        else:
            alarm_status = ''

        template = template.replace('{{datetime}}', weather['datetime'])
        template = template.replace('{{temp}}', weather['temp'])
        template = template.replace('{{humid}}', weather['humid'])
        template = template.replace('{{press}}', weather['press'])
        template = template.replace('{{light}}', weather['light'])
        template = template.replace('{{title}}', self.config['site_title'])
        template = template.replace('{{subtitle}}', self.config['site_subtitle'])
        template = template.replace('{{chk_alarm_status}}', alarm_status)
        template = template.replace('{{temp_value}}', str(self.config['temp_alarm_value']))

        return template

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


