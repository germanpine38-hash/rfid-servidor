from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Lista que guarda todos los ticks recibidos
ticks = []

@app.route("/tick", methods=["POST"])
def recibir_tick():
    """La Raspberry Pi manda el tick acá"""
    datos = request.get_json()

    if not datos or "uid" not in datos:
        return jsonify({"error": "Datos inválidos"}), 400

    tick = {
        "uid": datos["uid"],
        "timestamp": datos.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        "recibido_en": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    ticks.append(tick)
    print(f"📡 Tick recibido — UID: {tick['uid']} — {tick['timestamp']}")

    return jsonify({"status": "ok"}), 200


@app.route("/ticks", methods=["GET"])
def ver_ticks():
    """El celular consulta acá para ver los ticks"""
    return jsonify(ticks), 200


@app.route("/ticks/ultimo", methods=["GET"])
def ver_ultimo():
    """Devuelve solo el tick más reciente"""
    if ticks:
        return jsonify(ticks[-1]), 200
    return jsonify({"mensaje": "Sin ticks todavía"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)