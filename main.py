import random
import datetime as dt
from html import escape
from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

# =========================
# BRAND
# =========================
TITLE = "RUNES & CIRCUITS"
SUBTITLE = "Rune Parlanti"
CTA_TEXT = "RICEVI LA DIVINAZIONE"

ELEMENTI = ["TERRA", "ACQUA", "ARIA", "FUOCO", "SPAZIO"]

COLORI = {
    "TERRA": "Giallo / Ocra",
    "ACQUA": "Bianco / Dorato",
    "ARIA": "Verde / Verde",
    "FUOCO": "Rosso / Rosso",
    "SPAZIO": "Blu / Blu",
}

SEGNI = {
    "TERRA": ["Toro", "Vergine", "Capricorno"],
    "ACQUA": ["Cancro", "Scorpione", "Pesci"],
    "ARIA": ["Gemelli", "Bilancia", "Acquario"],
    "FUOCO": ["Ariete", "Leone", "Sagittario"],
    "SPAZIO": ["Acquario", "Pesci", "Sagittario"],
}

RUNE = {
    "TERRA": ["Fehu", "Uruz", "Berkano", "Jera"],
    "ACQUA": ["Laguz", "Perthro", "Eihwaz", "Isa"],
    "ARIA": ["Ansuz", "Raido", "Gebo", "Wunjo"],
    "FUOCO": ["Kenaz", "Sowilo", "Tiwaz", "Hagalaz"],
    "SPAZIO": ["Algiz", "Dagaz", "Nauthiz", "Othila"],
}

RUNE_SYMBOL = {
    "Fehu":"ᚠ","Uruz":"ᚢ","Ansuz":"ᚨ","Raido":"ᚱ","Kenaz":"ᚲ","Gebo":"ᚷ",
    "Wunjo":"ᚹ","Hagalaz":"ᚺ","Nauthiz":"ᚾ","Isa":"ᛁ","Jera":"ᛃ",
    "Eihwaz":"ᛇ","Perthro":"ᛈ","Algiz":"ᛉ","Sowilo":"ᛋ","Tiwaz":"ᛏ",
    "Berkano":"ᛒ","Laguz":"ᛚ","Dagaz":"ᛞ","Othila":"ᛟ"
}

MESSAGGI = {
    "TERRA": [
        ("Metti ordine: ciò che è semplice diventa forte.",
         "Create order: what is simple becomes strong.")
    ],
    "ACQUA": [
        ("Lascia scorrere. Una risposta arriva senza sforzo.",
         "Let it flow. An answer arrives without force.")
    ],
    "ARIA": [
        ("Una nuova idea chiede spazio. Seguila.",
         "A new idea asks for space. Follow it.")
    ],
    "FUOCO": [
        ("Accendi il coraggio: una scelta ti libera.",
         "Ignite courage: one choice sets you free.")
    ],
    "SPAZIO": [
        ("Sospendi il giudizio: il vuoto è una porta.",
         "Suspend judgment: the void is a door.")
    ],
}

# =========================
# ORACOLO
# =========================
def genera_oracolo(elemento):
    elemento = elemento if elemento in ELEMENTI else random.choice(ELEMENTI)

    # 🔑 chiave SEMPRE diversa (millisecondi)
    seed = f"{dt.datetime.utcnow().isoformat()}:{random.random()}"
    rng = random.Random(seed)

    runa = rng.choice(RUNE[elemento])
    simbolo = RUNE_SYMBOL.get(runa, "ᚱ")
    msg_it, msg_en = rng.choice(MESSAGGI[elemento])

    return {
        "elemento": elemento,
        "colore": COLORI[elemento],
        "segni": SEGNI[elemento],
        "runa": runa,
        "runa_symbol": simbolo,
        "messaggio_it": msg_it,
        "messaggio_en": msg_en,
        "seed": seed,
        "ts": dt.datetime.utcnow().isoformat(timespec="seconds")+"Z"
    }

# =========================
# API JSON
# =========================
@app.get("/oracle")
def oracle():
    elemento = request.args.get("elemento", "RANDOM").upper()
    data = genera_oracolo(elemento)
    return jsonify(data)

# =========================
# UI
# =========================
@app.get("/")
@app.get("/view")
def view():
    elemento = request.args.get("elemento", "RANDOM").upper()
    data = genera_oracolo(elemento)

    def e(x): return escape(str(x))

    html = f"""
<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{TITLE} — {SUBTITLE}</title>
</head>

<body style="margin:0;background:#020308;color:#f6f3ff;
font-family:system-ui,Segoe UI,Arial;">

<div style="max-width:900px;margin:40px auto;padding:24px;">

<h1 style="text-align:center;">✨ {SUBTITLE}</h1>

<h2>Elemento: {e(data["elemento"])}</h2>

<div style="display:flex;align-items:center;gap:12px;">
  <div id="runa-symbol" style="font-size:40px;">{e(data["runa_symbol"])}</div>
  <div id="runa-name" style="font-size:34px;font-weight:bold;">
    {e(data["runa"])}
  </div>
</div>

<div id="msg-it" style="margin-top:16px;font-size:18px;">
  {e(data["messaggio_it"])}
</div>

<div id="msg-en" style="opacity:.7;margin-top:6px;">
  {e(data["messaggio_en"])}
</div>

<a href="#" id="cta"
style="display:inline-block;margin-top:28px;
padding:16px 26px;border-radius:999px;
background:#ffd27a;color:#1a1206;
font-weight:bold;text-decoration:none;">
{CTA_TEXT}
</a>

</div>

<script>
(function(){{
  const btn = document.getElementById("cta");
  const rName = document.getElementById("runa-name");
  const rSym  = document.getElementById("runa-symbol");
  const msgIt = document.getElementById("msg-it");
  const msgEn = document.getElementById("msg-en");

  function speak(text){{
    if(!("speechSynthesis" in window)) return;
    const u = new SpeechSynthesisUtterance(text);
    u.lang = "it-IT";
    u.rate = 1.02;
    speechSynthesis.cancel();
    speechSynthesis.speak(u);
  }}

  btn.onclick = async function(e){{
    e.preventDefault();
    btn.textContent = "… in ascolto";
    const res = await fetch("/oracle?elemento={e(data["elemento"])}&nonce="+Date.now());
    const d = await res.json();

    rName.textContent = d.runa;
    rSym.textContent  = d.runa_symbol;
    msgIt.textContent = d.messaggio_it;
    msgEn.textContent = d.messaggio_en;

    speak(d.messaggio_it);
    btn.textContent = "{CTA_TEXT}";
  }};
}})();
</script>

</body>
</html>
"""
    return make_response(html)
