"""Captura y análisis del bus J1939 de la EC210B (docs/CAPTURA_CAN.md).

Adaptador: DSD TECH SH-C30A (o cualquier candleLight / gs_usb) a 250 kbit/s,
SIEMPRE en modo solo escucha: el adaptador no transmite ni confirma tramas.

Uso:
    python tools/captura_can.py capturar --nombre 03_ralenti
    python tools/captura_can.py analizar capturas/2026-10-25_03_ralenti.log
    python tools/captura_can.py analizar capturas/*.log --informe capturas/resumen.md

Formato de los ficheros: el de candump -l, legible por SavvyCAN y python-can:
    (1729440000.123456) can0 0CF00400#F07D7D9C1E00FFFF
Las notas que se escriben durante la captura quedan como líneas "# (t) texto".

Dependencias: tools/requirements.txt (en Windows basta con
    python -m pip install --user gs_usb pyusb libusb-package)
"""
import argparse
import datetime as dt
import glob
import os
import statistics
import sys
import threading
import time
from collections import defaultdict

BITRATE = 250000

# ---------------------------------------------------------------- J1939

NOMBRES_PGN = {
    0: "TSC1 (petición de régimen/par)",
    59904: "Request",
    60160: "TP.DT (transporte, datos)",
    60416: "TP.CM (transporte, control)",
    60928: "Address Claimed",
    61441: "EBC1",
    61442: "ETC1",
    61443: "EEC2 (acelerador, % carga)",
    61444: "EEC1 (rpm, par)",
    65226: "DM1 (averías activas)",
    65227: "DM2 (averías anteriores)",
    65242: "SOFT (versión de software)",
    65247: "EEC3",
    65251: "EC1 (configuración del motor)",
    65253: "HOURS (horas de motor)",
    65259: "CI (identificación)",
    65262: "ET1 (temperaturas)",
    65263: "EFL/P1 (presiones y niveles)",
    65265: "CCVS",
    65266: "LFE (consumo)",
    65269: "AMB (ambiente)",
    65270: "IC1 (admisión/turbo)",
    65271: "VEP1 (tensión de batería)",
    65276: "DD (panel)",
}

DIRECCIONES = {0x00: "E-ECU", 0x03: "transmisión", 0x11: "V-ECU", 0x17: "panel I-ECU",
               0x27: "(0x27)", 0xF9: "herramienta", 0xFE: "nula", 0xFF: "global"}


def descomponer(can_id):
    """(prioridad, pgn, destino, origen) de un identificador de 29 bits."""
    prio = (can_id >> 26) & 0x7
    pf = (can_id >> 16) & 0xFF
    ps = (can_id >> 8) & 0xFF
    sa = can_id & 0xFF
    dp = (can_id >> 24) & 0x3
    if pf < 240:
        return prio, (dp << 16) | (pf << 8), ps, sa
    return prio, (dp << 16) | (pf << 8) | ps, 0xFF, sa


def nombre_dir(sa):
    return f"0x{sa:02X} {DIRECCIONES.get(sa, '')}".strip()


def dtcs(datos):
    """Lista de (SPN, FMI, OC) a partir de los bytes de un DM1 (desde el byte 2)."""
    out = []
    for i in range(2, len(datos) - 3, 4):
        b0, b1, b2, b3 = datos[i:i + 4]
        spn = b0 | (b1 << 8) | ((b2 >> 5) << 16)
        fmi = b2 & 0x1F
        if spn == 0 and fmi == 0:
            continue
        if spn == 0x7FFFF:
            continue
        out.append((spn, fmi, b3 & 0x7F))
    return out


# ---------------------------------------------------------------- captura

