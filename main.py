import os
import random
import datetime as dt
from html import escape
from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

PROJECT = "RUNES & CIRCUITS"

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
    "SPAZIO": ["Sagittario", "Acquario", "Pesci"],  # puoi cambiare
}

RUNE_PER_ELEMENTO = {
    "TERRA": ["Fehu", "Uruz", "Berkano", "Ingwaz", "Jera"],
    "ACQUA": ["Laguz", "Perthro", "Eihwaz", "Ingwaz", "Ansuz"],
    "ARIA": ["Ansuz", "Raido", "Kenaz", "Gebo", "Wunjo"],
    "FUOCO": ["Kenaz", "Sowilo", "Tiwaz", "Hagalaz", "Othila"],
    "SPAZIO": ["Algiz", "Eihwaz", "Dagaz", "Isa", "Nauthiz"],
}

MESSAGGI = {
    "TERRA": [
        "Radicati. La forma si stabilizza quando smetti di inseguire.",
        "Il passo lento è quello che arriva. Cura la base.",
        "Metti ordine: ciò che è semplice diventa forte.",
    ],
    "ACQUA": [
        "Ascolta: il segno è già in movimento.",
        "Lascia scorrere. Una risposta arriva senza sforzo.",
        "Sii morbida con te: la marea cambia presto.",
    ],
    "ARIA": [
        "Una nuova idea chiede spazio. Seguila.",
        "Parla chiaro: il vento porta alleati.",
        "Alleggerisci il pensiero: vedrai l’uscita.",
    ],
    "FUOCO": [
        "Accendi il coraggio: una scelta ti libera.",
        "La scintilla guida. Muoviti adesso, non perfetto: vivo.",
        "Trasforma la paura in gesto: la strada si apre.",
    ],
    "SPAZIO": [
        "Sospendi il giudizio: il vuoto è una porta.",
        "Tra due mondi c’è un varco. Restaci un istante.",
        "Il silenzio è codice: ascolta prima di agire.",
    ],
}

def _seed_key(mode: str) -> str:
    now = dt.datetime.utcnow()
    if mode == "minute":
        return now.strftime("%Y-%m-%d-%H%M")
    return now.strftime("%Y-%m-%d")

def _pick_elemento(elem: str) -> str:
    e = (elem or "").strip().upper()
    if e in COLORI:
        return e
    return random.choice(list(COLORI.keys()))

def _oracle_payload(elemento: str, mode: str):
    seed = _seed_key(mode)
    rng = random.Random(f"{elemento}:{seed}")

    runa = rng.choice(RUNE_PER_ELEMENTO[elemento])
    msg = rng.choice(MESSAGGI[elemento])
    segni = SEGNI_PER_ELEMENTO[elemento]
    colore = COLORI[elemento]

    return {
        "progetto": PROJECT,
        "elemento": elemento,
        "colore": colore,
        "runa": runa,
        "messaggio": msg,
        "segni": segni,
        "seed": seed,
        "cta": "Ricarica per un nuovo segno (mode=minute) oppure usa mode=day per coerenza giornaliera.",
        "ts_utc": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }

@app.get("/")
def home():
    # Pagina bella di default
    elemento = request.args.get("elemento", "RANDOM")
    mode = request.args.get("mode", "minute")
    return view(elemento=elemento, mode=mode)

@app.get("/oracle")
def oracle():
    elemento_in = request.args.get("elemento", "RANDOM")
    mode = request.args.get("mode", "minute")
    elemento = _pick_elemento(elemento_in)
    data = _oracle_payload(elemento, mode)

    resp = jsonify(data)
    resp.headers["Cache-Control"] = "no-store"
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp

