"""
Studios 700 — DEVIS Conférence Golden Impact (vidéo récap)
==========================================================
Équipe : 2 vidéastes (Alex + Steven). Location 70-200 + 2 casques intercom.
Usage :  python3 devis_generator_goldenimpact.py
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from devis_generator_cocacola import _draw

OBJET = {
    "intitule": "Couverture vidéo & montage récap — Conférence Golden Impact",
    "date_presta": "À confirmer",
    "lieu": "À confirmer (Abidjan)",
    "client": {"nom": "Conférence Golden Impact", "adresse": "Abidjan, Côte d'Ivoire"},
    "date_emission": "19 juin 2026",
    "valide": "19 juillet 2026",
    "delais": "Délais : montage récap livré sous 5–7 jours après la conférence.",
}

VERSIONS = [
    {
        "numero": "DEV-2026-009",
        "tag": "300K",
        "lignes": [
            {"titre": "Captation vidéo — 2 vidéastes (journée)",
             "description": ["2 caméras : intervenants, public, temps forts de la conférence"], "qte": 1, "prix": 180000},
            {"titre": "Montage récap vidéo (60–90s)",
             "description": ["Montage rythmé, étalonnage et sound design"], "qte": 1, "prix": 70000},
            {"titre": "Location objectif 70-200mm f/2.8",
             "description": ["Objectif longue focale pour la scène et les plans serrés"], "qte": 1, "prix": 25000},
            {"titre": "Location 2 casques intercom",
             "description": ["Communication équipe en direct pendant la captation"], "qte": 1, "prix": 25000},
        ],
    },
]

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    for v in VERSIONS:
        out = os.path.join(OUTPUT_DIR, f"DEVIS_GOLDENIMPACT_{v['tag']}.pdf")
        c = canvas.Canvas(out, pagesize=A4)
        _draw(c, v, OBJET)
        c.save()
        total = sum(l["qte"] * l["prix"] for l in v["lignes"])
        print(f"OK  {v['tag']:8s} total={total:>9,} XOF  ->  {os.path.basename(out)}")
