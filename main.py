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

RUNE_SYMBOL = {
    "Fehu": "ᚠ", "Uruz": "ᚢ", "Ansuz": "ᚨ", "Raido": "ᚱ", "Kenaz": "ᚲ", "Gebo": "ᚷ",
    "Wunjo": "ᚹ", "Hagalaz": "ᚺ", "Nauthiz": "ᚾ", "Isa": "ᛁ", "Jera": "ᛃ",
    "Eihwaz": "ᛇ", "Perthro": "ᛈ", "Algiz": "ᛉ", "Sowilo": "ᛋ", "Tiwaz": "ᛏ",
    "Berkano": "ᛒ", "Laguz": "ᛚ", "Dagaz": "ᛞ", "Othila": "ᛟ",
}

RUNE_PER_ELEMENTO = {
    "TERRA": ["Fehu", "Uruz", "Berkano", "Jera", "Othila"],
    "ACQUA": ["Laguz", "Perthro", "Isa", "Eihwaz"],
    "ARIA": ["Ansuz", "Raido", "Gebo", "Wunjo"],
    "FUOCO": ["Kenaz", "Sowilo", "Tiwaz", "Hagalaz", "Nauthiz"],
    "SPAZIO": ["Dagaz", "Algiz", "Perthro", "Eihwaz"],
}

