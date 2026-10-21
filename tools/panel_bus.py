"""Panel en el navegador para leer el bus J1939 de la EC210B con el portátil (docs/CAPTURA_CAN.md).

Lee el bus con el adaptador SH-C30A (candleLight / gs_usb) SIEMPRE en solo escucha y muestra
en directo rpm, par, temperaturas, averías (DM1), nodos y la tabla de mensajes. Graba las
capturas en el mismo formato que tools/captura_can.py (candump -l, con notas) y las analiza.

    python tools/panel_bus.py                      (adaptador SH-C30A, abre http://127.0.0.1:8766)
    python tools/panel_bus.py --demo               (E-ECU simulada, para probar sin máquina)
    python tools/panel_bus.py --reproducir capturas/2026-10-25_..._03_ralenti.log

Dependencias: tools/requirements.txt (gs_usb, pyusb, libusb-package).
"""
import argparse
import csv
import datetime as dt
import json
import math
import os
import queue
import random
import re
import signal
import sys
import threading
import time
import webbrowser
from collections import deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import captura_can as cc  # noqa: E402  (decodificación J1939 y análisis compartidos)

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
HTML = os.path.join(AQUI, "panel_bus.html")
CARPETA = os.path.join(RAIZ, "capturas")
CARPETA_REG = os.path.join(RAIZ, "registros", "bus")
BITS_TRAMA = 130  # trama extendida de 8 bytes con relleno de bits (igual que captura_can.py)
MUESTREO_S = 0.2  # puntos de la gráfica: 5 por segundo
MAX_PUNTOS = 3000  # 10 minutos

PRUEBAS = [  # docs/CAPTURA_CAN.md §4
    {"nombre": "01_contacto", "duracion": 60, "que": "Llave en contacto, motor parado"},
    {"nombre": "02_arranque", "duracion": 60, "que": "Empezar antes de girar la llave"},
    {"nombre": "03_ralenti", "duracion": 120, "que": "Motor a ralentí (interruptor 26 en ralentí)"},
    {"nombre": "04_alta", "duracion": 120, "que": "Interruptor 26 en ALTA"},
    {"nombre": "05_carga", "duracion": 120, "que": "En alta moviendo brazo y cuchara"},
    {"nombre": "06_parada", "duracion": 60, "que": "Vuelta a ralentí y parada"},
]


class FuenteError(Exception):
    def __init__(self, msg, fatal=False):
        super().__init__(msg)
        self.fatal = fatal


def v1(b, escala=1.0, offset=0.0):
    return None if b >= 0xFB else b * escala + offset


def v2(lo, hi, escala=1.0, offset=0.0):
    x = lo | hi << 8
    return None if x >= 0xFB00 else x * escala + offset


# ------------------------------------------------------------------ fuentes de tramas
# Cada fuente es un iterador que devuelve (ts, id, extendida, remota, datos) o None si no hay
# trama en ese momento (para que el bucle pueda atender el resto), y una descripción.

class Adaptador:
    """SH-C30A (gs_usb) en solo escucha: no transmite ni confirma tramas."""

    def __init__(self):
        import libusb_package
        import usb.core
        from gs_usb.constants import GS_CAN_MODE_HW_TIMESTAMP, GS_CAN_MODE_LISTEN_ONLY
        from gs_usb.gs_usb import GsUsb
        from gs_usb.gs_usb_frame import GsUsbFrame

        backend = libusb_package.get_libusb1_backend()
        devs = list(usb.core.find(find_all=True, backend=backend, custom_match=GsUsb.is_gs_usb_device))
        if not devs:
            raise FuenteError("No se encuentra el SH-C30A. ¿Está enchufado con el interruptor 1 (arranque) en OFF?")
        self.dev = GsUsb(devs[0])
        if not self.dev.set_bitrate(cc.BITRATE):
            raise FuenteError("El adaptador no admite 250 kbit/s.", fatal=True)
        self.dev.start(GS_CAN_MODE_LISTEN_ONLY | GS_CAN_MODE_HW_TIMESTAMP)
        if not self.dev.device_flags & GS_CAN_MODE_LISTEN_ONLY:
            self.dev.stop()
            raise FuenteError("ABORTADO: el adaptador no admite el modo solo escucha. No se lee el bus "
                              "para no transmitir en la máquina.", fatal=True)
        self.frame = GsUsbFrame()
        self.t_hw0 = None
        self.errores = 0
        self.descripcion = f"SH-C30A · {self.dev}"

    def leer(self):
        f = self.frame
        if not self.dev.read(f, 100):
            return None
        if f.is_error_frame:
            self.errores += 1
            return None
        if f.echo_id != 0xFFFFFFFF:
            return None
        ahora = time.time()
        if self.t_hw0 is None:
            self.t_hw0 = (ahora, f.timestamp_us)
        ts = self.t_hw0[0] + ((f.timestamp_us - self.t_hw0[1]) & 0xFFFFFFFF) / 1e6
        return ts, f.arbitration_id, f.is_extended_id, f.is_remote_frame, bytes(f.data[:f.can_dlc])

    def cerrar(self):
        try:
            self.dev.stop()
        except Exception:
            pass


