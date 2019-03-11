# Python 
import os
import sys
import argparse
import requests
import time
import json
from json2html import *

BUS_CRITERIA = {}

def queryCastRestAPI(_apiurl, _auth, _appname, _report):
    _headers = {'Accept':'application/json'}

    if _report == "summary":
        _resturi = 'AAD/results?quality-indicators=(60011,60012,60013,60014,60016,60017)&snapshots=-1&applications=' +_appname 
     
        try:
            print('Credentials: ', _auth)
            print('Rest Call: ', _apiurl+'/'+_resturi)
            print('First attempt to connect...')
            _data = requests.get(_apiurl+'/'+_resturi, headers=_headers, auth=_auth, verify=False, timeout=10)
            print('First attempt succeeded!')
            _results = _data.json()
        except Exception as e:
            print('First attempt to connect failed. Exception occured.')
            print(e)
            print('Sleep for 5 seconds... zzzz')
            time.sleep(5)
            print('Try connecting again...')
            try:
                _data = requests.get(_apiurl+'/'+_resturi, headers=_headers, auth=_auth, verify=False, timeout=10)
                print('Second and final attempt succeeded!')
                _results = _data.json()
            except Exception as e:
                print('Second attempt to connect failed. Exception occured again.')
                print(e)
                _results = json.dumps({'Error': 'Unable to connect'}, sort_keys=True, indent=4, separators=(',', ': '))
    else:
        print("Incorrect arguments - unknown report specified")
        _results = json.dumps({'Error': 'Unknown Report'}, sort_keys=True, indent=4, separators=(',', ': '))
   
    return(_results)


if __name__ == "__main__":
    """ Access RESTAPI, then check results """
    parser = argparse.ArgumentParser(description="""\n\nCAST Blocking Rule Check - \n Reads RestAPI, Pulls scores, runs a test and returns 0 if all is ok, and 10 if not""")
    
    parser.add_argument('-c', '--connection', action='store', dest='connection', required=True, help='Specifies URL to the RestAPI service')
    parser.add_argument('-u', '--username', action='store', dest='username', required=True, help='Username to connect to RestAPI')
    parser.add_argument('-p', '--password', action='store', dest='password', required=True, help='Password to connect to RestAPI')
    parser.add_argument('-a', '--appname', action='store', dest='appname', required=True, help='Name of the target application as shown in AAD')		
    parser.add_argument('-r', '--report', action='store', dest='report', required=False, default="summary",
       choices=['summary', 'etc.'], help='Pre-defined report name')
    
    parser.add_argument('-v','--version', action='version', version='%(prog)s 1.0')
    _results = parser.parse_args()
    _auth = (_results.username, _results.password)

    _jsonResults = queryCastRestAPI(_results.connection, _auth, _results.appname, _results.report)
    print('Results: ' + str(_jsonResults))
    
    f = open('index.html','w')
    #f.write('<html><head></head><body></body>')
    f.write(json2html.convert(json = _jsonResults))
    #f.write('</html>')
    f.close()
    sys.exit(0)

