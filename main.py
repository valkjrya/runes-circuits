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
        "La scintil
