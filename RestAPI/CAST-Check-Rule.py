# Python 
import os
import sys
import argparse
import requests
import time
#import json
#from json2html import *

def getAddedViolationCount(_apiurl, _auth, _appname, _ruleid):

    try:
        print('Making RestAPI call...')
        _headers = {'Accept':'application/json'}
        _resturi = 'AAD/results?quality-indicators=(' + _ruleid + ')&select=evolutionSummary&snapshots=-9999&applications=' +_appname 
        _data = requests.get(_apiurl+'/'+_resturi, headers=_headers, auth=_auth, verify=False, timeout=10)
        print('Rest call succeeded!')
        
        _vCount = 0
        for item in _data.json():
            # add any new violations for the specified metric
            _vCount = _vCount + item['applicationResults'][0]['result']['evolutionSummary']['addedViolations']
            # subtract any removed violations
            _vCount = _vCount - item['applicationResults'][0]['result']['evolutionSummary']['removedViolations']

        _results = _vCount
            
    except Exception as e:
        print('RestAPI call failed...')
        print(e)
        sys.exit(1)
   
    return(_results)


if __name__ == "__main__":
    """ Access RESTAPI, then check results """
    parser = argparse.ArgumentParser(description="""\n\nCAST Blocking Rule Check - \n Reads RestAPI, Pulls scores, runs a test and returns 0 if all is ok, and 10 if not""")
    
    parser.add_argument('-c', '--connection', action='store', dest='connection', required=True, help='Specifies URL to the RestAPI service')
    parser.add_argument('-u', '--username', action='store', dest='username', required=True, help='Username to connect to RestAPI')
    parser.add_argument('-p', '--password', action='store', dest='password', required=True, help='Password to connect to RestAPI')
    parser.add_argument('-a', '--appname', action='store', dest='appname', required=True, help='Name of the target application as shown in AAD')        
    parser.add_argument('-r', '--ruleid', action='store', dest='ruleid', required=True, help='Rule ID')
    
    parser.add_argument('-v','--version', action='version', version='%(prog)s 1.0')
    _params = parser.parse_args()
    _auth = (_params.username, _params.password)

    _fResults = getAddedViolationCount(_params.connection, _auth, _params.appname, _params.ruleid)
    print('Added Violations: ' + str(_fResults))

    sys.exit(_fResults)

