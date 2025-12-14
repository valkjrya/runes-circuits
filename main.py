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

# =========================
# DATI BASE
# =========================
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

# =========================
# RUNE + SIMBOLI
# =========================
RUNE_PER_ELEMENTO = {
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

# =========================
# MESSAGGI UNICI PER RUNA
# =========================
RUNA_MESSAGES = {
    "Fehu": (
        "Ciò che possiedi cresce se lo condividi con consapevolezza.",
        "What you hold grows when shared with awareness."
    ),
    "Uruz": (
        "La forza è già in te: usala senza forzarla.",
        "Strength is already within you: use it without strain."
    ),
    "Berkano": (
        "Proteggi ciò che nasce, anche se è fragile.",
        "Protect what is being born, even if it is fragile."
    ),
    "Jera": (
        "Ogni cosa arriva nel tempo giusto. Abbi fiducia.",
        "Everything arrives in its right time. Trust the cycle."
    ),
    "Laguz": (
        "Lascia scorrere. La risposta arriva senza sforzo.",
        "Let it flow. The answer arrives without force."
    ),
    "Perthro": (
        "Il mistero non va risolto: va attraversato.",
        "The mystery is not to be solved, but crossed."
    ),
    "Eihwaz": (
        "Rimani nel passaggio: la trasformazione è in atto.",
        "Stay in the passage: transformation is underway."
    ),
    "Isa": (
        "Fermati. Nel silenzio trovi chiarezza.",
        "Pause. In stillness, clarity emerges."
    ),
    "Ansuz": (
        "Ascolta il messaggio: sta già parlando.",
        "Listen to the message: it is already speaking."
    ),
    "Raido": (
        "Il viaggio è iniziato: muoviti con intenzione.",
        "The journey has begun: move with intention."
    ),
    "Gebo": (
        "Dare e ricevere sono lo stesso gesto.",
        "Giving and receiving are the same movement."
    ),
    "Wunjo": (
        "La gioia arriva quando smetti di cercarla.",
        "Joy arrives when you stop chasing it."
    ),
    "Kenaz": (
        "Una scintilla illumina ciò che era nascosto.",
        "A spark reveals what was hidden."
    ),
    "Sowilo": (
        "La luce è dalla tua parte. Avanza.",
        "The light is on your side. Move forward."
    ),
    "Tiwaz": (
        "Accendi il coraggio: una scelta ti libera.",
        "Ignite courage: one choice sets you free."
    ),
    "Hagalaz": (
        "Il cambiamento rompe ciò che non serve più.",
        "Change breaks what no longer serves."
    ),
    "Algiz": (
        "Sei protetta mentre resti fedele a te.",
        "You are protected while staying true to yourself."
    ),
    "Dagaz": (
        "Una nuova visione si apre ora.",
        "A new vision opens now."
    ),
    "Nauthiz": (
        "La necessità rivela la via.",
        "Necessity reveals the path."
    ),
    "Othila": (
        "Riconosci ciò che ti appartiene davvero.",
        "Recognize what truly belongs to you."
    ),
}

# =========================
# ORACOLO
# =========================
def genera_oracolo(elemento):
    elemento = elemento if elemento in ELEMENTI else random.choice(ELEMENTI)

    # seed sempre diverso
    seed = f"{dt.datetime.utcnow().isoformat()}:{random.random()}"
    rng = random.Random(seed)

    runa = rng.choice(RUNE_PER_ELEMENTO[elemento])
    simbolo = RUNE_SYMBOL.get(runa, "ᚱ")
    msg_it, msg_en = RUNA_MESSAGES[runa]

    return {
        "elemento": elemento,
        "colore": COLORI[elemento],
        "segni": SEGNI[elemento],
        "runa": runa,
        "runa_symbol": simbolo,
        "messaggio_it": msg_it,
        "messaggio_en": msg_en,
        "seed": seed,
        "ts": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z"
    }

# =========================
# API
# =========================
@app.get("/oracle")
def oracle():
    elemento = request.args.get("elemento", "RANDOM").upper()
    return jsonify(genera_oracolo(elemento))

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

<div style="display:flex;align-items:center;gap:14px;">
  <div id="runa-symbol" style="font-size:42px;">{e(data["runa_symbol"])}</div>
  <div id="runa-name" style="font-size:36px;font-weight:bold;">
    {e(data["runa"])}
  </div>
</div>

<div id="msg-it" style="margin-top:16px;font-size:20px;">
  {e(data["messaggio_it"])}
</div>

<div id="msg-en" style="opacity:.7;margin-top:6px;">
  {e(data["messaggio_en"])}
</div>

<a href="#" id="cta"
style="display:inline-block;margin-top:28px;
padding:16px 28px;border-radius:999px;
background:#ffd27a;color:#1a1206;
font-weight:900;text-decoration:none;">
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
