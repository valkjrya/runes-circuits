import os
import random
import datetime as dt
from html import escape
from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

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
    "SPAZIO": ["Oltre i segni", "Tra le stelle", "Nel varco"],
}

# ✅ simboli (inclusi Thurisaz, Ingwaz, Ehwaz)
RUNE_SYMBOL = {
    "Fehu": "ᚠ",
    "Uruz": "ᚢ",
    "Thurisaz": "ᚦ",
    "Ansuz": "ᚨ",
    "Raido": "ᚱ",
    "Kenaz": "ᚲ",
    "Gebo": "ᚷ",
    "Wunjo": "ᚹ",
    "Hagalaz": "ᚺ",
    "Nauthiz": "ᚾ",
    "Isa": "ᛁ",
    "Jera": "ᛃ",
    "Eihwaz": "ᛇ",
    "Perthro": "ᛈ",
    "Algiz": "ᛉ",
    "Sowilo": "ᛋ",
    "Tiwaz": "ᛏ",
    "Berkana": "ᛒ",
    "Ehwaz": "ᛖ",
    "Mannaz": "ᛗ",
    "Laguz": "ᛚ",
    "Ingwaz": "ᛜ",
    "Dagaz": "ᛞ",
    "Othila": "ᛟ",
}

# ✅ ORDINE ESATTO che hai richiesto
RUNE_PER_ELEMENTO = {
    "TERRA": ["Algiz", "Eihwaz", "Uruz", "Wunjo", "Berkana", "Othila", "Isa", "Jera"],
    "ACQUA": ["Perthro", "Laguz", "Ingwaz", "Raido", "Gebo", "Hagalaz"],
    "ARIA": ["Algiz", "Ansuz", "Tiwaz", "Berkana", "Ehwaz"],
    "FUOCO": ["Dagaz", "Othila", "Fehu", "Thurisaz", "Nauthiz", "Eihwaz"],
    "SPAZIO": ["Algiz", "Dagaz", "Perthro", "Eihwaz"],
}

