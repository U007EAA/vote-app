from flask import Flask, render_template, request, make_response, g
from redis import Redis
import os
import socket
import random
import json
import logging

option_a = os.getenv('OPTION_A', "AWS")
option_b = os.getenv('OPTION_B', "Azure")
option_c = os.getenv('OPTION_C', "GCP")
option_a_icon = os.getenv('OPTION_A_ICON', "static/images/aws-circ.png")
option_b_icon = os.getenv('OPTION_B_ICON', "static/images/azure-circ.png")
option_c_icon = os.getenv('OPTION_C_ICON', "static/images/gcp-circ.png")
option_a_bgcolor = os.getenv('OPTION_A_BGCOLOR', "#FF9900")
option_b_bgcolor = os.getenv('OPTION_B_BGCOLOR', "#0080F")
option_c_bgcolor = os.getenv('OPTION_C_BGCOLOR', "#0F9D58")
hostname = socket.gethostname()

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

def get_redis():
    if not hasattr(g, 'redis'):
        g.redis = Redis(host="redis", db=0, socket_timeout=5)
    return g.redis

@app.route("/", methods=['POST','GET'])
def hello():
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote = None

    if request.method == 'POST':
        redis = get_redis()
        vote = request.form['vote']
        app.logger.info('Received vote for %s', vote)
        data = json.dumps({'voter_id': voter_id, 'vote': vote})
        redis.rpush('votes', data)

    resp = make_response(render_template(
        'index.html',
        option_a=option_a,
        option_b=option_b,
        option_c=option_c,
        option_a_icon=option_a_icon,
        option_b_icon=option_b_icon,
        option_c_icon=option_c_icon,
        option_a_bgcolor=option_a_bgcolor,
        option_b_bgcolor=option_b_bgcolor,
        option_c_bgcolor=option_c_bgcolor,
        hostname=hostname,
        vote=vote,
    ))
    resp.set_cookie('voter_id', voter_id)
    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)