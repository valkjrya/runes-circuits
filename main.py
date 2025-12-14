import os
import random
import datetime as dt
from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

PROJECT = "RUNES & CIRCUITS"

# ----------------------------
# DATI BASE
# ----------------------------
COLORI = {
    "TERRA": "Giallo / Ocra",
    "ACQUA": "Bianco / Dorato",
    "ARIA": "Verde / Verde",
    "FUOCO": "Rosso / Rosso",
    "SPAZIO": "Blu / Blu",
}

SEGNI_PER_ELEMENTO = {
    "TERRA": ["Toro", "Vergine", "Capricorno"],
    "ACQUA": ["Cancro", "Scorpione", "Pesci"],
    "ARIA": ["Gemelli", "Bilancia", "Acquario"],
    "FUOCO": ["Ariete", "Leone", "Sagittario"],
    "SPAZIO": ["Ophiuchus", "Trans-zodiacale", "Anima cosmica"],
}

RUNE_PER_ELEMENTO = {
    "TERRA": ["Uruz", "Wunjo", "Berkana", "Jera", "Othila", "Isa", "Eihwaz"],
    "ACQUA": ["Perth", "Laguz", "Ingwaz", "Raido", "Gebo", "Hagalaz"],
    "ARIA": ["Ansuz", "Tiwaz", "Kenaz", "Eihwaz"],
    "FUOCO": ["Dagaz", "Fehu", "Thurisaz", "Nauthiz", "Othila"],
    "SPAZIO": [
        "Dagaz – soglia cosmica",
        "Perth – mistero dell’oracolo",
        "Ansuz – trasmissione",
        "Eihwaz – asse dei mondi",
        "Isa – vuoto fertile",
        "Kenaz – scintilla/codice",
        "Gebo – connessione/rete",
        "Ingwaz – potenziale non manifesto",
    ],
}

MESSAGGI_TEMPO = [
    "Il tempo si apre quando ascolti.",
    "Oggi il circuito chiede presenza.",
    "Non forzare: la runa arriva.",
    "Il segno è già in movimento.",
    "Il silenzio è parte del codice.",
]

# ----------------------------
# CORS / JSON helper
# ----------------------------
def _cors_json(payload, status=200):
    res = make_response(jsonify(payload), status)
    res.headers["Content-Type"] = "application/json; charset=utf-8"
    res.headers["Access-Control-Allow-Origin"] = "*"
    res.headers["Access-Control-Allow-Methods"] = "GET,OPTIONS"
    res.headers["Access-Control-Allow-Headers"] = "Content-Type"
    res.headers["Cache-Control"] = "no-store"
    return res

# ----------------------------
# ROUTES
# ----------------------------
@app.route("/health", methods=["GET"])
def health():
    return _cors_json({"ok": True, "service": PROJECT})

@app.route("/", methods=["GET", "OPTIONS"])
def home():
    if request.method == "OPTIONS":
        return _cors_json({"ok": True})
    return _cors_json({
        "progetto": PROJECT,
        "stato": "attivo",
        "messaggio": "OK. Prova /oracle per ricevere una runa.",
        "uso": {
            "random": "/oracle",
            "per_elemento": "/oracle?elemento=TERRA|ACQUA|ARIA|FUOCO|SPAZIO",
            "modalita": "/oracle?mode=day oppure /oracle?mode=minute (default)",
        },
    })

@app.route("/oracle", methods=["GET", "OPTIONS"])
def oracle():
    if request.method == "OPTIONS":
        return _cors_json({"ok": True})

    now = dt.datetime.utcnow()

    # mode=minute cambia ogni minuto; mode=day cambia una volta al giorno
    mode = (request.args.get("mode") or "minute").strip().lower()

    if mode == "day":
        seed = f"{now.date().isoformat()}"
    else:
        seed = f"{now.date().isoformat()}-{now.hour:02d}{now.minute:02d}"

    rnd = random.Random(seed)

    elemento = (request.args.get("elemento") or "").strip().upper()
    if elemento not in RUNE_PER_ELEMENTO:
        elemento = rnd.choice(list(RUNE_PER_ELEMENTO.keys()))

    runa = rnd.choice(RUNE_PER_ELEMENTO[elemento])
    messaggio = rnd.choice(MESSAGGI_TEMPO)

    return _cors_json({
        "progetto": PROJECT,
        "ts_utc": now.isoformat(timespec="seconds") + "Z",
        "seed": seed,
        "elemento": elemento,
        "colore": COLORI[elemento],
        "segni": SEGNI_PER_ELEMENTO[elemento],
        "runa": runa,
        "messaggio": messaggio,
        "cta": "Ricarica per un nuovo segno (mode=minute) oppure usa mode=day per coerenza giornaliera."
    })

# ----------------------------
# LOCAL RUN (non usato su Cloud Run, ma utile in locale)
# ----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
