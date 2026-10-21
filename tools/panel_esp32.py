"""Panel en el navegador para el firmware V-ECU (firmware/esp32): modos, relé, ajustes y log.

Hace lo mismo que la consola serie (firmware/README.md) con botones:
    python tools/panel_esp32.py                  (abre http://127.0.0.1:8765)
    python tools/panel_esp32.py --puerto /dev/ttyACM0 --no-abrir

El panel es el único programa que abre el puerto serie (en exclusiva): cerrar antes
cualquier `platformio device monitor`. Si el programador se desenchufa y vuelve con
otro nombre (ttyACM0 → ttyACM1, COM5 → COM6), lo vuelve a encontrar solo.

Dependencias: pyserial (viene con PlatformIO; tools/requirements.txt).
"""
import argparse
import datetime as dt
import json
import os
import queue
import re
import signal
import sys
import threading
import time
import webbrowser
from collections import deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

try:
    import serial
    from serial.tools import list_ports
except ImportError:
    sys.exit("Falta pyserial: activar el entorno del proyecto (source .venv/bin/activate.fish) "
             "o python -m pip install pyserial")

BAUDIOS = 115200
PERIODO_ESTADO_S = 1.0
HTML = os.path.join(os.path.dirname(os.path.abspath(__file__)), "panel_esp32.html")
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA_REG = os.path.join(RAIZ, "registros", "placa")
RESUMEN_S = 10.0

# Programadores USB-serie habituales: WCH (CH340/CH343/CH9102), CP210x, FTDI, ESP32-S3 nativo.
VIDS_CONOCIDOS = {0x1A86, 0x10C4, 0x0403, 0x303A}

RE_MODO = re.compile(r"^modo=(\S+?)(?:\((\d+)\))? rele=(ON|off) \| ralenti=(\d+)s par>=(-?\d+)% rpmTSC1=(\d+)$")
RE_MOTOR = re.compile(r"^motor: (-?[\d.]+) rpm, par (-?\d+)%, refrig (-?\d+) C, DTC (\d+) \(SPN (\d+) FMI (\d+)\)$")
RE_CAN = re.compile(r"^can: (.+?), (solo escucha|TX), (\d+) tramas rx, (\d+) TSC1 \| oled: (si|no) \| libre (\d+) B$")
RE_ARRANQUE = re.compile(r"^V-ECU rpm .* reinicio: (\d+), TSC1 (\S+)")
COMANDO_VALIDO = re.compile(r"^[\x20-\x7e]{1,60}$")


def ahora_txt():
    t = time.time()
    return time.strftime("%H:%M:%S", time.localtime(t)) + f".{int(t * 1000) % 1000:03d}"


