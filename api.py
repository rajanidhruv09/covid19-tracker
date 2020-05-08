import os

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from backend import db

app = Flask(__name__,
            static_folder='frontend/dist',
            template_folder="frontend")
CORS(app)

app.config.from_object(os.environ['APP_SETTINGS'])


@app.route('/')
def root():
    return render_template("index.html")


@app.route("/stats", methods=["GET"])
def get_stats_for_country():
    country = request.args.get('country')
    return db.get_country_data(country)


@app.route("/allStats", methods=["GET"])
def get_world_wide_stats():
    return jsonify(db.get_world_wide_stats())


if __name__ == '__main__':
    app.run()