def abrir_adaptador():
    try:
        import libusb_package
        import usb.core
        from gs_usb.gs_usb import GsUsb
        from gs_usb.constants import GS_CAN_MODE_LISTEN_ONLY, GS_CAN_MODE_HW_TIMESTAMP
    except ImportError:
        sys.exit("Faltan librerías: python -m pip install --user gs_usb pyusb libusb-package")

    backend = libusb_package.get_libusb1_backend()
    devs = list(usb.core.find(find_all=True, backend=backend, custom_match=GsUsb.is_gs_usb_device))
    if not devs:
        sys.exit("No se encuentra ningún adaptador candleLight/gs_usb. ¿Está enchufado, con el "
                 "interruptor de arranque en OFF? En Linux, instalar los permisos con "
                 "tools/linux/instalar_permisos.sh; en Windows, el driver WinUSB con Zadig "
                 "(ver docs/CAPTURA_CAN.md).")
    dev = GsUsb(devs[0])
    print(f"Adaptador: {dev}")
    if not dev.set_bitrate(BITRATE):
        sys.exit("El adaptador no admite 250 kbit/s con su reloj.")
    pedidos = GS_CAN_MODE_LISTEN_ONLY | GS_CAN_MODE_HW_TIMESTAMP
    dev.start(pedidos)
    if not dev.device_flags & GS_CAN_MODE_LISTEN_ONLY:
        dev.stop()
        sys.exit("ABORTADO: el adaptador no admite el modo solo escucha. No se captura para no "
                 "transmitir en el bus de la máquina.")
    print("Modo SOLO ESCUCHA confirmado · 250 kbit/s")
    return dev


def capturar(args):
    from gs_usb.gs_usb_frame import GsUsbFrame

    os.makedirs(args.carpeta, exist_ok=True)
    marca = dt.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    ruta = os.path.join(args.carpeta, f"{marca}_{args.nombre}.log")
    dev = abrir_adaptador()

    notas = []

    def leer_notas():
        for linea in sys.stdin:
            notas.append((time.time(), linea.strip()))

    threading.Thread(target=leer_notas, daemon=True).start()

    print(f"Grabando en {ruta}")
    print("Escribe una nota y pulsa Enter para marcar un momento (p. ej. 'interruptor en ALTA').")
    print("Ctrl+C para terminar." + (f" Se parará sola a los {args.duracion} s." if args.duracion else ""))

    frame = GsUsbFrame()
    total = 0
    ids = set()
    rpm = temp = None
    t0 = time.time()
    t_hw0 = None
    ultimo_estado = 0
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(f"# captura {args.nombre} · {dt.datetime.now().isoformat(timespec='seconds')} · "
                f"{BITRATE} bit/s · solo escucha\n")
        try:
            while True:
                ahora = time.time()
                if args.duracion and ahora - t0 >= args.duracion:
                    break
                while notas:
                    tn, texto = notas.pop(0)
                    f.write(f"# ({tn:.6f}) {texto}\n")
                    print(f"  [nota] {texto}")
                if dev.read(frame, 100):
                    if frame.is_error_frame or frame.echo_id != 0xFFFFFFFF:
                        continue
                    # Marca de tiempo: reloj del PC al primer frame + reloj del adaptador
                    if t_hw0 is None:
                        t_hw0 = (ahora, frame.timestamp_us)
                    ts = t_hw0[0] + ((frame.timestamp_us - t_hw0[1]) & 0xFFFFFFFF) / 1e6
                    can_id = frame.arbitration_id
                    datos = bytes(frame.data[:frame.can_dlc])
                    sep = "#R" if frame.is_remote_frame else "#"
                    fmt_id = f"{can_id:08X}" if frame.is_extended_id else f"{can_id:03X}"
                    f.write(f"({ts:.6f}) can0 {fmt_id}{sep}{datos.hex().upper()}\n")
                    total += 1
                    ids.add(can_id)
                    if frame.is_extended_id:
                        _, pgn, _, sa = descomponer(can_id)
                        if pgn == 61444 and sa == 0 and len(datos) >= 5:
                            crudo = datos[3] | (datos[4] << 8)
                            rpm = crudo * 0.125 if crudo < 0xFB00 else None
                        elif pgn == 65262 and sa == 0 and datos:
                            temp = datos[0] - 40 if datos[0] < 0xFB else None
                if ahora - ultimo_estado >= 1:
                    ultimo_estado = ahora
                    r = f"{rpm:.0f} rpm" if rpm is not None else "-- rpm"
                    tt = f"{temp} °C" if temp is not None else "-- °C"
                    print(f"\r  {ahora - t0:6.0f} s · {total:7d} tramas · {len(ids):3d} IDs · {r} · {tt}   ",
                          end="", flush=True)
        except KeyboardInterrupt:
            pass
        finally:
            dev.stop()
    print(f"\nGuardado: {ruta} ({total} tramas, {len(ids)} identificadores)")
    if total == 0:
        print("No llegó ninguna trama: revisar CAN H/L (¿invertidos?), masa, llave en contacto y 250 kbit/s.")