class Placa:
    """Conexión serie con la placa, lectura de líneas y estado interpretado."""

    def __init__(self, puerto_fijo=None):
        self.puerto_fijo = puerto_fijo  # None = automático
        self.ser = None
        self.puerto = None
        self.serie_usb = None  # número de serie del programador, para reencontrarlo
        self.error = None
        self.lock_tx = threading.Lock()
        self.lock_clientes = threading.Lock()
        self.clientes = []
        self.historial = deque(maxlen=3000)
        self.estado = {"modo": None, "ralentiNivel": None, "rele": None, "ralentiS": None, "parPct": None,
                       "rpmConsigna": None, "motor": None, "can": None, "tsc1Disponible": None,
                       "logFirmware": None, "ultimoEstado": None}
        self.ultimo_sondeo = 0.0
        self.bloque_estado = 0  # líneas de estado pendientes de un sondeo propio
        self.reg = None         # registro de la sesión (registros/placa/<fecha>_<hora>.log)
        self.ruta_reg = None
        self.ultimo_resumen = 0.0

    def abrir_registro(self):
        os.makedirs(CARPETA_REG, exist_ok=True)
        self.ruta_reg = os.path.join(CARPETA_REG, f"{dt.datetime.now():%Y-%m-%d_%H%M%S}.log")
        self.reg = open(self.ruta_reg, "w", encoding="utf-8", buffering=1)
        self.reg.write(f"# Registro del panel de la placa V-ECU · {dt.datetime.now().isoformat(timespec='seconds')}\n"
                       f"# Todo lo que dice la placa, los comandos enviados (>) y un [resumen] cada {RESUMEN_S:.0f} s.\n")

    def registrar(self, texto, tipo):
        if self.reg:
            pre = "> " if tipo == "enviado" else ""
            self.reg.write(f"{dt.datetime.now():%Y-%m-%d %H:%M:%S.%f}"[:-3] + f" [{tipo}] {pre}{texto}\n")

    def resumen(self):
        e = self.estado
        if not self.reg or not e.get("modo"):
            return
        m, c = e.get("motor"), e.get("can") or {}
        motor = (f"{m['rpm']:.0f} rpm, par {m['parPct']} %, refrig. {m['refrigeranteC']} °C, DTC {m['numDtc']}"
                 if m else "sin EEC1")
        nivel = f"({e['ralentiNivel']})" if e.get("ralentiNivel") else ""
        self.registrar(f"modo {e['modo']}{nivel} · relé {'ON' if e['rele'] else 'off'} · ralentí {e['ralentiS']} s · "
                       f"par mín. {e['parPct']} % · consigna {e['rpmConsigna']} · motor: {motor} · "
                       f"CAN {c.get('bus', '?')} {'solo escucha' if c.get('soloEscucha') else 'TX'} "
                       f"{c.get('tramasRx', 0)} rx · OLED {'sí' if c.get('oled') else 'no'}", "resumen")

    # ------------------------------------------------------------ difusión a navegadores
    def suscribir(self):
        q = queue.Queue(maxsize=2000)
        with self.lock_clientes:
            self.clientes.append(q)
        return q

    def desuscribir(self, q):
        with self.lock_clientes:
            if q in self.clientes:
                self.clientes.remove(q)

    def emitir(self, evento, datos):
        with self.lock_clientes:
            for q in list(self.clientes):
                try:
                    q.put_nowait((evento, datos))
                except queue.Full:
                    pass

    def linea(self, texto, tipo):
        item = {"t": ahora_txt(), "texto": texto, "tipo": tipo}
        if tipo != "sondeo":
            self.registrar(texto, tipo)
        self.historial.append(item)
        self.emitir("linea", item)

    def conexion(self):
        return {"conectado": self.ser is not None, "puerto": self.puerto, "error": self.error,
                "registro": os.path.relpath(self.ruta_reg, RAIZ) if self.ruta_reg else None,
                "fijo": self.puerto_fijo, "puertos": puertos_disponibles()}

    # ------------------------------------------------------------ puerto serie
    def elegir_puerto(self):
        if self.puerto_fijo:
            return self.puerto_fijo
        disponibles = list(list_ports.comports())
        if self.serie_usb:  # el mismo programador aunque haya cambiado de nombre
            for p in disponibles:
                if p.serial_number and p.serial_number == self.serie_usb:
                    return p.device
        for p in disponibles:
            if p.vid in VIDS_CONOCIDOS:
                return p.device
        for p in disponibles:
            if re.search(r"ttyACM|ttyUSB|cu\.usb|COM\d+", p.device):
                return p.device
        return None

    def abrir(self):
        dev = self.elegir_puerto()
        if not dev:
            self.fijar_error("No se encuentra el programador USB. ¿Está enchufado?")
            return False
        try:
            s = serial.Serial()
            s.port, s.baudrate, s.timeout = dev, BAUDIOS, 0.2
            s.dtr = False  # sin pulsos en EN/IO0 si el programador los tuviera cableados
            s.rts = False
            if os.name == "posix":
                s.exclusive = True
            s.open()
        except (serial.SerialException, OSError) as e:
            msg = str(e)
            if "lock" in msg.lower() or "busy" in msg.lower() or "ocupado" in msg.lower():
                msg = f"{dev} está ocupado: cerrar la consola de PlatformIO u otro programa que lo use."
            self.fijar_error(msg)
            return False
        self.ser, self.puerto, self.error = s, dev, None
        for p in list_ports.comports():
            if p.device == dev and p.serial_number:
                self.serie_usb = p.serial_number
        self.linea(f"Conectado a {dev} ({BAUDIOS} baudios)", "sistema")
        self.emitir("conexion", self.conexion())
        return True

    def fijar_error(self, msg):
        if msg != self.error:
            self.error = msg
            self.linea(msg, "error")
            self.emitir("conexion", self.conexion())

    def cerrar(self, motivo=None):
        if self.ser:
            try:
                self.ser.close()
            except Exception:
                pass
            self.ser = None
            self.linea(motivo or f"Desconectado de {self.puerto}", "sistema")
            self.emitir("conexion", self.conexion())

    def cambiar_puerto(self, puerto):
        self.puerto_fijo = puerto or None
        self.serie_usb = None
        self.error = None
        self.cerrar(f"Cambio de puerto: {puerto or 'automático'}")

    def enviar(self, cmd, sondeo=False):
        cmd = cmd.strip()
        if not COMANDO_VALIDO.match(cmd):
            return False, "Comando vacío o con caracteres no válidos (máx. 60, solo ASCII)."
        if not self.ser:
            return False, "No hay conexión con la placa."
        try:
            with self.lock_tx:
                self.ser.write((cmd + "\n").encode("ascii"))
        except (serial.SerialException, OSError) as e:
            self.cerrar(f"Error al escribir: {e}")
            return False, "Se perdió la conexión al enviar."
        if sondeo:
            self.bloque_estado = 3
        else:
            self.linea(cmd, "enviado")
        return True, None

    # ------------------------------------------------------------ interpretación
    def interpretar(self, texto):
        e = self.estado
        tipo = "placa"
        m = RE_MODO.match(texto)
        if m:
            e.update(modo=m[1], ralentiNivel=int(m[2]) if m[2] else None, rele=m[3] == "ON",
                     ralentiS=int(m[4]), parPct=int(m[5]), rpmConsigna=int(m[6]), ultimoEstado=ahora_txt())
            tipo = "estado"
        elif texto == "motor: sin EEC1":
            e["motor"] = None
            tipo = "estado"
        elif (m := RE_MOTOR.match(texto)):
            e["motor"] = {"rpm": float(m[1]), "parPct": int(m[2]), "refrigeranteC": int(m[3]),
                          "numDtc": int(m[4]), "spn": int(m[5]), "fmi": int(m[6])}
            tipo = "estado"
        elif (m := RE_CAN.match(texto)):
            e["can"] = {"bus": m[1], "soloEscucha": m[2] == "solo escucha", "tramasRx": int(m[3]),
                        "tsc1Enviados": int(m[4]), "oled": m[5] == "si", "libreB": int(m[6])}
            e["tsc1Disponible"] = m[2] == "TX"
            tipo = "estado"
        elif (m := RE_ARRANQUE.match(texto)):
            e["tsc1Disponible"] = m[2].upper().startswith("HABILITADO")
            e["logFirmware"] = False
            tipo = "arranque"
        elif texto in ("log on", "log off"):
            e["logFirmware"] = texto == "log on"
        elif texto.startswith("modo no disponible"):
            e["tsc1Disponible"] = False
            tipo = "error"
        elif texto == "modo desconocido":
            tipo = "error"
        elif texto.startswith("[control]") or texto.startswith("[rele]"):
            tipo = "control"
        # Las tres líneas que responde a un sondeo propio se marcan aparte (el panel las oculta).
        if tipo == "estado" and self.bloque_estado > 0:
            self.bloque_estado -= 1
            tipo = "sondeo"
        if tipo in ("estado", "sondeo", "arranque") or texto.startswith(("log ", "modo no")):
            self.emitir("estado", e)
        return tipo

    # ------------------------------------------------------------ bucle principal
    def bucle(self):
        resto = b""
        while True:
            if not self.ser:
                if not self.abrir():
                    time.sleep(1.0)
                    continue
                resto = b""
                self.ultimo_sondeo = 0
            try:
                datos = self.ser.read(256)
            except (serial.SerialException, OSError, TypeError):
                self.cerrar(f"Se perdió la conexión con {self.puerto} (¿programador desenchufado?). Reintentando…")
                time.sleep(0.5)
                continue
            if datos:
                resto += datos
                *lineas, resto = resto.split(b"\n")
                for bruta in lineas:
                    texto = bruta.decode("utf-8", errors="replace").rstrip("\r").replace("\x00", "")
                    if texto.strip():
                        self.linea(texto, self.interpretar(texto))
                if len(resto) > 512:  # basura sin salto de línea (p. ej. al quitar tensión)
                    self.linea(resto.decode("utf-8", errors="replace"), "placa")
                    resto = b""
            if self.ser and time.time() - self.ultimo_resumen >= RESUMEN_S and self.estado.get("ultimoEstado"):
                self.ultimo_resumen = time.time()
                self.resumen()
            if time.time() - self.ultimo_sondeo >= PERIODO_ESTADO_S:
                self.ultimo_sondeo = time.time()
                self.enviar("estado", sondeo=True)