class Demo:
    """E-ECU simulada: contacto → arranque → ralentí → alta con ciclos de trabajo → ralentí."""

    descripcion = "DEMO · E-ECU simulada (no es la máquina)"
    errores = 0

    def __init__(self):
        self.t0 = time.time()
        self.prox = {}
        self.rpm = 0.0
        self.par = 0.0
        self.temp = 35.0
        self.horas = 8123.4

    def objetivo(self, t):
        c = t % 150
        if c < 8:
            return 0, 0            # contacto
        if c < 11:
            return 250, 30         # arranque
        if c < 40:
            return 800, 7          # ralentí
        if c < 130:                # alta: trabajo a ratos
            trabajo = (c - 40) % 30 < 18
            return 1900, (35 + 30 * math.sin(c)) if trabajo else 11
        return 800, 7

    def tramas(self, ahora):
        t = ahora - self.t0
        r_obj, p_obj = self.objetivo(t)
        self.rpm += (r_obj - self.rpm) * 0.08 + random.uniform(-4, 4) * (r_obj > 0)
        self.rpm = max(self.rpm, 0)
        self.par += (p_obj - self.par) * 0.15 + random.uniform(-1, 1) * (r_obj > 0)
        self.temp = min(82, self.temp + 0.002 * (self.rpm > 500))
        self.horas += 1 / 3600 / 50
        marcha = self.rpm > 100
        out = []

        def toca(clave, periodo):
            if ahora >= self.prox.get(clave, 0):
                self.prox[clave] = ahora + periodo
                return True
            return False

        if toca("eec1", 0.02):
            crudo = int(self.rpm / 0.125)
            par = int(max(-125, min(125, self.par))) + 125
            out.append((0x0CF00400, bytes([0xF0, 0x7D, par, crudo & 0xFF, crudo >> 8, 0x00, 0xFF, 0xFF])))
        if toca("eec2", 0.05):
            carga = int(max(0, min(100, self.par * 1.1)))
            out.append((0x0CF00300, bytes([0xFF, 0x00, carga, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])))
        if toca("et1", 1.0):
            out.append((0x18FEEE00, bytes([int(self.temp) + 40, 0x55, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])))
        if toca("eflp1", 0.5):
            aceite = int((380 if marcha else 0) / 4 + random.uniform(-2, 2) * marcha)
            out.append((0x18FEEF00, bytes([0xFF, 0xFF, 0xFF, max(aceite, 0), 0xFF, 0xFF, 0xFF, 0xFF])))
        if toca("vep1", 1.0):
            v = int((27.8 if marcha else 24.6) / 0.05)
            out.append((0x18FEF700, bytes([0xFF, 0xFF, 0xFF, 0xFF, v & 0xFF, v >> 8, 0xFF, 0xFF])))
        if toca("hours", 1.0):
            h = int(self.horas / 0.05)
            out.append((0x18FEE500, h.to_bytes(4, "little") + b"\xFF\xFF\xFF\xFF"))
        if toca("dm1", 1.0):  # avería de ejemplo: SPN 639 FMI 9 (red J1939, frecuencia anormal)
            out.append((0x18FECA00, bytes([0x04, 0xFF, 0x7F, 0x02, 0x09, 0x03, 0xFF, 0xFF])))
        if toca("panel", 1.0):
            out.append((0x18FEFC17, bytes([0xFF, 0x96, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])))
        return [(ahora, i, True, False, d) for i, d in out]

    def leer(self):
        pend = getattr(self, "_pend", [])
        if not pend:
            time.sleep(0.005)
            pend = self.tramas(time.time())
        self._pend = pend[1:]
        return pend[0] if pend else None

    def cerrar(self):
        pass


