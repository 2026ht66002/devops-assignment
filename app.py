from flask import Flask, jsonify, request

app = Flask(__name__)

MEMBERS = [
    {"member_id": "M101", "name": "Aisha Nair",
        "status": "active", "plan": "Premium"},
    {"member_id": "M102", "name": "Rahul Sharma",
        "status": "active", "plan": "Basic"},
    {"member_id": "M103", "name": "Priya Menon",
        "status": "active", "plan": "Elite"},
    {"member_id": "M104", "name": "Karan Singh",
        "status": "inactive", "plan": "Basic"},
]

PLANS = [
    {"name": "Basic", "fee": 799, "access": "Gym floor & cardio"},
    {"name": "Premium", "fee": 1499, "access": "Gym, group classes & trainer support"},
    {"name": "Elite", "fee": 2499, "access": "All access + nutrition consultations"},
]


@app.route('/')
def home():
    return """
    <!doctype html>
    <html lang=\"en\">
    <head>
        <meta charset=\"UTF-8\" />
        <title>ACEest Fitness & Gym</title>
    </head>
    <body>
        <h1>ACEest Fitness & Gym</h1>
        <p>Welcome to the DevOps assignment application.</p>
        <p>Health endpoint: /health</p>
        <p>Members endpoint: /members</p>
        <p>Plans endpoint: /plans</p>
    </body>
    </html>
    """


@app.route('/health')
def health():
    return jsonify({"status": "ok", "service": "aceest-fitness-gym"})


@app.route('/members')
def get_members():
    return jsonify({"members": MEMBERS})


@app.route('/plans')
def get_plans():
    return jsonify({"plans": PLANS})


@app.route('/checkin', methods=['POST'])
def check_in():
    payload = request.get_json(silent=True) or {}
    member_id = payload.get('member_id')

    if not member_id:
        return jsonify({"error": "member_id is required"}), 400

    member = next(
        (item for item in MEMBERS if item['member_id'] == member_id), None)
    if member is None:
        return jsonify({"error": f"Member {member_id} not found"}), 404

    member['last_checkin'] = 'checked_in'
    return jsonify({
        "member_id": member_id,
        "status": "checked_in",
        "name": member['name'],
        "plan": member['plan'],
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
