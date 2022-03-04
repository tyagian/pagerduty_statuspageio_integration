from flask import json
from flask import request
from flask import Flask
import pprint
import statuspageio

app = Flask(__name__)

# init printer
pp = pprint.PrettyPrinter(indent=4)

HOST="127.0.0.1"
#PORT=500

@app.route('/')
def api_root():
    return 'Welcome Guys'

@app.route('/pagerduty',methods=['POST'])
def api_gh_message():
    if request.headers['Content-Type'] == 'application/json':

        data = request.get_json()
        #data = json.dumps(request.json)
        pp.pprint (data)

        #priority = data["event"]["data"]["priority"]["summary"]
        #incident_summary  = data["event"]["data"]["title"]
        #event_type = data["event"]["event_type"]

        #print ("priority:",priority," - ","incident:", incident_summary," - ","event type:", event_type)

        return " "    


if __name__ == '__main__':
    app.run(host=HOST, debug=True, threaded=True)
