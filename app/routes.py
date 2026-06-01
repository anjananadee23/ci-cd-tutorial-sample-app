from flask import json, jsonify
from app import app
from app import db
from app.models import Menu

@app.route('/')
def home():
    return jsonify({ "status": "ok", "message": "Welcome to the CI/CD tutorial sample app" })

@app.route('/menu')
def menu():
    today = Menu.query.first()
    if today:
        body = { "today_special": today.name }
        status = 200
    else:
        body = { "error": "Sorry, the service is not available today." }
        status = 404
    return jsonify(body), status


@app.route('/health')
def health():
    return jsonify({ "status": "ok", "version": "1.1" })