# ✅ frasi per tutte le rune usate nelle liste sopra
RUNE_VARIANTS_IT = {
    "Algiz": [
        "Sei protetta mentre resti fedele a te.",
        "Oggi lo scudo è la tua verità.",
        "Cammina con dignità: la protezione ti segue.",
        "Non temere: ciò che è tuo è custodito.",
    ],
    "Eihwaz": [
        "Tra radice e cielo: sei il ponte.",
        "Resisti senza irrigidirti: la via si apre.",
        "Il limite è una soglia, non un muro.",
        "Oggi la trasformazione lavora in profondità.",
    ],
    "Uruz": [
        "La forza è già in te: usala senza forzarla.",
        "Oggi un passo deciso basta a spostare montagne.",
        "Forza non è muscoli: è presenza totale.",
        "Il tuo istinto è la bussola migliore.",
    ],
    "Wunjo": [
        "La gioia arriva quando smetti di inseguirla.",
        "Oggi il sorriso è già dentro.",
        "La gioia non si insegue: si respira.",
        "Sii felice senza motivo: è potere puro.",
    ],
    "Berkana": [
        "Proteggi ciò che nasce, anche se è fragile.",
        "La crescita lenta è la più forte.",
        "Accogli il nuovo senza fretta.",
        "Lascia che fiorisca nel tuo silenzio.",
    ],
    "Othila": [
        "Riconosci ciò che ti appartiene davvero.",
        "Torna alla radice: lì c'è forza.",
        "Ciò che è tuo non si perde.",
        "Onora l'eredità, ma crea il tuo ramo.",
    ],
    "Isa": [
        "Fermati. Nel silenzio trovi chiarezza.",
        "La pausa è potere.",
        "Non muoverti: ascolta il vuoto.",
        "Lascia che la verità si sedimenti.",
    ],
    "Jera": [
        "Ogni cosa arriva nel tempo giusto. Abbi fiducia.",
        "La ruota gira lenta, ma gira.",
        "Oggi il tempo lavora per te.",
        "Non forzare: la stagione sa.",
    ],
    "Perthro": [
        "Il mistero non va risolto: va attraversato.",
        "Accetta l'ignoto: è il tuo alleato.",
        "Un velo si alza piano: guarda.",
        "Rimani nel passaggio: la trasformazione è in atto.",
    ],
    "Laguz": [
        "Lascia scorrere. La risposta arriva senza sforzo.",
        "Non combattere la corrente: vai con lei.",
        "L'intuizione è la tua corrente.",
        "Non afferrare: l'onda ti porta.",
    ],
    "Ingwaz": [
        "Il seme è pronto: ora può diventare vita.",
        "Dentro di te matura qualcosa di vero.",
        "Chiudi un ciclo con dolcezza: è fertilità, non fine.",
        "Radica l’intento: il futuro germoglia nel silenzio.",
    ],
    "Raido": [
        "Il viaggio è iniziato: muoviti con intenzione.",
        "Oggi un passo cambia tutto.",
        "Scegli la direzione, poi fidati della strada.",
        "Il movimento è una preghiera.",
    ],
    "Gebo": [
        "Dare e ricevere sono lo stesso gesto.",
        "L'equilibrio è nel tuo cuore.",
        "La connessione è reciproca.",
        "Oggi un dono torna in altra forma.",
    ],
    "Hagalaz": [
        "Il cambiamento rompe ciò che non serve più.",
        "Lascia che cada: rinasci.",
        "Nel caos c'è un ordine nascosto.",
        "Oggi la tempesta pulisce l’aria.",
    ],
    "Ansuz": [
        "Ascolta: la parola giusta arriva dal vento.",
        "Il messaggio è già qui: leggilo tra le righe.",
        "Parla solo quando senti presenza.",
        "Oggi la verità si dice con delicatezza.",
    ],
    "Tiwaz": [
        "Accendi il coraggio: una scelta ti libera.",
        "Agisci con rettitudine: la via si apre.",
        "La decisione è la tua forza.",
        "Scegli ciò che è giusto, non ciò che è facile.",
    ],
    "Ehwaz": [
        "Avanza: il cambiamento si muove con te.",
        "Oggi fidati della collaborazione: non sei sola.",
        "Il ritmo giusto ti porta lontano.",
        "Muoviti in armonia: l’energia ti sostiene.",
    ],
    "Dagaz": [
        "Una nuova visione si apre ora.",
        "Tra notte e giorno: scegli il risveglio.",
        "La luce cambia tutto, anche te.",
        "Oggi l’alba nasce dentro.",
    ],
    "Fehu": [
        "Ciò che possiedi cresce se lo condividi con consapevolezza.",
        "La vera ricchezza è invisibile: inizia dal cuore.",
        "Non trattenere: l’abbondanza ama il flusso.",
        "Oggi semina fiducia: il raccolto è vicino.",
    ],
    "Thurisaz": [
        "Proteggi il confine: scegli cosa far entrare.",
        "La forza va guidata, non lasciata libera.",
        "Oggi taglia ciò che ti consuma.",
        "Il coraggio è dire NO quando serve.",
    ],
    "Nauthiz": [
        "La necessità rivela la via.",
        "Oggi il bisogno ti guida.",
        "La stretta è una lezione: ascoltala.",
        "Sopravvivi: e poi fiorisci.",
    ],
}

def _norm_elemento(x: str) -> str:
    x = (x or "RANDOM").strip().upper()
    if x in ELEMENTI:
        return x
    return random.choice(ELEMENTI)

def genera_oracolo(elemento: str, nonce: str | None = None) -> dict:
    """
    - nonce None      -> oracolo del giorno (stabile per elemento)
    - nonce presente  -> cambia ad ogni click (seed diverso)
    """
    elemento = _norm_elemento(elemento)
    oggi = dt.date.today().isoformat()

    base_seed = f"runa-{elemento}-{oggi}"
    seed = base_seed if not nonce else f"{base_seed}-{nonce}"
    rng = random.Random(seed)

    rune_list = RUNE_PER_ELEMENTO.get(elemento) or []
    if not rune_list:
        rune_list = list(RUNE_SYMBOL.keys())

    runa = rng.choice(rune_list)
    simbolo = RUNE_SYMBOL.get(runa, "ᚱ")

    varianti = RUNE_VARIANTS_IT.get(runa) or ["Oggi ascolta. La runa parla in silenzio."]
    msg_it = rng.choice(varianti)
    msg_en = "Today: " + msg_it.replace("Oggi", "Today").replace("oggi", "today")

    return {
        "elemento": elemento,
        "colore": COLORI.get(elemento, ""),
        "segni": SEGNI.get(elemento, []),
        "runa": runa,
        "runa_symbol": simbolo,
        "messaggio_it": msg_it,
        "messaggio_en": msg_en,
        "seed": seed,
        "ts": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }

