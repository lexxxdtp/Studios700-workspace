"""
Studios 700 — Générateur de DEVIS (Bal de promo universitaire)
==============================================================
Public étudiant / budget accessible.
3 versions : V1 ESSENTIEL 150K / V2 STANDARD 250K / V3 COMPLET 400K
Réutilise la mise en page du générateur Coca-Cola.
Usage :  python3 devis_generator_balpromo.py
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from devis_generator_cocacola import _draw

OBJET = {
    "intitule": "Couverture photo & vidéo — Bal de promo (universitaire)",
    "date_presta": "À confirmer",
    "lieu": "À confirmer (Abidjan)",
    "client": {"nom": "Bal de promo — Université", "adresse": "Abidjan, Côte d'Ivoire"},
    "date_emission": "19 juin 2026",
    "valide": "19 juillet 2026",
    "delais": "Délais : photos retouchées sous 48–72h — récap vidéo & capsules sous 5–7 jours.",
}

VERSIONS = [
    {
        "numero": "DEV-2026-008",
        "tag": "V1_200K",
        "lignes": [
            {"titre": "Couverture photo — 1 photographe",
             "description": ["Tapis rouge + photos dans la salle + 60 photos retouchées"], "qte": 1, "prix": 100000},
            {"titre": "Couverture vidéo — 1 vidéaste",
             "description": ["Captation des temps forts pendant la soirée"], "qte": 1, "prix": 60000},
            {"titre": "Montage récap vidéo 60s",
             "description": ["1 vidéo souvenir rythmée de la soirée"], "qte": 1, "prix": 40000},
        ],
    },
    {
        "numero": "DEV-2026-008",
        "tag": "V2_300K",
        "lignes": [
            {"titre": "Couverture photo — 1 photographe",
             "description": ["Tapis rouge + photos dans la salle + ~100 photos retouchées"], "qte": 1, "prix": 130000},
            {"titre": "Couverture vidéo — 1 vidéaste",
             "description": ["Captation des temps forts pendant la soirée"], "qte": 1, "prix": 90000},
            {"titre": "Montage récap 60s soigné + 1 capsule réseaux",
             "description": ["Vidéo souvenir + 1 clip court pour les réseaux"], "qte": 1, "prix": 80000},
        ],
    },
    {
        "numero": "DEV-2026-008",
        "tag": "V3_400K",
        "lignes": [
            {"titre": "Couverture photo — 1 photographe",
             "description": ["Tapis rouge dédié + photos dans la salle + ~150 photos retouchées"], "qte": 1, "prix": 160000},
            {"titre": "Couverture vidéo — 1 vidéaste",
             "description": ["Captation complète des temps forts de la soirée"], "qte": 1, "prix": 120000},
            {"titre": "Montage récap 60s (pro) + 2 capsules réseaux",
             "description": ["Vidéo souvenir soignée + 2 clips courts pour les réseaux"], "qte": 1, "prix": 100000},
            {"titre": "Livraison express + logistique",
             "description": ["Traitement prioritaire et déplacement sur site"], "qte": 1, "prix": 20000},
        ],
    },
]

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    for v in VERSIONS:
        out = os.path.join(OUTPUT_DIR, f"DEVIS_BALPROMO_{v['tag']}.pdf")
        c = canvas.Canvas(out, pagesize=A4)
        _draw(c, v, OBJET)
        c.save()
        total = sum(l["qte"] * l["prix"] for l in v["lignes"])
        print(f"OK  {v['tag']:18s} total={total:>9,} XOF  ->  {os.path.basename(out)}")
