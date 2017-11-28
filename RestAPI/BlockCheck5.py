# Python 
import os
import sys
import argparse
import requests

BUS_CRITERIA = {}

def check_rule(_apiurl, _auth, _appname, _rule):
    _headers = {'Accept':'application/json'}

    if _rule == "new_vs_old":
        _resturi = 'AAD/results?select=(evolutionSummary)&quality-indicators=(60017)&snapshots=(-1)&applications=(' +_app + ')'
     
        try:
            print('Credentials: ', _auth)
            print('Rest Call: ', _apiurl+_resturi)
            _data = requests.get(_apiurl+_resturi, headers=_headers, auth=_auth, verify=False)
            BUS_CRITERIA = _data.json()
        except:
            print('Failed on RESTAPI')
            return(200)
        try:
            _results = (BUS_CRITERIA[0])
        except IndexError:
            print("Likely invalid application name")
            return(100)             
        _data = _results.get('applicationResults')
        _results = _data[0].get('result')
        _added =    _results.get('evolutionSummary').get('addedCriticalViolations')
        _removed =  _results.get('evolutionSummary').get('removedCriticalViolations')
        print(str(_added) + ' violations added, and  ' + str(_removed) + ' were removed')
        if _added <= _removed:
            print(str(_added) + ' were added and ' + str(_removed) + ' were removed')
            return(0)
        else:
            print('build failed')
            return(10)       
    else:
        print("invalid rule - failing")
        return(10)


if __name__ == "__main__":
    """ Access RESTAPI, then check results """
    parser = argparse.ArgumentParser(description="""\n\nCAST Blocking Rule Check - \n Reads RestAPI, Pulls scores, runs a test and returns 0 if all is ok, and 10 if not""")
    
    parser.add_argument('-c', '--connection', action='store', dest='connection', required=True, help='Specifies URL to the RestAPI service')
    parser.add_argument('-u', '--username', action='store', dest='username', required=True, help='Username to connect to RestAPI')
    parser.add_argument('-p', '--password', action='store', dest='password', required=True, help='Password to connect to RestAPI')
    parser.add_argument('-a', '--appname', action='store', dest='appname', required=True, help='Name of the target application as shown in AAD')		
    parser.add_argument('-r', '--rule', action='store', dest='rule', required=False, default="new_vs_old",
       choices=['new_vs_old', 'TQI_change'], help='Pre-defined rule number that will be evaluated for success')
    
    parser.add_argument('-v','--version', action='version', version='%(prog)s 1.0')
    _results = parser.parse_args()
    _auth = (_results.username, _results.password)

    _result_code = check_rule(_results.connection, _auth, _results.appname, _results.rule)
    print('exit code is ' + str(_result_code))
    sys.exit(_result_code)
