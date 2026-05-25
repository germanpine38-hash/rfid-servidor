import time
import requests
import threading
from rfid_mock import RFIDMock

# ─── Configuración ───────────────────────────────────────
URL_SERVIDOR = "https://web-production-3c67.up.railway.app/tick"  # Reemplazá con tu URL
TIEMPO_IGNORAR = 5
# ─────────────────────────────────────────────────────────

lector = RFIDMock()
ultimas_lecturas = {}

def ya_fue_leida_recientemente(uid):
    uid_str = str(uid)
    ahora = time.time()
    if uid_str in ultimas_lecturas:
        tiempo_pasado = ahora - ultimas_lecturas[uid_str]
        if tiempo_pasado < TIEMPO_IGNORAR:
            print(f"⏱️  Tarjeta ignorada, esperá {TIEMPO_IGNORAR - int(tiempo_pasado)}s")
            return True
    ultimas_lecturas[uid_str] = ahora
    return False

def mandar_tick(uid):
    payload = {
        "uid": uid,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        respuesta = requests.post(URL_SERVIDOR, json=payload, timeout=5)
        if respuesta.status_code == 200:
            print(f"✅ Tick enviado — UID: {uid}")
        else:
            print(f"⚠️  Error del servidor: {respuesta.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar al servidor")
    except requests.exceptions.Timeout:
        print("❌ El servidor no respondió a tiempo")

def bucle_principal():
    print("🔄 Esperando tarjetas RFID...\n")
    while True:
        estado, uid = lector.read_no_block()
        if uid:
            if not ya_fue_leida_recientemente(uid):
                mandar_tick(uid)
        time.sleep(0.5)

def simular_eventos():
    time.sleep(1)
    lector.simular_acercamiento((147, 24, 83, 210))
    time.sleep(3)
    lector.simular_retiro()
    time.sleep(1)
    lector.simular_acercamiento((52, 99, 17, 188))
    time.sleep(3)
    lector.simular_retiro()

if __name__ == "__main__":
    hilo_lectura = threading.Thread(target=bucle_principal, daemon=True)
    hilo_eventos = threading.Thread(target=simular_eventos)
    hilo_lectura.start()
    hilo_eventos.start()
    hilo_eventos.join()
    time.sleep(1)
    print("\n✔️  Simulación completada")