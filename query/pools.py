from flask import Flask
from flask import request
import xml.etree.ElementTree as ET
import requests
import json
app = Flask(__name__)
source = "https://raw.githubusercontent.com/devdattakulkarni/elements-of-web-programming/master/data/austin-pool-timings.xml"
data = requests.get(source)
root = ET.fromstring(data.text)

@app.route('/')
def query_search():
    # Passing the parameters
    weekend_q = request.args.get('weekend')
    pool_type_q = request.args.get('pool_type')
    weekday_closure_q = request.args.get('weekday_closure')
    dictionary = {}
    for pool in root.findall('row'):
        pool_name = ''
        weekday = ''
        pool_type = ''
        weekday_closure = ''
        weekend = ''
        try:
            pool_name = pool.find('pool_name').text
            weekday = pool.find('weekday').text
            pool_type = pool.find('pool_type').text
            weekday_closure = pool.find('weekday_closure').text
            weekend = pool.find('weekend').text
        except AttributeError:
            continue
        # searching the query
        if (pool_type_q == pool_type) and (weekday_closure_q == None) and (weekend_q == None):
            dictionary[pool_name] = pool_type
        elif (pool_type_q == None) and (weekday_closure_q == weekday_closure) and (weekend_q == None):
            dictionary[pool_name] = weekday_closure
        elif (pool_type_q == None) and (weekday_closure_q == None) and (weekend_q == weekend):
            dictionary[pool_name] = weekend
        elif (pool_type_q == pool_type) and (weekday_closure_q == weekday_closure) and (weekend_q == None):
            dictionary[pool_name] = [pool_type, weekday_closure]
        elif (pool_type_q == pool_type) and (weekday_closure_q == None) and (weekend_q == weekend):
            dictionary[pool_name] = [pool_type, weekend]
        elif (pool_type_q == None) and (weekday_closure_q == weekday_closure) and (weekend_q == weekend):
            dictionary[pool_name] = [ weekday_closure,weekend]
        elif (pool_type_q == pool_type) and (weekday_closure_q == weekday_closure) and (weekend_q == weekend):
            dictionary[pool_name] = [pool_type, weekday_closure,weekend]
        print(pool_name, " ", weekday, " ", pool_type, " ", weekday_closure)
    print(dictionary)
    # reuturn statement
    if pool_type_q:
        return '\n'.join(list(dictionary.keys()))
    elif weekday_closure_q: 
        return '\n'.join(list(dictionary.keys()))
    elif weekend_q:
        return '\n'.join(list(dictionary.keys()))
    elif pool_type_q and weekday_closure_q:
        return '\n'.join(list(dictionary.keys()))
    elif pool_type_q and weekend_q:  
        return '\n'.join(list(dictionary.keys()))
    elif weekday_closure_q and weekend_q:
        return '\n'.join(list(dictionary.keys()))
    elif pool_type_q and weekday_closure_q and weekend_q:
        return '\n'.join(list(dictionary.keys()))
    elif (pool_type_q == None) and (weekday_closure_q == None) and (weekend_q == None):
        return("Welcome to Austin Pool Information Website.")
    else:
        return("Wrong Search")


if __name__ == "__main__":
    app.run(debug=True)
