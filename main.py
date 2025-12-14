import random
import datetime as dt
from html import escape
from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

# -----------------------------
# BRAND / TESTI
# -----------------------------
TITLE = "RUNES & CIRCUITS"
SUBTITLE = "Rune Parlanti"
CTA_BUTTON_TEXT = "RICEVI LA DIVINAZIONE"

ELEMENTI = ["TERRA", "ACQUA", "ARIA", "FUOCO", "SPAZIO"]

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
    "SPAZIO": ["Acquario", "Pesci", "Sagittario"],  # puoi cambiare
}

# Rune per elemento (nomi + simboli Elder Futhark)
RUNE_PER_ELEMENTO = {
    "TERRA": ["Fehu", "Uruz", "Berkano", "Ingwaz", "Jera"],
    "ACQUA": ["Laguz", "Perthro", "Eihwaz", "Isa", "Ansuz"],
    "ARIA": ["Ansuz", "Raido", "Gebo", "Wunjo", "Ehwaz"],
    "FUOCO": ["Kenaz", "Sowilo", "Tiwaz", "Hagalaz", "Othila"],
    "SPAZIO": ["Algiz", "Dagaz", "Nauthiz", "Isa", "Eihwaz"],
}

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
    "Berkano": "ᛒ",
    "Ehwaz": "ᛖ",
    "Mannaz": "ᛗ",
    "Laguz": "ᛚ",
    "Ingwaz": "ᛜ",
    "Dagaz": "ᛞ",
    "Othila": "ᛟ",
}

# Messaggi bilingue per elemento
MESSAGGI = {
    "TERRA": [
        (
            "Metti ordine: ciò che è semplice diventa forte.",
            "Create order: what is simple becomes strong."
        ),
        (
            "Radicati. La forma si stabilizza quando smetti di inseguire.",
            "Root yourself. Form stabilizes when you stop chasing."
        ),
        (
            "Il passo lento è quello che arriva. Cura la base.",
            "The slow step is the one that arrives. Tend the foundation."
        ),
    ],
    "ACQUA": [
        (
            "Ascolta: il segno è già in movimento.",
            "Listen: the sign is already in motion."
        ),
        (
            "Lascia scorrere. Una risposta arriva senza sforzo.",
            "Let it flow. An answer arrives without force."
        ),
        (
            "Sii morbida con te: la marea cambia presto.",
            "Be gentle with yourself: the tide will shift soon."
        ),
    ],
    "ARIA": [
        (
            "Una nuova idea chiede spazio. Seguila.",
            "A new idea asks for space. Follow it."
        ),
        (
            "Parla chiaro: il vento porta alleati.",
            "Speak clearly: the wind brings allies."
        ),
        (
            "Alleggerisci il pensiero: vedrai l’uscita.",
            "Lighten the mind: the exit will appear."
        ),
    ],
    "FUOCO": [
        (
            "Accendi il coraggio: una scelta ti libera.",
            "Ignite courage: one choice sets you free."
        ),
        (
            "La scintilla guida. Muoviti: vivo, non perfetto.",
            "The spark leads. Move: alive, not perfect."
        ),
        (
            "Trasforma la paura in gesto: la strada si apre.",
            "Turn fear into action: the path opens."
        ),
    ],
    "SPAZIO": [
        (
            "Sospendi il giudizio: il vuoto è una porta.",
            "Suspend judgment: the void is a door."
        ),
        (
            "Tra due mondi c’è un varco. Restaci un istante.",
            "Between two worlds there is a passage. Stay there a moment."
        ),
        (
            "Il silenzio è codice: ascolta prima di agire.",
            "Silence is code: listen before you act."
        ),
    ],
}

# -----------------------------
# CORE ORACLE
# -----------------------------
def _seed_key(mode: str) -> str:
    now = dt.datetime.utcnow()
    if (mode or "").lower() == "minute":
        return now.strftime("%Y-%m-%d-%H%M")
    return now.strftime("%Y-%m-%d")

def _pick_elemento(elem: str) -> str:
    e = (elem or "").strip().upper()
    if e in ELEMENTI:
        return e
    return random.choice(ELEMENTI)

def _oracle_payload(elemento_in: str, mode: str):
    elemento = _pick_elemento(elemento_in)
    mode = (mode or "minute").lower()
    seed = _seed_key(mode)

    rng = random.Random(f"{TITLE}:{SUBTITLE}:{elemento}:{seed}")

    runa_name = rng.choice(RUNE_PER_ELEMENTO[elemento])
    runa_symbol = RUNE_SYMBOL.get(runa_name, "ᚱ")
    msg_it, msg_en = rng.choice(MESSAGGI[elemento])

    return {
        "progetto": TITLE,
        "sottotitolo": SUBTITLE,
        "elemento": elemento,
        "colore": COLORI[elemento],
        "runa": runa_name,
        "runa_symbol": runa_symbol,
        "messaggio_it": msg_it,
        "messaggio_en": msg_en,
        "segni": SEGNI_PER_ELEMENTO[elemento],
        "seed": seed,
        "mode": mode,
        "cta": "Ricarica per un nuovo segno (mode=minute) oppure usa mode=day per coerenza giornaliera.",
        "ts_utc": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }

# -----------------------------
# ROUTES
# -----------------------------
@app.get("/")
def home():
    return view()

@app.get("/oracle")
def oracle():
    elemento_in = request.args.get("elemento", "RANDOM")
    mode = request.args.get("mode", "minute")
    data = _oracle_payload(elemento_in, mode)

    resp = jsonify(data)
    resp.headers["Cache-Control"] = "no-store"
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp

@app.get("/view")
def view():
    elemento_in = request.args.get("elemento", "RANDOM")
    mode = request.args.get("mode", "minute")
    data = _oracle_payload(elemento_in, mode)

    def esc(x): return escape(str(x)) if x is not None else "—"

    def pill(label, elemento_value):
        href = f"/view?elemento={elemento_value}&mode={esc(data['mode'])}"
        active = (data["elemento"] == elemento_value)
        style = (
            "text-decoration:none;display:inline-flex;align-items:center;gap:10px;"
            "padding:12px 18px;border-radius:999px;font-weight:850;font-size:14px;"
            "letter-spacing:.02em;color:#eef2ff;background:rgba(255,255,255,.06);"
            "border:1px solid rgba(255,255,255,.14);"
            "box-shadow:0 0 0 1px rgba(255,215,140,.10) inset, 0 0 18px rgba(120,90,255,.10);"
        )
        if active:
            style += (
                "background:rgba(255,255,255,.09);border:1px solid rgba(255,215,140,.36);"
                "box-shadow:0 0 0 1px rgba(255,215,140,.18) inset, 0 0 26px rgba(255,215,140,.12), 0 0 28px rgba(120,90,255,.12);"
            )
        return f'<a href="{href}" style="{style}">{label}</a>'

    # CTA: “Ricevi la divinazione” -> ricarica minute sullo stesso elemento
    cta_href = f"/view?elemento={esc(data['elemento'])}&mode=minute"
    cta_style = (
        "text-decoration:none;display:inline-block;padding:16px 22px;border-radius:999px;"
        "font-weight:950;font-size:14px;letter-spacing:.08em;color:#2a1a00;"
        "background:linear-gradient(135deg,#ffd36b,#ffb347);"
        "box-shadow:0 0 0 2px rgba(255,215,140,.55) inset,0 0 28px rgba(255,190,80,.35),0 0 78px rgba(255,215,140,.24);"
    )

    ghost_style = (
        "text-decoration:none;display:inline-block;padding:14px 18px;border-radius:999px;"
        "font-weight:850;font-size:14px;letter-spacing:.06em;color:#eef2ff;opacity:.92;"
        "border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.06);"
        "box-shadow:0 0 0 1px rgba(255,215,140,.10) inset;"
    )

    json_href = f"/oracle?elemento={esc(data['elemento'])}&mode={esc(data['mode'])}"

    # Rune symbol glow style
    rune_symbol_span = f"""
      <span style="
        display:inline-flex;align-items:center;justify-content:center;
        width:40px;height:40px;border-radius:999px;
        background:rgba(255,255,255,.06);
        border:1px solid rgba(255,215,140,.22);
        box-shadow:
          0 0 0 1px rgba(255,215,140,.12) inset,
          0 0 26px rgba(255,215,140,.14),
          0 0 38px rgba(120,90,255,.12);
        font-size:22px;font-weight:900; line-height:1;
        text-shadow:0 0 14px rgba(255,215,140,.30), 0 0 18px rgba(120,90,255,.24);
      ">{esc(data["runa_symbol"])}</span>
    """

    html = f"""<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>{esc(TITLE)} — {esc(SUBTITLE)}</title>
</head>
<body style="margin:0;min-height:100vh;color:#eef2ff;font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
  background:
    radial-gradient(circle at 8% 0%, rgba(170,140,255,.55) 0%, rgba(60,40,140,.10) 35%, rgba(2,3,8,1) 70%),
    radial-gradient(circle at 92% 18%, rgba(120,90,255,.28) 0%, rgba(2,3,8,0) 48%),
    radial-gradient(circle at 50% 100%, rgba(255,215,140,.12) 0%, rgba(2,3,8,0) 52%),
    linear-gradient(180deg, rgba(2,3,8,1) 0%, rgba(2,3,8,1) 100%);
  overflow-x:hidden;">

  <div style="max-width:980px;margin:0 auto;padding:44px 16px 54px;">
    <div style="text-align:center;letter-spacing:.28em;font-size:11px;opacity:.75;">{esc(TITLE)}</div>

    <div style="margin-top:12px;text-align:center;">
      <div style="font-size:44px;font-weight:950;line-height:1.05;
        text-shadow:0 0 22px rgba(120,90,255,.28),0 0 14px rgba(255,215,140,.20);">
        ✨ {esc(SUBTITLE)}
      </div>
      <div style="margin-top:10px;opacity:.84;font-size:15px;">
        Messaggio del momento • modalità: <b>{esc(data["mode"])}</b>
      </div>
    </div>

    <div style="display:flex;justify-content:center;gap:12px;flex-wrap:wrap;margin:22px 0 18px;">
      {pill("🌕 Terra", "TERRA")}
      {pill("🌊 Acqua", "ACQUA")}
      {pill("💨 Aria", "ARIA")}
      {pill("🔥 Fuoco", "FUOCO")}
      {pill("🟦 Spazio", "SPAZIO")}
      {pill("✨ Random", "RANDOM")}
    </div>

    <div style="margin:0 auto;max-width:920px;background:rgba(8,10,22,.44);
      border-radius:30px;border:1px solid rgba(255,255,255,.12);
      box-shadow:0 26px 90px rgba(0,0,0,.62),0 0 0 1px rgba(255,215,140,.10) inset,0 0 55px rgba(120,90,255,.10);
      backdrop-filter:blur(10px);overflow:hidden;">

      <div style="padding:22px 22px 16px;border-bottom:1px solid rgba(255,255,255,.08);">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:14px;flex-wrap:wrap;">
          <div>
            <div style="font-size:28px;font-weight:950;">
              Elemento: <span style="color:#ffd78a;text-shadow:0 0 12px rgba(255,215,140,.18);">{esc(data["elemento"])}</span>
            </div>
            <div style="margin-top:10px;opacity:.86;font-size:14px;">
              Colore: <b>{esc(data["colore"])}</b> • Segni: <b>{esc(", ".join(data["segni"]))}</b>
            </div>
          </div>

          <a href="{json_href}" target="_blank" rel="noopener"
             style="text-decoration:none;color:#eef2ff;opacity:.88;font-size:13px;padding:12px 16px;border-radius:999px;
             border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.06);">
             Apri JSON
          </a>
        </div>
      </div>

      <div style="padding:22px;">
        <div style="display:grid;grid-template-columns:1fr 1.4fr;gap:22px;">
          <div style="min-width:0;">
            <div style="opacity:.72;font-size:12px;letter-spacing:.18em;">RUNA</div>

            <div style="margin-top:12px;display:flex;align-items:center;gap:12px;flex-wrap:wrap;">
              {rune_symbol_span}
              <div style="font-size:40px;font-weight:950;
                text-shadow:0 0 22px rgba(120,90,255,.25),0 0 12px rgba(255,215,140,.18);">
                {esc(data["runa"])}
              </div>
            </div>

            <div style="margin-top:10px;opacity:.62;font-size:12px;">
              seed: {esc(data["seed"])} • {esc(data["ts_utc"])}
            </div>
          </div>

          <div style="min-width:0;">
            <div style="opacity:.72;font-size:12px;letter-spacing:.18em;">MESSAGGIO</div>

            <div style="margin-top:12px;padding:16px 16px;border-radius:18px;
              border:1px solid rgba(120,90,255,.26);background:rgba(0,0,0,.18);
              box-shadow:0 0 0 1px rgba(255,215,140,.08) inset, 0 0 34px rgba(120,90,255,.10);">

              <div style="opacity:.75;font-size:12px;letter-spacing:.14em;margin-bottom:8px;">🇮🇹 ITALIANO</div>
              <div style="font-size:16px;line-height:1.6;opacity:.98;">{esc(data["messaggio_it"])}</div>

              <div style="height:14px;"></div>

              <div style="opacity:.75;font-size:12px;letter-spacing:.14em;margin-bottom:8px;">🇬🇧 ENGLISH</div>
              <div style="font-size:16px;line-height:1.6;opacity:.95;">{esc(data["messaggio_en"])}</div>
            </div>

            <div style="margin-top:18px;display:flex;gap:12px;flex-wrap:wrap;">
              <a href="{cta_href}" style="{cta_style}">{esc(CTA_BUTTON_TEXT)}</a>
              <a href="/view?elemento={esc(data["elemento"])}&mode=day" style="{ghost_style}">Coerenza (day)</a>
            </div>

            <div style="margin-top:12px;opacity:.65;font-size:12px;">
              Ricarica per un nuovo segno (mode=minute) oppure usa mode=day per coerenza giornaliera.
            </div>
          </div>
        </div>
      </div>

    </div>

    <div style="text-align:center;margin-top:18px;font-size:12px;opacity:.62;">
      {esc(TITLE)} — arcano + futuro • Tina Örn vibes ✨
    </div>
  </div>
</body>
</html>"""

    resp = make_response(html)
    resp.headers["Content-Type"] = "text/html; charset=utf-8"
    resp.headers["Cache-Control"] = "no-store"
    return resp