# ---------------------------------------------------------------- análisis

def leer_log(ruta):
    tramas, notas = [], []
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            if linea.startswith("#"):
                if linea.startswith("# (") and ")" in linea:
                    t, _, texto = linea[3:].partition(")")
                    notas.append((float(t), texto.strip()))
                continue
            try:
                ts, _canal, trama = linea.split()
                ident, _, datos = trama.partition("#")
                remota = datos.startswith("R")
                datos = b"" if remota else bytes.fromhex(datos)
                tramas.append((float(ts.strip("()")), int(ident, 16), len(ident) > 3, datos))
            except ValueError:
                continue
    return tramas, notas


def analizar_fichero(ruta):
    tramas, notas = leer_log(ruta)
    out = [f"## {os.path.basename(ruta)}", ""]
    if not tramas:
        out.append("Sin tramas.")
        return out
    t0, t1 = tramas[0][0], tramas[-1][0]
    dur = max(t1 - t0, 1e-9)
    out.append(f"- Duración: **{dur:.1f} s** · tramas: **{len(tramas)}** "
               f"(≈ {len(tramas) / dur:.0f} tramas/s, carga del bus ≈ {len(tramas) / dur * 130 / BITRATE * 100:.0f} %)")

    por_id = defaultdict(list)
    for ts, ident, ext, datos in tramas:
        por_id[(ident, ext)].append((ts, datos))

    origenes = sorted({ident & 0xFF for (ident, ext) in por_id if ext})
    out.append("- Direcciones de origen vistas: " + ", ".join(nombre_dir(sa) for sa in origenes))
    if 0x11 in origenes:
        out.append("- ⚠️ Hay tramas con origen **0x11 (V-ECU)**: ¿está la V-ECU conectada?")
    out.append("")

    # Tabla de identificadores
    out += ["| ID | PGN | Mensaje | Origen → destino | Nº | Periodo medio | Bytes que cambian | Último dato |",
            "|---|---|---|---|---|---|---|---|"]
    for (ident, ext), lista in sorted(por_id.items(), key=lambda kv: kv[0][0]):
        tiempos = [t for t, _ in lista]
        periodos = [b - a for a, b in zip(tiempos, tiempos[1:])]
        per = f"{statistics.mean(periodos) * 1000:.0f} ms" if periodos else "—"
        largo = max(len(d) for _, d in lista)
        cambian = [str(i + 1) for i in range(largo)
                   if len({d[i] if i < len(d) else None for _, d in lista}) > 1]
        ultimo = lista[-1][1].hex(" ").upper()
        if ext:
            _, pgn, da, sa = descomponer(ident)
            dest = "global" if da == 0xFF else nombre_dir(da)
            out.append(f"| `{ident:08X}` | {pgn} (0x{pgn:04X}) | {NOMBRES_PGN.get(pgn, '')} | "
                       f"{nombre_dir(sa)} → {dest} | {len(lista)} | {per} | {','.join(cambian) or '—'} | `{ultimo}` |")
        else:
            out.append(f"| `{ident:03X}` (11 bits) | — | — | — | {len(lista)} | {per} | "
                       f"{','.join(cambian) or '—'} | `{ultimo}` |")
    out.append("")

    # EEC1: rpm y par
    eec1 = [(t, d) for (ident, ext), l in por_id.items() if ext
            and descomponer(ident)[1] == 61444 and ident & 0xFF == 0 for t, d in l]
    if eec1:
        rpms = [(d[3] | d[4] << 8) * 0.125 for _, d in eec1 if len(d) >= 5 and (d[3] | d[4] << 8) < 0xFB00]
        pares = [d[2] - 125 for _, d in eec1 if len(d) >= 3 and d[2] < 0xFB]
        if rpms:
            out.append(f"- **EEC1 rpm**: mín {min(rpms):.0f} · media {statistics.mean(rpms):.0f} · máx {max(rpms):.0f}")
        if pares:
            out.append(f"- **EEC1 par real**: mín {min(pares)} % · media {statistics.mean(pares):.0f} % · máx {max(pares)} %")
    else:
        out.append("- ⚠️ No hay EEC1 (0x0CF00400) de la E-ECU: ¿motor parado o bus equivocado?")

    et1 = [d for (ident, ext), l in por_id.items() if ext
           and descomponer(ident)[1] == 65262 and ident & 0xFF == 0 for _, d in l]
    temps = [d[0] - 40 for d in et1 if d and d[0] < 0xFB]
    if temps:
        out.append(f"- **ET1 refrigerante**: {min(temps)}–{max(temps)} °C")

    # DM1 (una trama) y DM1 por transporte BAM
    averias = defaultdict(set)
    bam = {}
    for ts, ident, ext, datos in tramas:
        if not ext:
            continue
        _, pgn, _, sa = descomponer(ident)
        if pgn == 65226 and len(datos) >= 6:
            for d in dtcs(datos):
                averias[sa].add(d)
        elif pgn == 60416 and len(datos) == 8 and datos[0] == 0x20:
            pgn_bam = datos[5] | datos[6] << 8 | datos[7] << 16
            if pgn_bam == 65226:
                bam[sa] = {"tam": datos[1] | datos[2] << 8, "paq": datos[3], "datos": {}}
        elif pgn == 60160 and sa in bam and datos:
            b = bam[sa]
            b["datos"][datos[0]] = datos[1:8]
            if len(b["datos"]) == b["paq"]:
                completo = b"".join(b["datos"][i] for i in sorted(b["datos"]))[:b["tam"]]
                for d in dtcs(completo):
                    averias[sa].add(d)
                del bam[sa]
    if averias:
        for sa, lista in averias.items():
            txt = "; ".join(f"SPN {s} FMI {f} (×{oc})" for s, f, oc in sorted(lista))
            out.append(f"- **DM1 de {nombre_dir(sa)}**: {txt}")
    else:
        out.append("- DM1: sin averías activas (o sin DM1 en la captura)")

    tsc1 = [k for k in por_id if k[1] and descomponer(k[0])[1] == 0]
    out.append("- TSC1 en el bus: " + (", ".join(f"`{k[0]:08X}`" for k in tsc1) if tsc1 else "ninguno"))

    if notas:
        out += ["", "Notas de la captura:", ""]
        out += [f"- t = {t - t0:6.1f} s · {texto}" for t, texto in notas]
    out.append("")
    return out