@app.get("/oracle")
def oracle():
    elemento = request.args.get("elemento", "RANDOM")
    nonce = request.args.get("nonce")
    return jsonify(genera_oracolo(elemento, nonce=nonce))

@app.get("/")
@app.get("/view")
def view():
    elemento = request.args.get("elemento", "RANDOM")
    data = genera_oracolo(elemento, nonce=None)  # oracolo quotidiano sul primo caricamento

    html = """<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__ — __SUBTITLE__</title>
</head>
<body style="margin:0;background:#020308;color:#f6f3ff;font-family:system-ui,Segoe UI,Arial;">
  <div style="max-width:900px;margin:40px auto;padding:24px;">
    <h1 style="text-align:center;">✨ __SUBTITLE__</h1>
    <div style="opacity:.85;text-align:center;margin-top:-10px;">__TITLE__</div>

    <div style="margin-top:26px;padding:18px;border:1px solid rgba(255,255,255,.12);border-radius:16px;">
      <div style="display:flex;align-items:center;justify-content:center;gap:14px;">
        <div id="runa-symbol" style="font-size:52px;line-height:1;">__RUNA_SYMBOL__</div>
        <div>
          <div style="opacity:.75;font-size:14px;">
            Elemento: <b id="el">__ELEMENTO__</b> — Colore: <span id="col">__COLORE__</span>
          </div>
          <div id="runa-name" style="font-size:34px;font-weight:900;margin-top:4px;">__RUNA__</div>
        </div>
      </div>

      <div id="msg-it" style="margin-top:18px;font-size:20px;text-align:center;">__MSG_IT__</div>
      <div id="msg-en" style="opacity:.7;margin-top:8px;text-align:center;">__MSG_EN__</div>

      <div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;margin-top:18px;">
        <a href="#" id="cta"
           style="display:inline-block;padding:16px 28px;border-radius:999px;background:#ffd27a;color:#1a1206;font-weight:900;text-decoration:none;">
          __CTA__
        </a>
      </div>

      <div style="opacity:.55;font-size:12px;margin-top:14px;text-align:center;">
        Seed: <span id="seed">__SEED__</span>
      </div>
    </div>
  </div>

<script>
(function(){
  const btn   = document.getElementById("cta");
  const el    = document.getElementById("el");
  const col   = document.getElementById("col");
  const rName = document.getElementById("runa-name");
  const rSym  = document.getElementById("runa-symbol");
  const msgIt = document.getElementById("msg-it");
  const msgEn = document.getElementById("msg-en");
  const seed  = document.getElementById("seed");

  function speak(text){
    if(!("speechSynthesis" in window)) return;
    const u = new SpeechSynthesisUtterance(text);
    u.lang = "it-IT";
    u.rate = 1.02;
    speechSynthesis.cancel();
    speechSynthesis.speak(u);
  }

  btn.onclick = async function(ev){
    ev.preventDefault();
    btn.textContent = "… in ascolto";
    try{
      const elemento = el.textContent || "RANDOM";
      const res = await fetch("/oracle?elemento=" + encodeURIComponent(elemento) + "&nonce=" + Date.now());
      const d = await res.json();
      el.textContent    = d.elemento;
      col.textContent   = d.colore || "";
      rName.textContent = d.runa;
      rSym.textContent  = d.runa_symbol;
      msgIt.textContent = d.messaggio_it;
      msgEn.textContent = d.messaggio_en;
      seed.textContent  = d.seed;
      speak(d.messaggio_it);
    }catch(err){
      console.error(err);
      msgIt.textContent = "Errore nel contattare l'oracolo. Riprova.";
    }finally{
      btn.textContent = "__CTA__";
    }
  };
})();
</script>

</body>
</html>
"""

    def e(x): return escape(str(x))

    html = (
        html.replace("__TITLE__", e(TITLE))
            .replace("__SUBTITLE__", e(SUBTITLE))
            .replace("__CTA__", e(CTA_TEXT))
            .replace("__ELEMENTO__", e(data["elemento"]))
            .replace("__COLORE__", e(data["colore"]))
            .replace("__RUNA__", e(data["runa"]))
            .replace("__RUNA_SYMBOL__", e(data["runa_symbol"]))
            .replace("__MSG_IT__", e(data["messaggio_it"]))
            .replace("__MSG_EN__", e(data["messaggio_en"]))
            .replace("__SEED__", e(data["seed"]))
    )

    return make_response(html)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port, debug=True)
