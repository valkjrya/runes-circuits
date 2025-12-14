import os
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- LOGICA FISSA: segno → elemento → colore → rune (non invertire) ---

COLORI = {
    "TERRA":  "Giallo / Ocra",
    "ACQUA":  "Bianco / Bianco",
    "ARIA":   "Verde / Verde",
    "FUOCO":  "Rosso / Rosso",
    "SPAZIO": "Blu / Blu",
}

SEGNI_PER_ELEMENTO = {
    "TERRA":  ["Toro", "Vergine", "Capricorno"],
    "ACQUA":  ["Cancro", "Scorpione", "Pesci"],
    "ARIA":   ["Gemelli", "Bilancia", "Acquario"],
    "FUOCO":  ["Ariete", "Leone", "Sagittario"],
    # SPAZIO è trans-zodiacale
}

RUNE_PER_ELEMENTO = {
    "TERRA":  ["Uruz", "Wunjo", "Berkana", "Othila", "Isa", "Eihwaz", "Jera"],
    "ACQUA":  ["Perth", "Laguz", "Ingwaz", "Raido", "Gebo", "Hagalaz"],
    "ARIA":   ["Ansuz", "Tiwaz", "Berkana", "Eihwaz"],
    "FUOCO":  ["Dagaz", "Othila", "Fehu", "Thurisaz", "Nauthiz", "Eihwaz"],
    "SPAZIO": ["Dagaz", "Perth", "Ansuz", "Eihwaz", "Isa", "Kenaz", "Gebo", "Ingwaz"],
}

NOTE_LUNARI = {
    "TERRA":  "🌑 Luna Nuova: Isa · Eihwaz · Jera",
    "ACQUA":  "🌘 Calare della Luna: Kenaz · Raido · Gebo",
    "ARIA":   "🌒 Luna Crescente",
    "FUOCO":  "",
    "SPAZIO": "✧ Trans-zodiacale / coscienza / anima cosmica",
}

PONTI_SPAZIO = {
    "Dagaz":  "soglia, alba cosmica",
    "Perth":  "mistero, oracolo",
    "Ansuz":  "voce divina, trasmissione",
    "Eihwaz": "asse dei mondi",
    "Isa":    "vuoto, silenzio primordiale",
    "Kenaz":  "scintilla, codice",
    "Gebo":   "connessione, rete",
    "Ingwaz": "potenziale non manifesto",
}

# Messaggistica breve (puoi cambiarla quando vuoi)
MESSAGGI_BASE = {
    "TERRA":  "Radicati. Fai una cosa concreta e semplice, senza forzare.",
    "ACQUA":  "Ascolta il flusso. Lascia andare ciò che pesa, scegli morbidezza.",
    "ARIA":   "Chiarezza e parola. Nomina ciò che senti: diventa reale.",
    "FUOCO":  "Trasforma. Un gesto deciso oggi apre un varco domani.",
    "SPAZIO": "Portale. Osserva dall’alto: la risposta è già in te.",
}

def corsify(resp):
    # CORS per WordPress / NFC
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    resp.headers["Cache-Control"] = "no-store"
    return resp

@app.route("/health", methods=["GET"])
def health():
    return corsify(jsonify({"ok": True, "service": "runes-circuits"}))

@app.route("/rune", methods=["GET", "OPTIONS"])
def rune():
    if request.method == "OPTIONS":
        return corsify(jsonify({"ok": True}))

    segno = (request.args.get("segno") or "").strip()
    elemento = (request.args.get("elemento") or "").strip().upper()

    # Determina elemento: prima da segno, poi fallback su parametro elemento
    elemento_dedotto = None
    segno_norm = segno.capitalize() if segno else ""

    if segno_norm:
        for el, segni in SEGNI_PER_ELEMENTO.items():
            if segno_norm in segni:
                elemento_dedotto = el
                break
        # SPAZIO se segno è Ophiuchus (accettiamo anche varianti)
        if not elemento_dedotto and segno_norm.lower() in ["ophiuchus", "ofiuco", "serpentario"]:
            elemento_dedotto = "SPAZIO"

    if not elemento_dedotto:
        # se non c'è segno valido, uso elemento passato
        if elemento in RUNE_PER_ELEMENTO:
            elemento_dedotto = elemento
        else:
            # default sicuro: SPAZIO (portale)
            elemento_dedotto = "SPAZIO"

    rune_lista = RUNE_PER_ELEMENTO[elemento_dedotto]
    runa = random.choice(rune_lista)

    colore = COLORI[elemento_dedotto]
    segni_txt = " · ".join(SEGNI_PER_ELEMENTO.get(elemento_dedotto, []))
    if elemento_dedotto == "SPAZIO":
        segni_txt = "✧ Ophiuchus · trans-zodiacale · anima cosmica"

    # testo: base + (se SPAZIO) descrizione ponte
    testo = MESSAGGI_BASE[elemento_dedotto]
    extra = ""
    if elemento_dedotto == "SPAZIO":
        extra = f"{runa} → {PONTI_SPAZIO.get(runa, '')}".strip()

    payload = {
        "segno": segno_norm if segno_norm else None,
        "elemento": elemento_dedotto,
        "colore": colore,
        "segni": segni_txt,
        "runa": runa,
        "testo": testo,
        "nota_lunare": NOTE_LUNARI.get(elemento_dedotto, ""),
        "ponte_spazio": extra if extra else None,
        # link opzionali (li useremo nei pulsanti WordPress)
        "nft_url": os.getenv("NFT_URL", ""),
        "github_url": os.getenv("GITHUB_URL", ""),
    }

    return corsify(jsonify(payload))

if __name__ == "__main__":
    # Cloud Run ascolta su $PORT
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