# Imágenes de docs/ para el visor de diagramas (solo esa carpeta y docs/fotos, solo imágenes).
TIPOS_IMG = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".svg": "image/svg+xml"}


def leer_doc(ruta_url):
    m = re.match(r"^/docs/((?:fotos/|esquemas/)?[\w\-.]+)$", ruta_url.split("?")[0])
    if not m:
        return None, None
    ext = os.path.splitext(m[1])[1].lower()
    ruta = os.path.realpath(os.path.join(RAIZ, "docs", m[1]))
    if ext not in TIPOS_IMG or not ruta.startswith(os.path.realpath(os.path.join(RAIZ, "docs")) + os.sep) \
            or not os.path.isfile(ruta):
        return None, None
    with open(ruta, "rb") as f:
        return f.read(), TIPOS_IMG[ext]


def puertos_disponibles():
    # Solo puertos USB (en Linux, ttyS0…ttyS31 son puertos internos que no llevan a nada).
    return [{"device": p.device, "desc": p.description or "", "conocido": p.vid in VIDS_CONOCIDOS}
            for p in sorted(list_ports.comports(), key=lambda p: p.device)
            if p.vid is not None or re.search(r"ttyACM|ttyUSB|cu\.usb", p.device)]


def crear_manejador(placa):
    class Manejador(BaseHTTPRequestHandler):
        server_version = "PanelVECU/1.0"

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
            elif self.path == "/api/estado":
                self.responder(200, {"conexion": placa.conexion(), "estado": placa.estado})
            elif self.path == "/api/eventos":
                self.eventos()
            elif self.path.startswith("/docs/"):
                datos, tipo = leer_doc(self.path)
                if datos is None:
                    self.responder(404, {"error": "no existe"})
                else:
                    self.responder(200, datos, tipo)
            else:
                self.responder(404, {"error": "no existe"})

        def do_POST(self):
            # Solo peticiones de la propia página (evita que otra web mande comandos a la placa).
            origen = self.headers.get("Origin")
            if origen and not re.match(r"^http://(127\.0\.0\.1|localhost)(:\d+)?$", origen):
                return self.responder(403, {"error": "origen no permitido"})
            try:
                n = int(self.headers.get("Content-Length", 0))
                cuerpo = json.loads(self.rfile.read(min(n, 4096)) or b"{}")
            except (ValueError, json.JSONDecodeError):
                return self.responder(400, {"error": "JSON no válido"})
            if self.path == "/api/comando":
                ok, err = placa.enviar(str(cuerpo.get("cmd", "")))
                self.responder(200 if ok else 409, {"ok": ok, "error": err})
            elif self.path == "/api/puerto":
                placa.cambiar_puerto(cuerpo.get("puerto") or None)
                self.responder(200, {"ok": True})
            else:
                self.responder(404, {"error": "no existe"})

        def eventos(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Connection", "keep-alive")
            self.end_headers()
            q = placa.suscribir()
            try:
                inicial = [("conexion", placa.conexion()), ("estado", placa.estado)]
                inicial += [("linea", item) for item in list(placa.historial)[-800:]]
                for ev, datos in inicial:
                    self.wfile.write(f"event: {ev}\ndata: {json.dumps(datos)}\n\n".encode("utf-8"))
                self.wfile.flush()
                ultimo_puertos = time.time()
                while True:
                    try:
                        ev, datos = q.get(timeout=2.0)
                        self.wfile.write(f"event: {ev}\ndata: {json.dumps(datos)}\n\n".encode("utf-8"))
                    except queue.Empty:
                        self.wfile.write(b": latido\n\n")
                    if time.time() - ultimo_puertos > 3:  # lista de puertos al día
                        ultimo_puertos = time.time()
                        self.wfile.write(f"event: conexion\ndata: {json.dumps(placa.conexion())}\n\n".encode("utf-8"))
                    self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError, OSError):
                pass
            finally:
                placa.desuscribir(q)

    return Manejador


