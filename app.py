# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import json, threading

app = Flask(__name__)
CORS(app)  # 允许跨域，若不需要可删

DATA_FILE = 'machines.json'
lock = threading.Lock()

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with lock:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/status', methods=['GET'])
def status():
    machine_id = request.args.get('machine_id')
    item_name = request.args.get('item_name')
    data = load_data()
    machine = data.get(machine_id)
    if not machine:
        return jsonify({"error": "Machine not found"}), 404

    if item_name:
        item = machine['items'].get(item_name)
        if not item:
            return jsonify({"error": "Item not found"}), 404
        return jsonify({"item": item_name, "count": item['count']})

    return jsonify(machine['items'])

@app.route('/win', methods=['POST'])
def win():
    body = request.get_json()
    mid = body.get('machine_id')
    name = body.get('item_name')
    data = load_data()
    machine = data.get(mid)
    if not machine or name not in machine['items']:
        return jsonify({"error": "Machine or Item not found"}), 404

    machine['items'][name]['wins'] += 1
    machine['items'][name]['count'] -= 1
    save_data(data)
    return jsonify({"message": "Win recorded", "item": name, "new_count": machine['items'][name]['count']})

@app.route('/restock', methods=['POST'])
def restock():
    body = request.get_json()
    mid = body.get('machine_id')
    name = body.get('item_name')
    amount = body.get('amount', 0)
    data = load_data()
    machine = data.get(mid)
    if not machine or name not in machine['items']:
        return jsonify({"error": "Machine or Item not found"}), 404

    machine['items'][name]['count'] += amount
    save_data(data)
    return jsonify({"message": "Restocked", "item": name, "new_count": machine['items'][name]['count']})

@app.route('/ranking', methods=['GET'])
def ranking():
    data = load_data()
    ranking = []
    for mid, info in data.items():
        for name, stats in info['items'].items():
            ranking.append({"item": name, "wins": stats['wins']})
    ranking.sort(key=lambda x: x['wins'], reverse=True)
    return jsonify(ranking)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
