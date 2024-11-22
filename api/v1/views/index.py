#!/usr/bin/python3
"""Create index routes"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """Sends ok status"""
    return jsonify({"status": "OK"})
