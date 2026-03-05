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
    "TERRA": ["Toro", "Vergine", "Capricorno" "Cancro", "Scorpione", "Pesci" "Ariete", "Leone", "Sagittario" "Acquario", "Pesci", "Sagittario"],
}

# =========================
# RUNE + SIMBOLI
# =========================
RUNE_PER_ELEMENTO = {
    "TERRA": ,
    "ACQUA": ["Laguz", "Perthro", "Eihwaz", "Isa" "Ansuz", "Raido", "Gebo", "Wunjo" "Kenaz", "Sowilo", "Tiwaz", "Hagalaz" "Algiz", "Dagaz", "Nauthiz", "Othila"],
}

RUNE_SYMBOL = {
    "Fehu":"ᚠ","Uruz":"ᚢ","Ansuz":"ᚨ","Raido":"ᚱ","Kenaz":"ᚲ","Gebo":"ᚷ",
    "Wunjo":"ᚹ","Hagalaz":"ᚺ","Nauthiz":"ᚾ","Isa":"ᛁ","Jera":"ᛃ",
    "Eihwaz":"ᛇ","Perthro":"ᛈ","Algiz":"ᛉ","Sowilo":"ᛋ","Tiwaz":"ᛏ",
    "Berkano":"ᛒ","Laguz":"ᛚ","Dagaz":"ᛞ","Othila":"ᛟ"
}

