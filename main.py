import os
import random
import datetime as dt
from html import escape
from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

TITLE = "RUNES & CIRCUITS"
SUBTITLE = "Rune Parlanti"
CTA_TEXT = "DIVINAZIONE"

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

# Alias -> forma canonica
RUNE_ALIAS = {
    "OTHALA": "Othila",
    "OTHILA": "Othila",
    "SOWULO": "Sowilo",
    "SOWILO": "Sowilo",
    "TEIWAZ": "Tiwaz",
    "TIWAZ": "Tiwaz",
    "RAIDHO": "Raido",
    "RAIDHO'": "Raido",
    "RAIDHO’": "Raido",
    "PERTHU": "Perthro",
    "PERTHRO": "Perthro",
    "KAUNAZ": "Kenaz",
    "KENAZ": "Kenaz",
}

def canon_rune(name: str) -> str:
    if not name:
        return name
    key = name.strip().upper()
    return RUNE_ALIAS.get(key, name.strip().title())

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
    "Ehwaz": "ᛖ",
    "Mannaz": "ᛗ",
    "Laguz": "ᛚ",
    "Ingwaz": "ᛜ",
    "Dagaz": "ᛞ",
    "Othila": "ᛟ",
    "Perthro": "ᛈ",
    "Algiz": "ᛉ",
    "Sowilo": "ᛋ",
    "Tiwaz": "ᛏ",
    "Berkana": "ᛒ",
}

# ✅ tuo ordine richiesto
RUNE_PER_ELEMENTO = {
    "TERRA": list(map(canon_rune, ["Othala", "Wunjo", "Isa", "Uruz", "Jera"])),
    "ACQUA": list(map(canon_rune, ["Ingwaz", "Raidho", "Hagalaz", "Perthu", "Laguz"])),
    "ARIA":  list(map(canon_rune, ["Teiwaz", "Sowulo", "Ansuz", "Ehwaz"])),
    "FUOCO": list(map(canon_rune, ["Kaunaz", "Dagaz", "Nauthiz", "Mannaz", "Thurisaz"])),
    "SPAZIO": list(map(canon_rune, ["Berkana", "Algiz", "Gebo", "Ehwaz", "Fehu"])),
}

