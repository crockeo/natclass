from flask import Flask, Response, request

import features
import models
import flask
import json

app = Flask(__name__)

instances = {}

###
# _all_sat
#
# Produces the set of sounds that are produced from the current set of
# constraints.
def _all_sat(constraint):
    s = []
    f = features.get_features()
    for k in f:
        if constraint.constrain(f[k]):
            s.append(k)
    return s

###
# _wrong_instance
#
# Generates a
def _wrong_instance():
    return Response(
        json.dumps({

        }),
        status = 400,
        mimetype = 'application/json'
    )

###
# new_instance
#
# Provides the client with a new instance with which it can 
@app.route('/api/newinstance', methods = ['POST'])
def new_instance():
    n = new_instance.instance
    instances[n] = models.SetConstraint()

    new_instance.instance += 1

    return Response(
        json.dumps({
            'status': 'success',
            'data': n
        }),
        status = 200,
        mimetype = 'application/json'
    )
new_instance.instance = 0

###
# current_sounds
#
# Get the current set of possible sounds.
@app.route('/api/<int:instance>/sounds', methods = ['GET'])
def current_sounds(instance):
    if instance not in instances:
        return 'No such instance.', 400

    return Response(
        json.dumps({
            'status': 'success',
            'data': _all_sat(instances[instance])
        }),
        status = 200,
        mimetype = 'application/json'
    )

###
# add_constraint
#
# Adding a constraint to the current set of constraints.
@app.route('/api/<int:instance>/constraint', methods = ['POST'])
def add_constraint(instance):
    if instance not in instances:
        return Response(
            json.dumps({
                'status': 'failure',
                'data': 'No such instance.'
            }),
            status = 400,
            mimetype = 'application/json'
        )

    fail = Response(
        json.dumps({
            'status': 'failure',
            'data': 'Could not parse request.'
        }),
        status = 400,
        mimetype = 'application/json'
    )

    try:
        r = request.get_json()
    except Exception as err:
        return fail

    if r['constraint'] == None:
        return fail

    try:
        c = parse(r['constraint'])
    except Exception as err:
        return fail

    instances[instance].add(c)
    return Response(
        json.dumps({

        }),
        status = 200,
        mimetype = 'application/json'
    )

###
# clear_constraints
#
# Clearing the constraints on a given instance.
@app.route('/api/<int:instance>/clear', methods = ['POST'])
def clear_constraints(instance):
    if instance not in instances:
        return 'No such instance.', 400
    instances[instance].clear()

    return Response(
        json.dumps({
            'status': 'success',
            'data': 'Constraints cleared.'
        }),
        status = 200,
        mimetype = 'application/json'
    )

###
# start
#
# Starting the server.
def start():
    app.run('0.0.0.0', 8000)