# =========================
# MESSAGGI VARIABILI PER OGNI RUNA (cambiano ogni giorno!)
# =========================
RUNE_VARIANTS_IT = {
    "Fehu": [
        "Ciò che possiedi cresce se lo condividi con consapevolezza.",
        "La vera ricchezza è invisibile: inizia dal cuore.",
        "Un gesto generoso oggi, un raccolto domani.",
        "Non trattenere: l'abbondanza ama il flusso.",
        "La moneta che dai torna triplicata, fidati.",
        "Oggi la tua energia attira ciò che meriti.",
        "Smetti di contare: l'universo già sa.",
        "Un sorriso condiviso vale più di mille lingotti.",
        "La porta della prosperità si apre con gratitudine.",
        "Oggi semina fiducia: il raccolto è vicino." "La forza è già in te: usala senza forzarla.",
        "Respira. Il tuo corpo sa più di quanto pensi.",
        "Oggi un passo deciso basta a spostare montagne.",
        "Non spingere: lascia che la vitalità scorra.",
        "La tua radice è solida, ora spingi in alto.",
        "Un urlo silenzioso dentro: è il tuo potere.",
        "Oggi la bestia interiore si sveglia gentile.",
        "Forza non è muscoli: è presenza totale.",
        "Lascia andare la stanchezza, lei se ne va da sola.",
        "Il tuo istinto è la bussola migliore." "Proteggi ciò che nasce, anche se è fragile.",
        "Un germoglio ha bisogno di te: coprilo.",
        "Oggi custodisci il tuo sogno, non farlo vedere.",
        "La crescita lenta è la più forte.",
        "Accogli il nuovo senza fretta.",
        "Un abbraccio al tuo futuro basta.",
        "Protezione non è mura: è attenzione.",
        "Lascia che fiorisca nel tuo silenzio.",
        "Oggi il fragile diventa forte grazie a te.",
        "Il seme che curi oggi ti salverà domani." "Ogni cosa arriva nel tempo giusto. Abbi fiducia.",
        "Il ciclo gira: aspetta il tuo turno.",
        "Oggi raccogli ciò che hai seminato ieri.",
        "Pazienza non è attesa: è preparazione.",
        "La ruota gira lenta, ma gira.",
        "Fidati: il raccolto è già in arrivo.",
        "Oggi il tempo lavora per te.",
        "Un anno di silenzio, un giorno di luce.",
        "Non forzare: la stagione sa.",
        "Il tuo momento è vicino, respira."
    ],
    "Laguz": [
        "Lascia scorrere. La risposta arriva senza sforzo.",
        "Oggi l'acqua lava via il peso.",
        "Non combattere la corrente: vai con lei.",
        "Il tuo cuore sa già dove andare.",
        "Fluisci come un fiume: arriva al mare.",
        "Le emozioni si muovono: seguile.",
        "Oggi ascolta il suono del tuo respiro.",
        "Lascia che tutto si sistemi da solo.",
        "L'intuizione è la tua corrente.",
        "Non afferrare: l'onda ti porta."         "Il mistero non va risolto: va attraversato.",
        "Oggi il destino gioca a carte coperte.",
        "Accetta l'ignoto: è il tuo alleato.",
        "La runa nasconde, ma non mente.",
        "Un velo si alza piano, guarda.",
        "Il segreto è dentro di te.",
        "Oggi cammina nel buio con fiducia.",
        "Non chiedere: vivi la sorpresa.",
        "Il caso è solo un messaggio.",
        "Lascia che il mistero ti guidi." "Rimani nel passaggio: la trasformazione è in atto.",
        "Oggi sei tra due mondi: resta fermo.",
        "Il ponte è fragile, ma regge.",
        "Cambiamento non è fine: è mezzo.",
        "Respira nel vuoto: lì nasce il nuovo.",
        "La tua forma vecchia si scioglie.",
        "Oggi il tronco si piega, non spezza.",
        "Il passaggio è sacro: onorarlo.",
        "Trasformati senza paura.",
        "La fine è solo un altro inizio." "Fermati. Nel silenzio trovi chiarezza.",
        "Oggi il gelo ti protegge.",
        "Non muoverti: ascolta il vuoto.",
        "La pausa è potere.",
        "Il ghiaccio riflette la verità.",
        "Respira. Tutto è sospeso.",
        "Oggi il mondo aspetta te.",
        "Silenzio non è assenza: è spazio.",
        "Lascia che il freddo ti pulisca.",
        "La chiarezza arriva quando smetti." "Ascolta il messaggio: sta già parlando.",
        "Oggi la parola arriva dal vento.",
        "La tua bocca sa cosa dire.",
        "Un respiro e la verità esce.",
        "Il divino sussurra: tendi l'orecchio.",
        "Oggi ascolta più che parlare.",
        "La voce interiore è alta.",
        "Il segno è nella tua lingua.",
        "Non inventare: ricevi.",
        "La saggezza è già qui." "Il viaggio è iniziato: muoviti con intenzione.",
        "Oggi un passo cambia tutto.",
        "La strada è tua: scegli.",
        "Non correre: cammina consapevole.",
        "Il movimento è preghiera.",
        "Oggi il sentiero ti chiama.",
        "Porta con te solo ciò che serve.",
        "Ogni metro è una lezione.",
        "La destinazione è dentro.",
        "Vai: il mondo ti aspetta." "Dare e ricevere sono lo stesso gesto.",
        "Oggi un regalo torna indietro.",
        "L'equilibrio è nel tuo cuore.",
        "Non contare: scambia.",
        "La connessione è reciproca.",
        "Un sì oggi, un sì domani.",
        "Il dono è la tua forza.",
        "Lascia che il cerchio si chiuda.",
        "Oggi offri, e ricevi in silenzio.",
        "Il legame è già lì: rafforzalo." "La gioia arriva quando smetti di cercarla.",
        "Oggi il sorriso è già dentro.",
        "Sii felice senza motivo.",
        "La luce è tua, accoglila.",
        "La gioia non si insegue: si respira.",
        "Un momento basta.",
        "Oggi tutto è perfetto così.",
        "Ridi: l'universo ride con te.",
        "La felicità è un atto semplice.",
        "Lascia entrare il calore." "Una scintilla illumina ciò che era nascosto.",
        "Oggi vedi chiaro.",
        "Il fuoco interiore si accende.",
        "La torcia è nella tua mano.",
        "Non temere l'ombra: accendila.",
        "La conoscenza brucia leggera.",
        "Oggi un'idea cambia tutto.",
        "Illumina senza bruciare.",
        "La rivelazione è qui.",
        "Guarda: tutto è visibile ora." "La luce è dalla tua parte. Avanza.",
        "Oggi il sole ti segue.",
        "Non nasconderti: splendi.",
        "La vittoria è già tua.",
        "Il giorno è lungo: usalo.",
        "La tua ombra si ritira.",
        "Avanti, la luce guida.",
        "Oggi tutto è possibile.",
        "Il calore ti sostiene.",
        "Brilla: il mondo ti vede."         "Accendi il coraggio: una scelta ti libera.",
        "Oggi decidi e vola.",
        "La spada è la tua volontà.",
        "Non dubitare: agisci.",
        "Il giusto è già dentro.",
        "Una scelta, una vita nuova.",
        "Il coraggio non aspetta.",
        "Sii la tua legge.",
        "La giustizia è il tuo scudo.",
        "Oggi scegli con forza." "Il cambiamento rompe ciò che non serve più.",
        "Oggi il vecchio crolla.",
        "La grandine pulisce.",
        "Lascia che cada: rinasci.",
        "Il caos è ordine nascosto.",
        "Non resistere: trasforma.",
        "La rottura è liberazione.",
        "Oggi il mondo si resetta.",
        "Il vento forte porta novità.",
        "Accogli la tempesta." "Sei protetta mentre resti fedele a te.",
        "Oggi il tuo scudo è vivo.",
        "Non temere: sei guardata.",
        "La protezione è dentro.",
        "Resta vera: niente ti tocca.",
        "Il corno ti copre.",
        "Fidati del tuo confine.",
        "Sei al sicuro ora.",
        "La guardia è sempre attiva.",
        "Il tuo centro è inviolabile." "Una nuova visione si apre ora.",
        "Oggi l'alba è dentro.",
        "Il buio finisce.",
        "Vedi oltre.",
        "La luce cambia tutto.",
        "Un clic: nuovo giorno.",
        "La prospettiva si ribalta.",
        "Oggi rinasci.",
        "Il giorno nuovo ti chiama.",
        "Guarda con occhi freschi." "La necessità rivela la via.",
        "Oggi il bisogno ti guida.",
        "Non c'è scelta: c'è destino.",
        "Il fuoco della fame illumina.",
        "Sopravvivi: cresci.",
        "La mancanza è maestra.",
        "Oggi ciò che manca ti salva.",
        "La via è stretta, ma vera.",
        "Il limite è la tua forza.",
        "Accetta: e troverai." "Riconosci ciò che ti appartiene davvero.",
        "Oggi la casa è dentro.",
        "Il tuo sangue parla.",
        "Torna alla radice.",
        "Ciò che è tuo non si perde.",
        "La famiglia è eredità viva.",
        "Accogli il tuo posto.",
        "Oggi sei a casa.",
        "L'eredità è il tuo potere.",
        "Ritrova il tuo centro."
    ]
}

