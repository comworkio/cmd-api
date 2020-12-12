from flask import Flask
from flask_restful import Resource, Api

from subprocess import check_output
from multiprocessing import Process
import os

app = Flask(__name__)
api = Api(app)

def get_script_output (cmd):
    print("[get_script_output] cmd = {}".format(cmd))
    try:
        return check_output(cmd, shell=True, text=True)
    except:
        return check_output(cmd, shell=True, universal_newlines=True)

def run_cmd_async():
    print("[run_cmd_async] output = {}".format(get_script_output(os.environ['API_CMD'])))

class AsyncCmdApi(Resource):
    def get(self):
        async_process = Process( 
            target=run_cmd_async,
            daemon=True
        )
        async_process.start()
        return {
            'executed': True,
            'async': True
        }

class CmdApi(Resource):
    def get(self):
        output = get_script_output(os.environ['API_CMD'])
        return {
            'executed': True,
            'details': output
        }

class RootEndPoint(Resource):
    def get(self):
        return {
            'alive': True
        }

health_check_routes = ['/', '/health', '/health/']
cmd_routes = ['/cmd', '/cmd-api', '/cmd/', '/cmd-api/']
async_cmd_routes = ['/cmd/async', '/cmd-api/async', '/cmd/async/', '/cmd-api/async/']

api.add_resource(RootEndPoint, *health_check_routes)
api.add_resource(CmdApi, *cmd_routes)
api.add_resource(AsyncCmdApi, *async_cmd_routes)

if __name__ == '__main__':
    app.run()