RUNE_VARIANTS_IT = {
    "Othila": [
        "Riconosci ciò che ti appartiene davvero.",
        "Torna alla radice: lì c'è forza.",
        "Ciò che è tuo non si perde.",
        "Proteggi i tuoi confini con amore.",
    ],
    "Wunjo": [
        "La gioia arriva quando smetti di inseguirla.",
        "Oggi il sorriso è già dentro.",
        "La gioia non si insegue: si respira.",
        "Lascia spazio al piacere semplice.",
    ],
    "Isa": [
        "Fermati. Nel silenzio trovi chiarezza.",
        "La pausa è potere.",
        "Rallenta: la verità si deposita da sola.",
        "Il gelo protegge da scelte impulsive.",
    ],
    "Uruz": [
        "La forza è già in te: usala senza forzarla.",
        "Oggi un passo deciso basta a spostare montagne.",
        "Forza è presenza totale, non sforzo.",
        "Il tuo istinto è la bussola migliore.",
    ],
    "Jera": [
        "Ogni cosa arriva nel tempo giusto. Abbi fiducia.",
        "La ruota gira lenta, ma gira.",
        "Non forzare: la stagione sa.",
        "Oggi il tempo lavora per te.",
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
    "Hagalaz": [
        "Il cambiamento rompe ciò che non serve più.",
        "Lascia che cada: rinasci.",
        "Nel caos c'è un ordine nascosto.",
        "Oggi la tempesta pulisce l’aria.",
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
    "Tiwaz": [
        "Accendi il coraggio: una scelta ti libera.",
        "Agisci con rettitudine: la via si apre.",
        "Scegli ciò che è giusto, non ciò che è facile.",
        "La decisione è la tua forza.",
    ],
    "Sowilo": [
        "La luce è dalla tua parte. Avanza.",
        "Non nasconderti: splendi.",
        "Usa il giorno: è un alleato.",
        "Lascia che la tua energia illumini.",
    ],
    "Ansuz": [
        "Ascolta: la parola giusta arriva dal vento.",
        "Il messaggio è già qui: leggilo tra le righe.",
        "Parla solo quando senti presenza.",
        "Oggi la verità si dice con delicatezza.",
    ],
    "Ehwaz": [
        "Avanza: il cambiamento si muove con te.",
        "Oggi fidati della collaborazione: non sei sola.",
        "Il ritmo giusto ti porta lontano.",
        "Muoviti in armonia: l’energia ti sostiene.",
    ],
    "Kenaz": [
        "Una scintilla illumina ciò che era nascosto.",
        "Oggi vedi chiaro.",
        "Accendi la creatività e cambia il quadro.",
        "Porta luce dove prima c’era dubbio.",
    ],
    "Dagaz": [
        "Una nuova visione si apre ora.",
        "Tra notte e giorno: scegli il risveglio.",
        "La luce cambia tutto, anche te.",
        "Oggi l’alba nasce dentro.",
    ],
    "Nauthiz": [
        "La necessità rivela la via.",
        "Oggi il bisogno ti guida.",
        "La stretta è una lezione: ascoltala.",
        "Sopravvivi: e poi fiorisci.",
    ],
    "Mannaz": [
        "La tua forza cresce quando ti ricordi chi sei.",
        "Oggi scegli l’umano: presenza, verità, relazione.",
        "Specchiati negli altri senza perderti.",
        "Il coraggio più grande è essere autentici.",
    ],
    "Thurisaz": [
        "Proteggi il confine: scegli cosa far entrare.",
        "La forza va guidata, non lasciata libera.",
        "Oggi taglia ciò che ti consuma.",
        "Il coraggio è dire NO quando serve.",
    ],
    "Berkana": [
        "Proteggi ciò che nasce, anche se è fragile.",
        "La crescita lenta è la più forte.",
        "Accogli il nuovo senza fretta.",
        "Lascia che fiorisca nel tuo silenzio.",
    ],
    "Algiz": [
        "Sei protetta mentre resti fedele a te.",
        "Oggi lo scudo è la tua verità.",
        "Cammina con dignità: la protezione ti segue.",
        "Non temere: ciò che è tuo è custodito.",
    ],
    "Gebo": [
        "Dare e ricevere sono lo stesso gesto.",
        "L'equilibrio è nel tuo cuore.",
        "La connessione è reciproca.",
        "Oggi un dono torna in altra forma.",
    ],
    "Fehu": [
        "Ciò che possiedi cresce se lo condividi con consapevolezza.",
        "La vera ricchezza è invisibile: inizia dal cuore.",
        "Non trattenere: l’abbondanza ama il flusso.",
        "Oggi semina fiducia: il raccolto è vicino.",
    ],
}

def _norm_elemento(x: str) -> str:
    x = (x or "RANDOM").strip().upper()
    if x in ELEMENTI:
        return x
    return random.choice(ELEMENTI)

def _simple_en(it_text: str) -> str:
    t = it_text.strip()
    t = t.replace("Oggi", "Today").replace("oggi", "today")
    return t

def genera_oracolo(elemento: str, nonce: str | None = None) -> dict:
    elemento = _norm_elemento(elemento)
    oggi = dt.date.today().isoformat()

    base_seed = f"runa-{elemento}-{oggi}"
    seed = base_seed if not nonce else f"{base_seed}-{nonce}"
    rng = random.Random(seed)

    rune_list = RUNE_PER_ELEMENTO.get(elemento) or list(RUNE_SYMBOL.keys())
    runa = rng.choice(rune_list)
    simbolo = RUNE_SYMBOL.get(runa, "ᚱ")

    varianti = RUNE_VARIANTS_IT.get(runa) or ["Oggi ascolta. La runa parla in silenzio."]
    msg_it = rng.choice(varianti)
    msg_en = _simple_en(msg_it)

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
    data = genera_oracolo(elemento, nonce=None)

    html = """<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__ — __SUBTITLE__</title>
<style>
  :root{
    --bg:#020308;
    --fg:#f6f3ff;
    --muted:rgba(246,243,255,.70);
    --border:rgba(255,255,255,.12);
    --cta:#ffd27a;
    --ctaText:#1a1206;
  }
  body{margin:0;background:var(--bg);color:var(--fg);font-family:system-ui,Segoe UI,Arial;}
  .wrap{max-width:900px;margin:40px auto;padding:24px;}
  .card{margin-top:18px;padding:18px;border:1px solid var(--border);border-radius:18px;position:relative;overflow:hidden;}
  .top{display:flex;align-items:center;justify-content:center;gap:12px;}
  h1{margin:0;}
  .sub{opacity:.85;text-align:center;margin-top:6px;}

  .meta{opacity:.75;font-size:14px;text-align:center;margin-top:10px;}
  .rline{display:flex;align-items:center;justify-content:center;gap:14px;margin-top:16px;position:relative;}
  #runa-symbol{
    font-size:66px;line-height:1;
    text-shadow: 0 0 0 rgba(255,255,255,0);
    transition: text-shadow .22s ease, transform .22s ease, filter .22s ease;
    filter: brightness(1.0);
    position:relative;
  }

  /* Cerchi energetici (portale) */
  .ring{
    position:absolute;
    left:50%; top:50%;
    width:10px; height:10px;
    transform: translate(-50%,-50%);
    border-radius:999px;
    border:1px solid rgba(255,210,122,.35);
    box-shadow:
      0 0 10px rgba(255,210,122,.22),
      0 0 22px rgba(255,255,255,.14);
    opacity:0;
    pointer-events:none;
  }
  .ring.r1{border-color: rgba(255,210,122,.45);}
  .ring.r2{border-color: rgba(255,255,255,.25);}
  .ring.r3{border-color: rgba(255,210,122,.25);}

  @keyframes ripple {
    0%   {opacity:0; transform:translate(-50%,-50%) scale(0.25);}
    15%  {opacity:1;}
    100% {opacity:0; transform:translate(-50%,-50%) scale(10);}
  }

  /* Particelle leggere */
  .spark{
    position:absolute;
    left:50%; top:50%;
    width:4px; height:4px;
    border-radius:999px;
    background: rgba(255,210,122,.9);
    box-shadow: 0 0 10px rgba(255,210,122,.55), 0 0 18px rgba(255,255,255,.22);
    opacity:0;
    transform: translate(-50%,-50%);
    pointer-events:none;
  }
  @keyframes spark {
    0%   {opacity:0; transform:translate(-50%,-50%) scale(0.6);}
    10%  {opacity:1;}
    100% {opacity:0; transform:translate(calc(-50% + var(--dx)), calc(-50% + var(--dy))) scale(0.2);}
  }

  /* Glow teatrale sulla runa */
  .glow #runa-symbol{
    filter: brightness(1.25);
    transform: scale(1.03);
    text-shadow:
      0 0 16px rgba(255,255,255,.55),
      0 0 34px rgba(255,210,122,.38),
      0 0 70px rgba(255,210,122,.20);
  }

  .msg{margin-top:16px;text-align:center;}
  #msg-it{font-size:20px;}
  #msg-en{opacity:.72;margin-top:8px;}

  .ctaRow{display:flex;justify-content:center;margin-top:18px;}
  #cta{
    display:inline-block;padding:16px 28px;border-radius:999px;
    background:var(--cta);color:var(--ctaText);
    font-weight:900;text-decoration:none;
  }
  .seed{opacity:.55;font-size:12px;margin-top:14px;text-align:center;}
</style>
</head>
<body>
  <div class="wrap">
    <div class="top">
      <h1>✨ __SUBTITLE__</h1>
    </div>
    <div class="sub">__TITLE__</div>

    <div class="card">
      <div class="meta">
        Elemento: <b id="el">__ELEMENTO__</b> — Colore: <span id="col">__COLORE__</span>
      </div>

      <div class="rline" id="rline">
        <div class="ring r1"></div>
        <div class="ring r2"></div>
        <div class="ring r3"></div>
        <div id="runa-symbol">__RUNA_SYMBOL__</div>
        <div>
          <div id="runa-name" style="font-size:34px;font-weight:900;">__RUNA__</div>
        </div>
      </div>

      <div class="msg">
        <div id="msg-it">__MSG_IT__</div>
        <div id="msg-en">__MSG_EN__</div>
      </div>

      <div class="ctaRow">
        <a href="#" id="cta">__CTA__</a>
      </div>

      <div class="seed">
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
  const rline = document.getElementById("rline");
  const card  = document.querySelector(".card");
  const rings = Array.from(document.querySelectorAll(".ring"));

  function speakItalian(text){
    if(!("speechSynthesis" in window)) return;
    const u = new SpeechSynthesisUtterance(text);
    u.lang = "it-IT";
    u.rate = 1.02;
    speechSynthesis.cancel();
    speechSynthesis.speak(u);
  }

  function spawnSparks(){
    // 6 particelle con direzioni random
    for(let i=0;i<6;i++){
      const s = document.createElement("div");
      s.className = "spark";
      const dx = (Math.random()*160 - 80).toFixed(0) + "px";
      const dy = (Math.random()*140 - 70).toFixed(0) + "px";
      s.style.setProperty("--dx", dx);
      s.style.setProperty("--dy", dy);
      s.style.animation = "spark .65s ease-out forwards";
      rline.appendChild(s);
      setTimeout(()=>s.remove(), 800);
    }
  }

  function ripple(){
    // riavvia animazione cerchi energetici
    rings.forEach((ring, idx)=>{
      ring.style.animation = "none";
      ring.offsetHeight; // force reflow
      ring.style.opacity = "1";
      ring.style.animation = "ripple " + (0.8 + idx*0.15) + "s ease-out forwards";
    });
  }

  function glowOn(){
    card.classList.add("glow");
    ripple();
    spawnSparks();
  }

  function glowOff(){
    setTimeout(()=>card.classList.remove("glow"), 320);
  }

  btn.onclick = async function(ev){
    ev.preventDefault();
    btn.textContent = "… in ascolto";
    glowOn();

    try{
      const elemento = el.textContent || "RANDOM";
      const res = await fetch("/oracle?elemento=" + encodeURIComponent(elemento) + "&nonce=" + Date.now());
      const d = await res.json();

      el.textContent    = d.elemento;
      col.textContent   = d.colore || "";
      rName.textContent = d.runa;
      rSym.textContent  = d.runa_symbol;

      msgIt.textContent = d.messaggio_it; // IT sopra
      msgEn.textContent = d.messaggio_en; // EN sotto
      seed.textContent  = d.seed;

      speakItalian(d.messaggio_it); // ✅ audio solo IT
    }catch(err){
      console.error(err);
      msgIt.textContent = "Errore nel contattare l'oracolo. Riprova.";
      msgEn.textContent = "Error contacting the oracle. Please try again.";
    }finally{
      btn.textContent = "__CTA__";
      glowOff();
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
