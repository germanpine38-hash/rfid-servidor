from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# ── Estado del conteo ─────────────────────────────────────
conteo_activo = False
animales_presentes = {}  # { uid: { "nombre": ..., "hora": ... } }

# ── Asociación UID → animal (luego vendrá de Supabase) ────
registro_animales = {
    "147-24-83-210": "Animal 001",
    "52-99-17-188":  "Animal 002",
    "200-45-130-77": "Animal 003",
}
# ─────────────────────────────────────────────────────────

@app.route("/conteo/iniciar", methods=["POST"])
def iniciar_conteo():
    global conteo_activo, animales_presentes
    conteo_activo = True
    animales_presentes = {}
    print("▶️  Conteo iniciado")
    return jsonify({"status": "conteo iniciado"}), 200


@app.route("/conteo/detener", methods=["POST"])
def detener_conteo():
    global conteo_activo
    conteo_activo = False
    print("⏹️  Conteo detenido")
    return jsonify({"status": "conteo detenido"}), 200


@app.route("/tick", methods=["POST"])
def recibir_tick():
    if not conteo_activo:
        return jsonify({"status": "conteo no activo"}), 200

    datos = request.get_json()
    if not datos or "uid" not in datos:
        return jsonify({"error": "Datos inválidos"}), 400

    uid_str = "-".join(str(x) for x in datos["uid"])
    nombre = registro_animales.get(uid_str, f"Desconocido ({uid_str})")

    animales_presentes[uid_str] = {
        "nombre": nombre,
        "hora": datetime.now().strftime("%H:%M:%S")
    }

    print(f"✅ {nombre} detectado — {animales_presentes[uid_str]['hora']}")
    return jsonify({"status": "ok", "animal": nombre}), 200


@app.route("/conteo/estado", methods=["GET"])
def ver_estado():
    return jsonify({
        "conteo_activo": conteo_activo,
        "animales_presentes": animales_presentes
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)