def analizar(args):
    rutas = []
    for patron in args.ficheros:
        rutas += sorted(glob.glob(patron)) or [patron]
    texto = [f"# Análisis del bus J1939 · {dt.date.today().isoformat()}", ""]
    for ruta in rutas:
        texto += analizar_fichero(ruta)
    salida = "\n".join(texto)
    print(salida)
    if args.informe:
        with open(args.informe, "w", encoding="utf-8") as f:
            f.write(salida + "\n")
        print(f"\nInforme guardado en {args.informe}")


def main():
    for flujo in (sys.stdout, sys.stderr):
        try:
            flujo.reconfigure(encoding="utf-8", errors="replace")
        except AttributeError:
            pass
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="orden", required=True)
    c = sub.add_parser("capturar", help="grabar el bus en modo solo escucha")
    c.add_argument("--nombre", required=True, help="nombre de la prueba, p. ej. 03_ralenti")
    c.add_argument("--duracion", type=float, default=0, help="segundos (0 = hasta Ctrl+C)")
    c.add_argument("--carpeta", default="capturas")
    c.set_defaults(func=capturar)
    an = sub.add_parser("analizar", help="resumen de uno o varios ficheros .log")
    an.add_argument("ficheros", nargs="+")
    an.add_argument("--informe", help="guardar el resumen en un .md")
    an.set_defaults(func=analizar)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
