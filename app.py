from flask import Flask, render_template, jsonify, request
import time

app = Flask(__name__)

# Globaler Timer-Status
start_time = None
laps = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    global start_time, laps
    if start_time is None:
        start_time = time.time()
        laps = []
    return jsonify({"status": "started"})

@app.route("/stop", methods=["POST"])
def stop():
    global start_time
    if start_time is not None:
        elapsed = time.time() - start_time
        start_time = None
        return jsonify({"status": "stopped", "elapsed": elapsed})
    return jsonify({"status": "not_running"})

@app.route("/lap", methods=["POST"])
def lap():
    global laps, start_time
    if start_time is None:
        return jsonify({"status": "not_running"})
    elapsed = time.time() - start_time
    laps.append(elapsed)
    return jsonify({"status": "lap_recorded", "lap_time": elapsed, "lap_number": len(laps)})

@app.route("/reset", methods=["POST"])
def reset():
    global start_time, laps
    start_time = None
    laps = []
    return jsonify({"status": "reset"})

if __name__ == "__main__":
    app.run(debug=True)