class Reproduccion:
    """Reproduce un .log grabado a velocidad real (o más rápido) y vuelve a empezar al terminar."""

    errores = 0

    def __init__(self, ruta, velocidad=1.0):
        self.tramas, self.notas = cc.leer_log(ruta)
        if not self.tramas:
            raise FuenteError(f"{ruta}: sin tramas.", fatal=True)
        self.velocidad = velocidad
        self.descripcion = f"Reproducción · {os.path.basename(ruta)}"
        self.reiniciar()

    def reiniciar(self):
        self.i = 0
        self.t_inicio = time.time()

    def leer(self):
        if self.i >= len(self.tramas):
            time.sleep(1.0)
            self.reiniciar()
            return None
        ts, ident, ext, datos = self.tramas[self.i]
        t_log0 = self.tramas[0][0]
        espera = (ts - t_log0) / self.velocidad - (time.time() - self.t_inicio)
        if espera > 0:
            time.sleep(min(espera, 0.1))
            return None
        self.i += 1
        return time.time(), ident, ext, False, datos

    def cerrar(self):
        pass


# ------------------------------------------------------------------ registro automático de la sesión

class Registro:
    """Todo lo de la sesión en registros/bus/<fecha>_<hora>/, sin tener que pulsar Grabar:
    bus_completo.log (todas las tramas y notas, formato de captura_can.py), motor.csv (1 por segundo)
    y eventos.log (conexiones, nodos, averías, notas, grabaciones y un resumen cada 10 s)."""

    COLUMNAS = ["hora", "rpm", "par_pct", "carga_pct", "refrigerante_c", "aceite_kpa", "bateria_v",
                "tramas_s", "errores_bus", "grabando", "nota"]

    def __init__(self, descripcion, sufijo=""):
        self.carpeta = os.path.join(CARPETA_REG, f"{dt.datetime.now():%Y-%m-%d_%H%M%S}{sufijo}")
        os.makedirs(self.carpeta, exist_ok=True)
        self.raw = open(os.path.join(self.carpeta, "bus_completo.log"), "w", encoding="utf-8")
        self.raw.write(f"# sesión completa · {dt.datetime.now().isoformat(timespec='seconds')} · "
                       f"{cc.BITRATE} bit/s · solo escucha · {descripcion}\n")
        self.csv = open(os.path.join(self.carpeta, "motor.csv"), "w", encoding="utf-8", newline="")
        self.csvw = csv.writer(self.csv)
        self.csvw.writerow(self.COLUMNAS)
        self.ev = open(os.path.join(self.carpeta, "eventos.log"), "w", encoding="utf-8", buffering=1)
        self.notas_pendientes = []
        self.tramas = 0
        self.evento(f"Inicio de sesión · {descripcion}")

    def ruta(self):
        return os.path.relpath(self.carpeta, RAIZ)

    def evento(self, texto):
        self.ev.write(f"{dt.datetime.now():%Y-%m-%d %H:%M:%S} · {texto}\n")

    def trama(self, ts, ident, ext, remota, datos):
        fmt_id = f"{ident:08X}" if ext else f"{ident:03X}"
        self.raw.write(f"({ts:.6f}) can0 {fmt_id}{'#R' if remota else '#'}{datos.hex().upper()}\n")
        self.tramas += 1

    def nota(self, ts, texto):
        self.raw.write(f"# ({ts:.6f}) {texto}\n")
        self.notas_pendientes.append(texto)
        self.evento(f"NOTA: {texto}")

    def muestra(self, motor, frescos, fps, errores, grabando):
        def val(clave, dec):
            v = motor.get(clave)
            return "" if v is None or not frescos.get(clave) else round(v, dec)
        self.csvw.writerow([dt.datetime.now().strftime("%H:%M:%S"), val("rpm", 0), val("par", 0), val("carga", 0),
                            val("refrigerante", 0), val("aceiteKpa", 0), val("bateriaV", 2), fps, errores,
                            grabando or "", " | ".join(self.notas_pendientes)])
        self.notas_pendientes = []
        self.raw.flush()
        self.csv.flush()

    def cerrar(self, motivo):
        self.evento(f"Fin de sesión ({motivo}) · {self.tramas} tramas guardadas")
        for f in (self.raw, self.csv, self.ev):
            f.close()


