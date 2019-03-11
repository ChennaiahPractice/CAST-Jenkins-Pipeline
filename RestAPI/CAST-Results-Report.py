# Python 
import os
import sys
import argparse
import requests
import time

BUS_CRITERIA = {}

def queryCastRestAPI(_apiurl, _auth, _appname, _report):
    _headers = {'Accept':'application/json'}

    if _report == "summary":
        _resturi = 'AAD/results?quality-indicators=(60014,60016)&snapshots=-1&applications=' +_appname 
     
        try:
            print('Credentials: ', _auth)
            print('Rest Call: ', _apiurl+'/'+_resturi)
            print('First attempt to connect...')
            _data = requests.get(_apiurl+'/'+_resturi, headers=_headers, auth=_auth, verify=False, timeout=10)
            print('First attempt succeeded!')
            BUS_CRITERIA = _data.json()
        except Exception as e:
            print('First attempt to connect failed. Exception occured.')
            print(e)
            print('Sleep for 5 seconds... zzzz')
            time.sleep(5)
            print('Try connecting again...')
            try:
                _data = requests.get(_apiurl+'/'+_resturi, headers=_headers, auth=_auth, verify=False, timeout=10)
                print('Second and final attempt succeeded!')
                BUS_CRITERIA = _data.json()
            except Exception as e:
                print('Second attempt to connect failed. Exception occured again.')
                print(e)
                return(2)
            
        return (_data)
    else:
        print("Incorrect arguments - unknown report specified")
        _data = 'print json.dumps({'Error': 'Unknown Report'}, sort_keys=True, indent=4, separators=(',', ': '))
        return(_data)


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

    jsonResults = queryCastRestAPI(_results.connection, _auth, _results.appname, _results.report)
    print('exit code is ' + str(_result_code))
    sys.exit(_result_code)