@app.get("/view")
def view(elemento=None, mode=None):
    elemento_in = elemento or request.args.get("elemento", "RANDOM")
    mode = mode or request.args.get("mode", "minute")
    elemento = _pick_elemento(elemento_in)
    data = _oracle_payload(elemento, mode)

    # HTML NIBI-style (tutto inline, nessun asset esterno)
    html = f"""<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Runes & Circuits — Oracolo</title>
</head>
<body style="margin:0; min-height:100vh; color:#eef2ff; font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
  background: radial-gradient(circle at 20% 0%, rgba(110,80,255,.30) 0%, rgba(10,12,26,1) 40%, rgba(2,3,8,1) 100%);
  overflow-x:hidden;">

  <div style="max-width:980px; margin:0 auto; padding:36px 16px 44px;">
    <div style="text-align:center; letter-spacing:.26em; font-size:11px; opacity:.75;">RUNES &amp; CIRCUITS</div>

    <div style="margin-top:14px; text-align:center;">
      <div style="font-size:34px; font-weight:900; line-height:1.1;
        text-shadow:0 0 18px rgba(120,90,255,.25), 0 0 12px rgba(255,215,140,.18);">
        ✨ Oracolo — Rune Parlanti
      </div>
      <div style="margin-top:10px; opacity:.85; font-size:14px;">
        Messaggio del momento • modalità: <b>{escape(mode)}</b>
      </div>
    </div>

    <div style="display:flex; justify-content:center; margin:18px 0 10px; gap:10px; flex-wrap:wrap;">
      {button("TERRA","🌿 Terra")}
      {button("ACQUA","🌊 Acqua")}
      {button("ARIA","💨 Aria")}
      {button("FUOCO","🔥 Fuoco")}
      {button("SPAZIO","🟦 Spazio")}
      {button("RANDOM","✨ Random")}
    </div>

    <div style="margin:18px auto 0; max-width:860px;
      background: rgba(0,0,0,.26);
      border-radius:26px;
      border:1px solid rgba(180,140,255,.35);
      box-shadow: 0 18px 60px rgba(0,0,0,.55), 0 0 0 1px rgba(255,215,140,.10) inset, 0 0 42px rgba(120,90,255,.10);
      overflow:hidden;">

      <div style="padding:18px 18px 12px; border-bottom:1px solid rgba(255,255,255,.08);">
        <div style="display:flex; align-items:center; justify-content:space-between; gap:12px; flex-wrap:wrap;">
          <div style="font-size:20px; font-weight:900;">
            Elemento: <span style="color:#ffd78a; text-shadow:0 0 12px rgba(255,215,140,.18);">{escape(data["elemento"])}</span>
          </div>
          <a href="/oracle?elemento={escape(data["elemento"])}&mode={escape(mode)}" target="_blank"
             style="text-decoration:none; color:#eef2ff; opacity:.85; font-size:12px; padding:10px 12px; border-radius:999px;
             border:1px solid rgba(255,255,255,.14); background:rgba(255,255,255,.06);">
             Apri JSON
          </a>
        </div>
        <div style="margin-top:8px; font-size:13px; opacity:.8;">
          Colore: <b>{escape(data["colore"])}</b>
          <span style="opacity:.5;"> • </span>
          Segni: <b>{escape(", ".join(data["segni"]))}</b>
        </div>
      </div>

      <div style="padding:18px;">
        <div style="display:flex; gap:16px; flex-wrap:wrap;">
          <div style="flex:1; min-width:220px;">
            <div style="opacity:.75; font-size:12px; letter-spacing:.12em;">RUNA</div>
            <div style="margin-top:8px; font-size:28px; font-weight:950;
              text-shadow:0 0 18px rgba(120,90,255,.25), 0 0 12px rgba(255,215,140,.18);">
              {escape(data["runa"])}
            </div>
            <div style="margin-top:10px; opacity:.65; font-size:12px;">seed: {escape(data["seed"])} • {escape(data["ts_utc"])}</div>
          </div>

          <div style="flex:2; min-width:260px;">
            <div style="opacity:.75; font-size:12px; letter-spacing:.12em;">MESSAGGIO</div>
            <div style="margin-top:10px; font-size:16px; line-height:1.55; opacity:.98;">
              {escape(data["messaggio"])}
            </div>

            <div style="margin-top:16px;">
              <a href="/view?elemento={escape(data["elemento"])}&mode=minute"
                 style="{gold_button_style()}">Ricarica (minute)</a>
              <a href="/view?elemento={escape(data["elemento"])}&mode=day"
                 style="{ghost_button_style()}">Coerenza (day)</a>
            </div>

            <div style="margin-top:10px; opacity:.65; font-size:12px;">
              {escape(data["cta"])}
            </div>
          </div>
        </div>
      </div>

    </div>

    <div style="text-align:center; margin-top:18px; font-size:12px; opacity:.65;">
      Oracolo R&amp;C — arcano + futuro • Tina Örn vibes ✨
    </div>
  </div>
</body>
</html>"""

    resp = make_response(html)
    resp.headers["Content-Type"] = "text/html; charset=utf-8"
    resp.headers["Cache-Control"] = "no-store"
    return resp

def gold_button_style():
    return ("display:inline-block; margin-right:10px; text-decoration:none; padding:12px 16px; border-radius:999px;"
            "font-weight:900; letter-spacing:.06em; font-size:13px; color:#2a1a00;"
            "background:linear-gradient(135deg,#ffd36b,#ffb347);"
            "box-shadow:0 0 0 2px rgba(255,215,140,.55) inset, 0 0 25px rgba(255,190,80,.38), 0 0 60px rgba(255,215,140,.22);")

def ghost_button_style():
    return ("display:inline-block; text-decoration:none; padding:12px 16px; border-radius:999px;"
            "font-weight:800; letter-spacing:.06em; font-size:13px; color:#eef2ff; opacity:.92;"
            "border:1px solid rgba(255,255,255,.14); background:rgba(255,255,255,.06);"
            "box-shadow:0 0 0 1px rgba(255,215,140,.10) inset;")

def button(key, label):
    href = f"/view?elemento={key}&mode=minute"
    return (f'<a href="{href}" style="text-decoration:none; display:inline-block; padding:10px 14px; border-radius:999px;'
            f'border:1px solid rgba(180,140,255,.30); background:rgba(255,255,255,.06); color:#eef2ff;'
            f'font-weight:800; font-size:13px; letter-spacing:.06em;'
            f'box-shadow:0 0 0 1px rgba(255,215,140,.10) inset, 0 0 18px rgba(120,90,255,.08);">{label}</a>')