# ------------------------------------------------------------------ estado del bus

class Bus:
    def __init__(self, crear_fuente, demo=False, registro=None):
        self.registro = registro
        self.crear_fuente = crear_fuente
        self.demo = demo
        self.fuente = None
        self.error = None
        self.fatal = False
        self.lock = threading.Lock()
        self.reiniciar_estadisticas()
        self.puntos = deque(maxlen=MAX_PUNTOS)  # (seq, t, rpm, par)
        self.seq = 0
        self.notas = deque(maxlen=200)          # (t, texto)
        self.grab = None                         # grabación en curso
        self.grabaciones = []                    # rutas grabadas en esta sesión
        self.mensajes_sistema = deque(maxlen=50)

    def reiniciar_estadisticas(self):
        self.ids = {}
        self.nodos = {}
        self.total = 0
        self.t_rate = deque()
        self.motor = {}
        self.t_motor = {}
        self.averias = {}
        self.bam = {}
        self.tsc1 = False
        self.t_inicio = time.time()

    def sistema(self, texto):
        self.mensajes_sistema.append({"t": time.strftime("%H:%M:%S"), "texto": texto})
        if self.registro:
            self.registro.evento(texto)

    # ---------------------------------------------------------------- tramas
    def procesar(self, ts, ident, ext, remota, datos):
        self.total += 1
        self.t_rate.append(ts)
        clave = (ident, ext)
        e = self.ids.get(clave)
        if e is None:
            if len(self.ids) >= 300:
                return
            e = self.ids[clave] = {"n": 0, "t0": ts, "tu": ts, "per": None, "primero": datos, "ultimo": datos,
                                   "cambian": 0}
        else:
            dtp = ts - e["tu"]
            if dtp > 0:
                e["per"] = dtp if e["per"] is None else e["per"] * 0.9 + dtp * 0.1
        e["n"] += 1
        e["tu"] = ts
        for i, b in enumerate(datos):
            if i >= len(e["ultimo"]) or e["ultimo"][i] != b:
                e["cambian"] |= 1 << i
        e["ultimo"] = datos
        if not ext:
            return
        _, pgn, _, sa = cc.descomponer(ident)
        if sa not in self.nodos and self.registro:
            aviso = " ⚠️ ¿V-ECU conectada?" if sa == 0x11 else ""
            self.registro.evento(f"Nodo nuevo en el bus: {cc.nombre_dir(sa)} (primera trama {ident:08X}){aviso}")
        nodo = self.nodos.setdefault(sa, {"n": 0, "tu": ts})
        nodo["n"] += 1
        nodo["tu"] = ts
        if pgn == 0:
            if not self.tsc1 and self.registro:
                self.registro.evento(f"⚠️ TSC1 en el bus ({ident:08X}): alguien pide régimen al motor")
            self.tsc1 = True
        if sa != 0:
            self.decodificar_comun(pgn, sa, datos)
            return
        d = datos
        m, t = self.motor, self.t_motor
        if pgn == 61444 and len(d) >= 5:      # EEC1
            m["rpm"], m["par"] = v2(d[3], d[4], 0.125), v1(d[2], 1, -125)
            t["rpm"] = t["par"] = ts
        elif pgn == 61443 and len(d) >= 3:    # EEC2
            m["acelerador"], m["carga"] = v1(d[1], 0.4), v1(d[2], 1)
            t["carga"] = t["acelerador"] = ts
        elif pgn == 65262 and len(d) >= 1:    # ET1
            m["refrigerante"] = v1(d[0], 1, -40)
            m["combustibleC"] = v1(d[1], 1, -40) if len(d) >= 2 else None
            t["refrigerante"] = t["combustibleC"] = ts
        elif pgn == 65263 and len(d) >= 4:    # EFL/P1
            m["aceiteKpa"] = v1(d[3], 4)
            t["aceiteKpa"] = ts
        elif pgn == 65271 and len(d) >= 6:    # VEP1
            m["bateriaV"] = v2(d[4], d[5], 0.05)
            t["bateriaV"] = ts
        elif pgn == 65253 and len(d) >= 4:    # HOURS
            x = int.from_bytes(d[:4], "little")
            m["horas"] = None if x >= 0xFB000000 else x * 0.05
            t["horas"] = ts
        elif pgn == 65266 and len(d) >= 2:    # LFE
            m["consumoLh"] = v2(d[0], d[1], 0.05)
            t["consumoLh"] = ts
        self.decodificar_comun(pgn, sa, datos)

    def decodificar_comun(self, pgn, sa, d):
        if pgn == 65226 and len(d) >= 6:     # DM1 de una trama
            self.fijar_dm1(sa, d)
        elif pgn == 60416 and len(d) == 8 and d[0] == 0x20:   # BAM que anuncia un DM1 largo
            if (d[5] | d[6] << 8 | d[7] << 16) == 65226:
                self.bam[sa] = {"tam": d[1] | d[2] << 8, "paq": d[3], "datos": {}}
        elif pgn == 60160 and sa in self.bam and d:
            b = self.bam[sa]
            b["datos"][d[0]] = d[1:8]
            if len(b["datos"]) >= b["paq"]:
                completo = b"".join(b["datos"][i] for i in sorted(b["datos"]))[:b["tam"]]
                del self.bam[sa]
                self.fijar_dm1(sa, completo)

    def fijar_dm1(self, sa, d):
        l = d[0]
        if self.registro:
            antes = {(x["spn"], x["fmi"]) for x in self.averias.get(sa, {}).get("dtc", [])}
            ahora = {(s_, f_) for s_, f_, _ in cc.dtcs(d)}
            for s_, f_ in sorted(ahora - antes):
                self.registro.evento(f"Avería ACTIVA en {cc.nombre_dir(sa)}: SPN {s_} FMI {f_} (lámparas 0x{l:02X})")
            for s_, f_ in sorted(antes - ahora):
                self.registro.evento(f"Avería ya no activa en {cc.nombre_dir(sa)}: SPN {s_} FMI {f_}")
        self.averias[sa] = {"lamparas": {"MIL": (l >> 6) & 3 == 1, "parada": (l >> 4) & 3 == 1,
                                         "aviso": (l >> 2) & 3 == 1, "proteccion": l & 3 == 1},
                            "dtc": [{"spn": s, "fmi": f, "oc": o} for s, f, o in cc.dtcs(d)],
                            "t": time.time()}

    # ---------------------------------------------------------------- grabación
    def grabar(self, nombre, duracion):
        nombre = re.sub(r"[^\w\-]+", "_", nombre.strip())[:40].strip("_") or "captura"
        if self.grab:
            return False, "Ya hay una grabación en curso."
        if not self.fuente:
            return False, "No hay conexión con el bus."
        carpeta = os.path.join(CARPETA, "demo") if self.demo else CARPETA
        os.makedirs(carpeta, exist_ok=True)
        ruta = os.path.join(carpeta, f"{dt.datetime.now():%Y-%m-%d_%H%M%S}_{nombre}.log")
        f = open(ruta, "w", encoding="utf-8")
        f.write(f"# captura {nombre} · {dt.datetime.now().isoformat(timespec='seconds')} · {cc.BITRATE} bit/s · "
                f"solo escucha · {self.fuente.descripcion}\n")
        self.grab = {"ruta": ruta, "f": f, "nombre": nombre, "t0": time.time(), "duracion": duracion or None,
                     "tramas": 0, "ultimo_flush": time.time()}
        self.sistema(f"Grabando {os.path.relpath(ruta, RAIZ)}")
        return True, None

    def parar(self, motivo="parada a mano"):
        g = self.grab
        if not g:
            return
        self.grab = None
        g["f"].close()
        self.grabaciones.append({"ruta": os.path.relpath(g["ruta"], RAIZ), "nombre": g["nombre"],
                                 "tramas": g["tramas"], "segundos": round(time.time() - g["t0"])})
        self.sistema(f"Grabación terminada ({motivo}): {g['tramas']} tramas")

    def nota(self, texto):
        texto = " ".join(texto.split())[:120]
        if not texto:
            return False, "Nota vacía."
        ahora = time.time()
        self.notas.append((ahora, texto))
        if self.registro:
            self.registro.nota(ahora, texto)
        if self.grab:
            self.grab["f"].write(f"# ({ahora:.6f}) {texto}\n")
        return True, None

    def escribir(self, ts, ident, ext, remota, datos):
        g = self.grab
        if not g:
            return
        fmt_id = f"{ident:08X}" if ext else f"{ident:03X}"
        g["f"].write(f"({ts:.6f}) can0 {fmt_id}{'#R' if remota else '#'}{datos.hex().upper()}\n")
        g["tramas"] += 1

    # ---------------------------------------------------------------- bucle de lectura
    def bucle(self):
        ultimo_punto = ultima_muestra = ultimo_resumen = 0.0
        while True:
            if not self.fuente:
                if self.fatal:
                    time.sleep(1)
                    continue
                try:
                    self.fuente = self.crear_fuente()
                    self.error = None
                    self.sistema(f"Conectado: {self.fuente.descripcion}")
                except FuenteError as ex:
                    self.error, self.fatal = str(ex), ex.fatal
                    time.sleep(2)
                    continue
                except Exception as ex:  # USB sin permisos, librería que falta…
                    self.error = f"No se pudo abrir el adaptador: {ex}"
                    time.sleep(2)
                    continue
            try:
                tr = self.fuente.leer()
            except Exception as ex:
                self.sistema(f"Se perdió el adaptador ({ex}). Reintentando…")
                self.parar("adaptador desconectado")
                self.fuente.cerrar()
                self.fuente = None
                continue
            with self.lock:
                if tr:
                    self.escribir(*tr)
                    if self.registro:
                        self.registro.trama(*tr)
                    self.procesar(*tr)
                ahora = time.time()
                if self.registro and ahora - ultima_muestra >= 1.0:
                    ultima_muestra = ahora
                    self.registrar(ahora, resumen=ahora - ultimo_resumen >= 10.0)
                    if ahora - ultimo_resumen >= 10.0:
                        ultimo_resumen = ahora
                g = self.grab
                if g:
                    if g["duracion"] and ahora - g["t0"] >= g["duracion"]:
                        self.parar("duración cumplida")
                    elif ahora - g["ultimo_flush"] > 1:
                        g["f"].flush()
                        g["ultimo_flush"] = ahora
                if ahora - ultimo_punto >= MUESTREO_S:
                    ultimo_punto = ahora
                    fresco = ahora - self.t_motor.get("rpm", 0) < 1.0
                    self.seq += 1
                    self.puntos.append((self.seq, round(ahora, 2),
                                        self.motor.get("rpm") if fresco else None,
                                        self.motor.get("par") if fresco else None))

    def registrar(self, ahora, resumen):
        while self.t_rate and ahora - self.t_rate[0] > 1.0:
            self.t_rate.popleft()
        fps = len(self.t_rate)
        frescos = {k: ahora - t < 3.0 for k, t in self.t_motor.items()}
        errores = getattr(self.fuente, "errores", 0) if self.fuente else 0
        self.registro.muestra(self.motor, frescos, fps, errores, self.grab["nombre"] if self.grab else None)
        if resumen:
            m = self.motor

            def f(clave, suf, dec=0):
                v = m.get(clave)
                return "—" if v is None or not frescos.get(clave) else f"{v:.{dec}f}{suf}"
            self.registro.evento(
                f"Resumen: {f('rpm', ' rpm')} · par {f('par', ' %')} · carga {f('carga', ' %')} · "
                f"refrig. {f('refrigerante', ' °C')} · aceite {f('aceiteKpa', ' kPa')} · batería {f('bateriaV', ' V', 1)} · "
                f"{fps} tramas/s · nodos {', '.join(f'0x{x:02X}' for x in sorted(self.nodos)) or '—'}"
                + (f" · {errores} errores de bus" if errores else "") + ("" if self.fuente else " · SIN ADAPTADOR"))

    # ---------------------------------------------------------------- foto para el navegador
    def foto(self, desde_seq):
        with self.lock:
            ahora = time.time()
            while self.t_rate and ahora - self.t_rate[0] > 1.0:
                self.t_rate.popleft()
            fps = len(self.t_rate)
            motor = {k: v for k, v in self.motor.items()}
            frescos = {k: ahora - t < 3.0 for k, t in self.t_motor.items()}
            ids = []
            for (ident, ext), e in sorted(self.ids.items()):
                fila = {"id": f"{ident:08X}" if ext else f"{ident:03X}", "n": e["n"],
                        "per": round(e["per"] * 1000) if e["per"] else None,
                        "datos": e["ultimo"].hex(" ").upper(), "cambian": e["cambian"],
                        "edad": round(ahora - e["tu"], 1)}
                if ext:
                    _, pgn, da, sa = cc.descomponer(ident)
                    fila.update(pgn=pgn, nombre=cc.NOMBRES_PGN.get(pgn, ""), origen=cc.nombre_dir(sa),
                                destino="global" if da == 0xFF else cc.nombre_dir(da))
                ids.append(fila)
            nodos = [{"sa": f"0x{sa:02X}", "nombre": cc.DIRECCIONES.get(sa, ""), "n": n["n"],
                      "edad": round(ahora - n["tu"], 1)} for sa, n in sorted(self.nodos.items())]
            averias = [{"sa": f"0x{sa:02X}", "nombre": cc.DIRECCIONES.get(sa, ""), **a,
                        "edad": round(ahora - a["t"], 1)} for sa, a in sorted(self.averias.items())]
            g = self.grab
            return {
                "fuente": {"conectado": self.fuente is not None, "descripcion": self.fuente.descripcion if self.fuente else None,
                           "error": self.error, "fatal": self.fatal, "demo": self.demo,
                           "erroresBus": getattr(self.fuente, "errores", 0) if self.fuente else 0},
                "bus": {"tramasS": fps, "carga": round(fps * BITS_TRAMA / cc.BITRATE * 100, 1), "total": self.total,
                        "tsc1": self.tsc1, "vecu": 0x11 in self.nodos},
                "motor": motor, "frescos": frescos, "ids": ids, "nodos": nodos, "averias": averias,
                "puntos": [p for p in self.puntos if p[0] > desde_seq],
                "notas": [{"t": round(t, 2), "texto": x} for t, x in self.notas],
                "grabacion": None if not g else {"nombre": g["nombre"], "ruta": os.path.relpath(g["ruta"], RAIZ),
                                                 "segundos": round(ahora - g["t0"]), "duracion": g["duracion"],
                                                 "tramas": g["tramas"]},
                "grabaciones": self.grabaciones[-20:],
                "sistema": list(self.mensajes_sistema)[-8:],
                "registro": self.registro.ruta() if self.registro else None,
                "ahora": round(ahora, 2),
            }