RUNE_VARIANTS_IT = {
    "Fehu": [
        "Ciò che possiedi cresce se lo condividi con consapevolezza.",
        "La vera ricchezza è invisibile: inizia dal cuore.",
        "Un gesto generoso oggi, un raccolto domani.",
        "Non trattenere: l'abbondanza ama il flusso.",
        "Oggi semina fiducia: il raccolto è vicino.",
    ],
    "Uruz": [
        "La forza è già in te: usala senza forzarla.",
        "Respira. Il tuo corpo sa più di quanto pensi.",
        "Oggi un passo deciso basta a spostare montagne.",
        "Forza non è muscoli: è presenza totale.",
        "Il tuo istinto è la bussola migliore.",
    ],
    "Berkano": [
        "Proteggi ciò che nasce, anche se è fragile.",
        "La crescita lenta è la più forte.",
        "Accogli il nuovo senza fretta.",
        "Lascia che fiorisca nel tuo silenzio.",
        "Il seme che curi oggi ti salva domani.",
    ],
    "Jera": [
        "Ogni cosa arriva nel tempo giusto. Abbi fiducia.",
        "Oggi raccogli ciò che hai seminato ieri.",
        "La ruota gira lenta, ma gira.",
        "Non forzare: la stagione sa.",
        "Il tuo momento è vicino, respira.",
    ],
    "Laguz": [
        "Lascia scorrere. La risposta arriva senza sforzo.",
        "Oggi l'acqua lava via il peso.",
        "Non combattere la corrente: vai con lei.",
        "L'intuizione è la tua corrente.",
        "Non afferrare: l'onda ti porta.",
    ],
    "Perthro": [
        "Il mistero non va risolto: va attraversato.",
        "Accetta l'ignoto: è il tuo alleato.",
        "Un velo si alza piano: guarda.",
        "Rimani nel passaggio: la trasformazione è in atto.",
        "Respira nel vuoto: lì nasce il nuovo.",
    ],
    "Isa": [
        "Fermati. Nel silenzio trovi chiarezza.",
        "La pausa è potere.",
        "Non muoverti: ascolta il vuoto.",
        "Il gelo ti protegge da scelte impulsive.",
        "Lascia che la verità si sedimenti.",
    ],
    "Eihwaz": [
        "Tra radice e cielo: sei il ponte.",
        "Resisti senza irrigidirti: la via si apre.",
        "La stabilità è un atto interiore.",
        "Il limite è una soglia, non un muro.",
        "La trasformazione è già iniziata.",
    ],
    "Ansuz": [
        "Ascolta: la parola giusta arriva dal vento.",
        "Una frase può aprire un portale.",
        "Il messaggio è già qui: leggilo tra le righe.",
        "Parla solo quando senti presenza.",
        "Oggi la verità si dice con delicatezza.",
    ],
    "Raido": [
        "Il viaggio è iniziato: muoviti con intenzione.",
        "Oggi un passo cambia tutto.",
        "Non correre: cammina consapevole.",
        "Scegli la direzione, poi fidati della strada.",
        "Il movimento è una preghiera.",
    ],
    "Gebo": [
        "Dare e ricevere sono lo stesso gesto.",
        "Oggi un dono torna indietro in altra forma.",
        "L'equilibrio è nel tuo cuore.",
        "Non contare: scambia.",
        "La connessione è reciproca.",
    ],
    "Wunjo": [
        "La gioia arriva quando smetti di cercarla.",
        "Oggi il sorriso è già dentro.",
        "Sii felice senza motivo.",
        "La luce è tua: accoglila.",
        "La gioia non si insegue: si respira.",
    ],
    "Kenaz": [
        "Una scintilla illumina ciò che era nascosto.",
        "Oggi vedi chiaro.",
        "Accendi la creatività e cambia il quadro.",
        "Non temere l'ombra: portaci luce.",
        "Il fuoco interiore sa la strada.",
    ],
    "Sowilo": [
        "La luce è dalla tua parte. Avanza.",
        "Oggi il sole ti segue.",
        "Non nasconderti: splendi.",
        "La vittoria è già tua se resti vero.",
        "Usa il giorno: è un alleato.",
    ],
    "Tiwaz": [
        "Accendi il coraggio: una scelta ti libera.",
        "Agisci con rettitudine: la via si apre.",
        "Oggi scegli ciò che è giusto, non ciòche è facile.",
        "La decisione è la tua forza.",
        "La tua volontà è una lama pulita.",
    ],
    "Hagalaz": [
        "Il cambiamento rompe ciò che non serve più.",
        "Lascia che cada: rinasci.",
        "Nel caos c'è un ordine nascosto.",
        "Oggi la grandine pulisce l'aria.",
        "Non resistere al vero: trasformalo.",
    ],
    "Nauthiz": [
        "La necessità rivela la via.",
        "Oggi il bisogno ti guida.",
        "La stretta è una lezione: ascoltala.",
        "Sopravvivi: e poi fiorisci.",
        "La fame di verità accende il passo.",
    ],
    "Algiz": [
        "Sei protetta mentre resti fedele a te.",
        "Oggi il tuo scudo è vivo.",
        "Resta vera: niente ti tocca.",
        "La protezione è dentro, non fuori.",
        "Cammina con dignità: sei guardata.",
    ],
    "Dagaz": [
        "Una nuova visione si apre ora.",
        "Oggi l'alba è dentro di te.",
        "Il buio finisce: cambia prospettiva.",
        "Tra notte e giorno: scegli il risveglio.",
        "La luce cambia tutto, anche te.",
    ],
    "Othila": [
        "Riconosci ciò che ti appartiene davvero.",
        "Torna alla radice: lì c'è forza.",
        "La casa è un luogo interiore.",
        "Ciò che è tuo non si perde.",
        "Onora l'eredità, ma crea il tuo ramo.",
    ],
}

def genera_oracolo(elemento: str) -> dict:
    elemento = (elemento or "RANDOM").strip().upper()
    if elemento not in ELEMENTI:
        elemento = random.choice(ELEMENTI)

    oggi = dt.date.today().isoformat()
    seed = f"runa-{elemento}-{oggi}"
    rng = random.Random(seed)

    rune_list = RUNE_PER_ELEMENTO.get(elemento) or list(RUNE_SYMBOL.keys())
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
    return jsonify(genera_oracolo(elemento))

@app.get("/")
@app.get("/view")
def view():
    elemento = request.args.get("elemento", "RANDOM")
    data = genera_oracolo(elemento)

    # niente f-string: così JS con {} non rompe Python
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
        Seed giornaliero: <span id="seed">__SEED__</span>
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

    def e(x):
        return escape(str(x))

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
