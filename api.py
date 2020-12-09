from flask import Flask
from flask_restful import Resource, Api

from subprocess import check_output
import os

app = Flask(__name__)
api = Api(app)

def get_script_output (cmd):
    print("[get_script_output] cmd = {}".format(cmd))
    try:
        return check_output(cmd, shell=True, text=True)
    except:
        return check_output(cmd, shell=True, universal_newlines=True)

class CmdApi(Resource):
    def get(self):
        output = get_script_output(os.environ['API_CMD'])
        return {
            'executed': True
            'details': output
        }

api.add_resource(CmdApi, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