def crear_manejador(bus):
    class Manejador(BaseHTTPRequestHandler):
        server_version = "PanelBus/1.0"

        def log_message(self, *args):
            pass

        def responder(self, codigo, cuerpo, tipo="application/json; charset=utf-8"):
            datos = cuerpo if isinstance(cuerpo, bytes) else json.dumps(cuerpo).encode("utf-8")
            self.send_response(codigo)
            self.send_header("Content-Type", tipo)
            self.send_header("Content-Length", str(len(datos)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(datos)

        def do_GET(self):
            if self.path in ("/", "/index.html"):
                with open(HTML, "rb") as f:
                    self.responder(200, f.read(), "text/html; charset=utf-8")
            elif self.path == "/api/pruebas":
                self.responder(200, PRUEBAS)
            elif self.path == "/api/eventos":
                self.eventos()
            else:
                self.responder(404, {"error": "no existe"})

        def do_POST(self):
            origen = self.headers.get("Origin")
            if origen and not re.match(r"^http://(127\.0\.0\.1|localhost)(:\d+)?$", origen):
                return self.responder(403, {"error": "origen no permitido"})
            try:
                n = int(self.headers.get("Content-Length", 0))
                c = json.loads(self.rfile.read(min(n, 4096)) or b"{}")
            except (ValueError, json.JSONDecodeError):
                return self.responder(400, {"error": "JSON no válido"})
            ok, err, extra = True, None, {}
            with bus.lock:
                if self.path == "/api/grabar":
                    try:
                        dur = int(c.get("duracion") or 0)
                    except (TypeError, ValueError):
                        dur = 0
                    ok, err = bus.grabar(str(c.get("nombre", "")), max(0, min(dur, 3600)))
                elif self.path == "/api/parar":
                    bus.parar()
                elif self.path == "/api/nota":
                    ok, err = bus.nota(str(c.get("texto", "")))
                elif self.path == "/api/limpiar":
                    bus.sistema("Contadores, tabla y gráficas reiniciados desde el panel")
                    bus.reiniciar_estadisticas()
                    bus.puntos.clear()
                elif self.path == "/api/analizar":
                    ruta = os.path.realpath(os.path.join(RAIZ, str(c.get("ruta", ""))))
                    if not ruta.startswith(os.path.realpath(CARPETA) + os.sep) or not os.path.isfile(ruta):
                        ok, err = False, "Fichero no válido."
                    else:
                        extra["texto"] = "\n".join(cc.analizar_fichero(ruta))
                else:
                    return self.responder(404, {"error": "no existe"})
            self.responder(200 if ok else 409, {"ok": ok, "error": err, **extra})

        def eventos(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            seq = 0
            try:
                while True:
                    f = bus.foto(seq)
                    if f["puntos"]:
                        seq = f["puntos"][-1][0]
                    self.wfile.write(f"event: foto\ndata: {json.dumps(f)}\n\n".encode("utf-8"))
                    self.wfile.flush()
                    time.sleep(0.5)
            except (BrokenPipeError, ConnectionResetError, OSError):
                pass

    return Manejador


def main():
    ap = argparse.ArgumentParser(description="Panel en el navegador para leer el bus J1939 (solo escucha).")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--demo", action="store_true", help="E-ECU simulada, para probar sin máquina")
    g.add_argument("--reproducir", metavar="LOG", help="reproducir una captura .log")
    ap.add_argument("--velocidad", type=float, default=1.0, help="velocidad de la reproducción (1 = real)")
    ap.add_argument("--http", type=int, default=8766, help="puerto del panel en 127.0.0.1 (8766)")
    ap.add_argument("--no-abrir", action="store_true", help="no abrir el navegador")
    ap.add_argument("--sin-registro", action="store_true", help="no guardar el registro de la sesión en registros/bus/")
    args = ap.parse_args()

    if args.demo:
        crear = Demo
    elif args.reproducir:
        crear = lambda: Reproduccion(args.reproducir, args.velocidad)  # noqa: E731
    else:
        crear = Adaptador
    bus = Bus(crear, demo=args.demo or bool(args.reproducir))
    try:
        servidor = ThreadingHTTPServer(("127.0.0.1", args.http), crear_manejador(bus))
    except OSError:  # ya hay un panel en marcha en ese puerto: se abre ese
        url = f"http://127.0.0.1:{args.http}"
        print(f"El panel ya está en marcha: se abre {url}")
        if not args.no_abrir:
            webbrowser.open(url)
        return
    servidor.daemon_threads = True
    if not args.sin_registro and not args.reproducir:
        bus.registro = Registro("DEMO · E-ECU simulada" if args.demo else "SH-C30A", "_demo" if args.demo else "")
        print(f"Registro de la sesión en {bus.registro.ruta()}/")
    threading.Thread(target=bus.bucle, daemon=True).start()
    url = f"http://127.0.0.1:{args.http}"
    print(f"Panel del bus en {url}  (Ctrl+C para salir)")
    if not args.no_abrir:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    def _salir(*_):  # cerrar la ventana del terminal (SIGHUP) o SIGTERM: cerrar como con Ctrl+C
        raise KeyboardInterrupt
    for sig in ("SIGTERM", "SIGHUP"):
        if hasattr(signal, sig):
            signal.signal(getattr(signal, sig), _salir)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nCerrando panel.")
        with bus.lock:
            bus.parar("panel cerrado")
            if bus.registro:
                bus.registro.cerrar("panel cerrado")
        if bus.fuente:
            bus.fuente.cerrar()


if __name__ == "__main__":
    main()