# =========================
# ORACOLO
# =========================
def genera_oracolo(elemento):
    elemento = elemento if elemento in ELEMENTI else random.choice(ELEMENTI)

    # Seed legato alla DATA: cambia ogni giorno!
    oggi = dt.date.today().isoformat()
    seed = f"runa-{elemento}-{oggi}"
    rng = random.Random(seed)

    runa = rng.choice(RUNE_PER_ELEMENTO )
    simbolo = RUNE_SYMBOL.get(runa, "ᚱ")

    # Scegli una variante diversa ogni giorno
    varianti = RUNE_VARIANTS_IT.get(runa, ["Messaggio base per oggi."])
    msg_it = rng.choice(varianti)

    # Inglese: versione semplice (puoi migliorare dopo)
    msg_en = f"Today: {msg_it.lower().replace('oggi', 'today').replace('la', 'the').replace('il', 'the')}"

    return {
        "elemento": elemento,
        "colore": COLORI ,
        "segni": SEGNI ,
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

<h2>Elemento: {e(data )}</h2>

<div style="display:flex;align-items:center;gap:14px;">
  <div id="runa-symbol" style="font-size:42px;">{e(data )}</div>
  <div id="runa-name" style="font-size:36px;font-weight:bold;">
    {e(data["runa"])}
  </div>
</div>

<div id="msg-it" style="margin-top:16px;font-size:20px;">
  {e(data )}
</div>

<div id="msg-en" style="opacity:.7;margin-top:6px;">
  {e(data )}
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
    const res = await fetch("/oracle?elemento={e(data )}&nonce="+Date.now());
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
