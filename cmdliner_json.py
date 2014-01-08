# import requests
# import json
# WRITTEN FOR PYTHON3
import traceback
import locale
from subprocess import check_output, CalledProcessError
from flask import Flask, jsonify, abort
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

__all__ = ['make_json_app']

cmds = [
    {
        'id': 1,
        'description': 'the w command',
        'command': 'w'
    },
    {
        'id': 2,
        'description': 'the top command',
        'command': 'top -l1 -u'
    },
]


def make_json_app(import_name, **kwargs):
    """
    Creates a JSON-oriented Flask app.

    All error responses that you don't specifically
    manage yourself will have application/json content
    type, and will contain JSON like this (just an example):

    { "message": "405: Method Not Allowed" }
    """
    def make_json_error(ex):
        response = jsonify(message=str(ex))
        response.status_code = (ex.code
                                if isinstance(ex, HTTPException)
                                else 500)
        return response

    app = Flask(import_name, **kwargs)

    for code in default_exceptions.keys():
        app.error_handler_spec[None][code] = make_json_error

    return app

#### HAY LETS MAKE THE APP HAHAHAHAHAH*ahem*
app = make_json_app(__name__)
app.config.from_object(__name__)


def execute_cmd(cmd):
    """
        run a command, return the code and the body
    """
    encoding = locale.getdefaultlocale()[1]
    try:
        output = check_output(cmd, shell=True)
    except CalledProcessError as e:
        return (e.returncode, e.output)
    else:
        return (0, output.decode(encoding).split('\n'))


@app.route('/v1.0/cmds', methods=['GET'])
def list_cmds():
    return jsonify({'cmds': cmds})


@app.route('/v1.0/cmds/<int:cmd_id>', methods=['GET'])
def get_cmd_info(cmd_id):
    cmd = list(filter(lambda t: t['id'] == cmd_id, cmds))
    if len(cmd) == 0:
        abort(404)
    return jsonify({'cmd': cmd[0]})


@app.route('/v1.0/cmds/<int:cmd_id>/run', methods=['POST'])
def run_cmd(cmd_id):
    cmd = list(filter(lambda t: t['id'] == cmd_id, cmds))
    if len(cmd) == 0:
        abort(404)
    else:
        try:
            xit_code, output = execute_cmd(cmd[0]['command'])
        except Exception as e:
            return jsonify(
                {
                    'response': {
                        'exception': e,
                        'traceback': traceback.format_exc()
                    }
                }
            ), 400
        else:
            return jsonify(
                {
                    'response': {
                        'return_code': xit_code,
                        'output': output
                    }
                }
            ), 201


if __name__ == '__main__':
    app.run(debug=True)