def main():
    ap = argparse.ArgumentParser(description="Panel en el navegador para la placa V-ECU (ESP32).")
    ap.add_argument("--puerto", help="puerto serie fijo (por defecto se busca el programador solo)")
    ap.add_argument("--http", type=int, default=8765, help="puerto del panel en 127.0.0.1 (8765)")
    ap.add_argument("--no-abrir", action="store_true", help="no abrir el navegador")
    ap.add_argument("--sin-registro", action="store_true", help="no guardar el registro en registros/placa/")
    args = ap.parse_args()

    placa = Placa(args.puerto)
    try:
        servidor = ThreadingHTTPServer(("127.0.0.1", args.http), crear_manejador(placa))
    except OSError:  # ya hay un panel en marcha en ese puerto: se abre ese
        url = f"http://127.0.0.1:{args.http}"
        print(f"El panel ya está en marcha: se abre {url}")
        if not args.no_abrir:
            webbrowser.open(url)
        return
    servidor.daemon_threads = True
    if not args.sin_registro:
        placa.abrir_registro()
        print(f"Registro de la sesión en {os.path.relpath(placa.ruta_reg, RAIZ)}")
    threading.Thread(target=placa.bucle, daemon=True).start()
    url = f"http://127.0.0.1:{args.http}"
    print(f"Panel V-ECU en {url}  (Ctrl+C para salir)")
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
        placa.cerrar("Panel cerrado")
        if placa.reg:
            placa.reg.close()


if __name__ == "__main__":
    main()
