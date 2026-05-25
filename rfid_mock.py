import random
import time

TARJETAS_SIMULADAS = {
    (147, 24, 83, 210): "Tarjeta A - Acceso permitido",
    (52,  99, 17, 188): "Tarjeta B - Acceso permitido",
    (200, 45, 130, 77): "Tarjeta C - Acceso denegado",
}

class RFIDMock:
    def __init__(self):
        self.deteccion_activa = False
        self.tarjeta_actual = None

    def simular_acercamiento(self, uid=None):
        if uid is None:
            self.tarjeta_actual = random.choice(list(TARJETAS_SIMULADAS.keys()))
        else:
            self.tarjeta_actual = uid
        self.deteccion_activa = True
        print(f"[SIMULADOR] Tarjeta acercada: UID {list(self.tarjeta_actual)}")

    def simular_retiro(self):
        self.deteccion_activa = False
        self.tarjeta_actual = None
        print("[SIMULADOR] Tarjeta retirada")

    def read_no_block(self):
        if self.deteccion_activa and self.tarjeta_actual:
            return (0x10, list(self.tarjeta_actual))
        return (None, None)