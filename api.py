from flask import Flask, request

## https://github.com/flask-restful/flask-restful/pull/913
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func

from flask_restful import Resource, Api

from subprocess import check_output
from multiprocessing import Process
import os
import json
import sys
import re

app = Flask(__name__)
api = Api(app)

def get_script_output (cmd):
    print("[get_script_output] cmd = {}".format(cmd))
    try:
        return check_output(cmd, shell=True, text=True)
    except:
        return check_output(cmd, shell=True, universal_newlines=True)

def is_forbidden (var):
    forbidden_chars = ["'" , "\"", "&", ";", "|", "\\", "$"]
    return any(char in var for char in forbidden_chars)

def is_not_empty (var):
    if (isinstance(var, bool)):
        return var
    elif (isinstance(var, int)):
        return True
    empty_chars = ["", "null", "nil", "false", "none"]
    return var is not None and not any(c == var.lower() for c in empty_chars)

def is_empty (var):
    return not is_not_empty(var)

def is_empty_request_field (name):
    body = request.get_json(force=True)
    return not name in body or is_empty(body[name])

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def is_not_ok(body):
    return not "status" in body or body["status"] != "ok"

def check_mandatory_param(name):
    if is_empty_request_field(name):
        eprint("[check_mandatory_param] bad request : missing argument = {}, body = {}".format(name, request.data))
        return {
            "status": "bad_request",
            "reason": "missing {} argument".format(name)
        }
    else:
        return {
            "status": "ok"
        }

def run_cmd():
    return get_script_output(os.environ['API_CMD'])

def run_cmd_async():
    print("[run_cmd_async] output = {}".format(run_cmd()))

def run_cmd_argv():
    body = request.get_json(force=True)
    cmd = "{} {}".format(os.environ['API_CMD'], body['argv'])
    return get_script_output(cmd)

def run_cmd_async_argv():
    print("[run_cmd_async] output = {}".format(run_cmd_argv()))

def check_api_cmd_is_defined():
    if is_empty(os.environ.get('API_CMD')):
        return {
            'status': 'forbidden',
            'reason': 'API_CMD is not defined for this instance'
        }
    else:
        return {
            'status': 'ok'
        }

def check_argv_is_enabled():
    regexp_argv = os.environ.get('REGEXP_ARGV')
    enable_argv = os.environ.get('ENABLE_ARGV')
    body = request.get_json(force=True)
    argv = body['argv']

    if is_empty(enable_argv) or enable_argv != "enabled":
        return {
            'status': 'forbidden',
            'reason': "ENABLE_ARGV is not enabled : value = {}".format(enable_argv)
        }
    elif is_not_empty(regexp_argv):
        if re.match(regexp_argv, argv) and not is_forbidden(argv):
            return {
               'status': 'ok'
            }
        else:
            return {
                'status': 'forbidden',
                'reason': "Args {} are not matching {}".format(argv, regexp_argv)
            } 
    else:
        return {
            'status': 'ok'
        }

class AsyncCmdApi(Resource):
    def get(self):
        c = check_api_cmd_is_defined()
        if is_not_ok(c):
            return c, 403

        async_process = Process( 
            target=run_cmd_async,
            daemon=True
        )
        async_process.start()
        return {
            'status': 'ok',
            'executed': True,
            'async': True
        }
    def post(self):
        c = check_api_cmd_is_defined()
        if is_not_ok(c):
            return c, 403

        c = check_mandatory_param('argv')
        if is_not_ok(c):
            return c, 400

        c = check_argv_is_enabled()
        if is_not_ok(c):
            return c, 403

        async_process = Process( 
            target=run_cmd_async_argv,
            daemon=True
        )
        async_process.start()
        return {
            'status': 'ok',
            'executed': True,
            'async': True
        }

class CmdApi(Resource):
    def get(self):
        c = check_api_cmd_is_defined()
        if is_not_ok(c):
            return c, 403

        output = run_cmd()
        return {
            'status': 'ok',
            'executed': True,
            'details': output
        }
    def post(self):
        c = check_api_cmd_is_defined()
        if is_not_ok(c):
            return c, 403
            
        c = check_mandatory_param('argv')
        if is_not_ok(c):
            return c, 400

        c = check_argv_is_enabled()
        if is_not_ok(c):
            return c, 403

        output = run_cmd_argv()
        return {
            'status': 'ok',
            'executed': True,
            'details': output
        }

class RootEndPoint(Resource):
    def get(self):
        return {
            'status': 'ok',
            'alive': True
        }

class ManifestEndPoint(Resource):
    def get(self):
        try:
            with open(os.environ['MANIFEST_FILE_PATH']) as manifest_file:
                manifest = json.load(manifest_file)
                return manifest
        except IOError as err:
            return {
                'status': 'error', 
                'reason': err
            }, 500

health_check_routes = ['/', '/health', '/health/']
cmd_routes = ['/cmd', '/cmd-api', '/cmd/', '/cmd-api/']
async_cmd_routes = ['/cmd/async', '/cmd-api/async', '/cmd/async/', '/cmd-api/async/']
manifest_routes = ['/manifest', '/manifest/']

api.add_resource(RootEndPoint, *health_check_routes)
api.add_resource(CmdApi, *cmd_routes)
api.add_resource(AsyncCmdApi, *async_cmd_routes)
api.add_resource(ManifestEndPoint, *manifest_routes)

if __name__ == '__main__':
    app.run()
