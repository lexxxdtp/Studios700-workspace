"""
Studios 700 — Générateur de DEVIS (Coca-Cola Fest Abidjan)
==========================================================
Identité visuelle : Noir & Blanc | Logo officiel studios700.
Produit 3 versions versionnées : V1 800K / V2 1.2M / V3 1.65M
Usage :  python3 devis_generator_cocacola.py
"""

from PIL import Image, ImageFile, ImageOps
ImageFile.LOAD_TRUNCATED_IMAGES = True
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
import io, os

# ─────────────────────────────────────────────────────────────────
#  OBJET COMMUN
# ─────────────────────────────────────────────────────────────────
OBJET = {
    "intitule": "Couverture photo & vidéo — Coca-Cola Fest Abidjan",
    "date_presta": "20 juin 2026 (à partir de 14h00)",
    "lieu": "Palais de la Culture, Abidjan",
    "client": {"nom": "Coca-Cola Fest Abidjan", "adresse": "Abidjan, Côte d'Ivoire"},
    "date_emission": "19 juin 2026",
    "valide": "19 juillet 2026",
}

# ─────────────────────────────────────────────────────────────────
#  LES 3 VERSIONS
# ─────────────────────────────────────────────────────────────────
VERSIONS = [
    {
        "numero": "DEV-2026-007",
        "tag": "V1_800K",
        "lignes": [
            {"titre": "Captation vidéo — équipe vidéastes (journée)",
             "description": ["Tournage complet : artiste, scène, public, activations"], "qte": 1, "prix": 300000},
            {"titre": "Couverture photo — 2 photographes (journée)",
             "description": ["Photos artiste, public, ambiance & activations"], "qte": 1, "prix": 200000},
            {"titre": "Montage & post-production",
             "description": ["Récap final 60s + Récap 30s + 2 à 3 capsules 10s"], "qte": 1, "prix": 200000},
            {"titre": "Location objectif 70-200mm + logistique équipe",
             "description": ["Location matériel + transport/restauration équipe"], "qte": 1, "prix": 100000},
        ],
    },
    {
        "numero": "DEV-2026-007",
        "tag": "V2_1200K",
        "lignes": [
            {"titre": "Captation vidéo — équipe vidéastes (journée)",
             "description": ["Tournage multi-cadreurs : artiste, scène, public"], "qte": 1, "prix": 350000},
            {"titre": "Couverture photo — 2 photographes (journée)",
             "description": ["Photos artiste, public, ambiance & activations"], "qte": 1, "prix": 200000},
            {"titre": "Montage Récap final 60s (montage pro)",
             "description": ["Montage rythmé, étalonnage, sound design"], "qte": 1, "prix": 180000},
            {"titre": "Montage Récap 30s (format réseaux)",
             "description": ["Version courte verticale pour réseaux sociaux"], "qte": 1, "prix": 90000},
            {"titre": "2 à 3 capsules 10s livrées le jour J",
             "description": ["Teasers express à poster en live pendant l'événement"], "qte": 1, "prix": 120000},
            {"titre": "Retouche & livraison photos",
             "description": ["Tri, retouche et livraison via Google Drive"], "qte": 1, "prix": 60000},
            {"titre": "Direction artistique, coordination & backups",
             "description": ["Supervision plateau, gestion fichiers & sauvegardes"], "qte": 1, "prix": 110000},
            {"titre": "Location 70-200mm + logistique équipe",
             "description": ["Location matériel + transport/restauration équipe"], "qte": 1, "prix": 90000},
        ],
    },
    {
        "numero": "DEV-2026-007",
        "tag": "V3_1650K",
        "lignes": [
            {"titre": "Captation vidéo — équipe vidéastes (journée)",
             "description": ["Tournage multi-cadreurs : artiste, scène, public, activations"], "qte": 1, "prix": 400000},
            {"titre": "Couverture photo — 2 photographes (journée)",
             "description": ["Photos artiste, public, ambiance & activations"], "qte": 1, "prix": 250000},
            {"titre": "Montage Récap final 60s (pro VFX/SFX + étalonnage)",
             "description": ["Montage haut de gamme, effets, sound design cinématique"], "qte": 1, "prix": 230000},
            {"titre": "Montage Récap 30s (format réseaux)",
             "description": ["Version courte verticale optimisée réseaux"], "qte": 1, "prix": 120000},
            {"titre": "3 capsules 10s livrées en LIVE le jour J",
             "description": ["Teasers express postés pendant l'événement"], "qte": 1, "prix": 180000},
            {"titre": "Retouche pro & livraison (~180 photos)",
             "description": ["Tri, retouche pro et livraison via Google Drive"], "qte": 1, "prix": 100000},
            {"titre": "Direction artistique & supervision plateau",
             "description": ["Cadrage créatif et coordination de l'équipe (5 pers.)"], "qte": 1, "prix": 120000},
            {"titre": "Location matériel (70-200mm, trépieds, audio)",
             "description": ["Objectif, supports et captation audio"], "qte": 1, "prix": 90000},
            {"titre": "Gestion fichiers, backups sécurisés & disque dur",
             "description": ["Transferts, sauvegardes et disque dur fourni"], "qte": 1, "prix": 70000},
            {"titre": "Logistique & restauration équipe (5 pers.)",
             "description": ["Transport et restauration de l'équipe"], "qte": 1, "prix": 90000},
        ],
    },
]

LIVRABLES = [
    ("Capsules 10s (jour J)", "MP4 vertical", "Le jour même"),
    ("Récap 30s (réseaux)", "MP4 HD/4K", "48h"),
    ("Récap final 60s", "MP4 4K", "5–7 jours"),
    ("Photos retouchées", "JPG HD", "48–72h"),
]

LOGO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
            "../00_IDENTITE_MARQUE/logos/studios700_logo_noir.png")
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

C_BLACK = colors.HexColor("#111111"); C_DARK = colors.HexColor("#222222")
C_MID = colors.HexColor("#555555"); C_LIGHT = colors.HexColor("#f4f4f4")
C_BORDER = colors.HexColor("#cccccc"); C_WHITE = colors.white
W, H = A4
ML = 20*mm; MR = 20*mm


def fmt_xof(n):
    return f"{n:,.0f}".replace(",", " ") + " XOF"


def load_logo_white(path):
    img = Image.open(path).convert("RGBA")
    r, g, b, a = img.split()
    white = Image.merge("RGBA", (ImageOps.invert(r), ImageOps.invert(g), ImageOps.invert(b), a))
    buf = io.BytesIO(); white.save(buf, format="PNG"); buf.seek(0)
    return ImageReader(buf)


def _draw(c, v, objet=OBJET):
    OBJET = objet
    # 1. HEADER
    hh = 42*mm
    c.setFillColor(C_BLACK); c.rect(0, H - hh, W, hh, fill=1, stroke=0)
    logo_img = load_logo_white(LOGO_PATH)
    logo_w = 58*mm; logo_h = logo_w * (256/882)
    c.drawImage(logo_img, ML, H - hh/2 - logo_h/2, width=logo_w, height=logo_h, mask='auto')
    c.setFont("Helvetica", 6.5); c.setFillColor(colors.HexColor("#999999"))
    c.drawRightString(W - MR, H - 10*mm, "VOTRE IMAGE, EN MIEUX")
    for i, line in enumerate(["team@studios700.com", "+225 07 77 22 52 77", "studios700.com"]):
        c.setFont("Helvetica-Bold" if i == 0 else "Helvetica", 7.5); c.setFillColor(C_WHITE)
        c.drawRightString(W - MR, H - 15*mm - i*5*mm, line)

    # 2. TITRE
    y = H - hh - 12*mm
    c.setFont("Helvetica-Bold", 28); c.setFillColor(C_BLACK); c.drawString(ML, y, "DEVIS")
    y2 = y - 8*mm
    c.setFont("Helvetica-Bold", 9); c.setFillColor(C_DARK)
    c.drawString(ML, y2, f"N° :  {v['numero']}")
    c.drawRightString(W - MR, y2, f"Date : {OBJET['date_emission']}")
    c.setFont("Helvetica", 7.5); c.setFillColor(C_MID)
    c.drawRightString(W - MR, y2 - 4*mm, f"Valable jusqu'au {OBJET['valide']}")
    c.setStrokeColor(C_BLACK); c.setLineWidth(1)
    c.line(ML, y2 - 6*mm, W - MR, y2 - 6*mm)

    # 3. DE / POUR
    y3 = y2 - 9*mm; bh = 28*mm
    c.setFillColor(C_LIGHT); c.roundRect(ML, y3 - bh, W - ML - MR, bh, 3, fill=1, stroke=0)
    lx = ML + 5*mm; rx = W/2 + 5*mm; ty = y3 - 5*mm
    c.setFont("Helvetica-Bold", 8); c.setFillColor(C_DARK); c.drawString(lx, ty, "DE :")
    c.setFont("Helvetica-Bold", 9.5); c.drawString(lx, ty - 5.5*mm, "Studios 700")
    c.setFont("Helvetica", 8.5); c.setFillColor(C_MID)
    for i, t in enumerate(["Alex Vianney Koffi", "Abidjan, Côte d'Ivoire",
                            "team@studios700.com", "+225 07 77 22 52 77"]):
        c.drawString(lx, ty - 10.5*mm - i*4*mm, t)
    c.setFont("Helvetica-Bold", 8); c.setFillColor(C_DARK); c.drawString(rx, ty, "POUR :")
    c.setFont("Helvetica-Bold", 9.5); c.drawString(rx, ty - 5.5*mm, OBJET["client"]["nom"])
    c.setFont("Helvetica", 8.5); c.setFillColor(C_MID)
    c.drawString(rx, ty - 11*mm, OBJET["client"]["adresse"])

    # 3b. OBJET
    yo = y3 - bh - 6*mm
    c.setFont("Helvetica-Bold", 8); c.setFillColor(C_BLACK); c.drawString(ML, yo, "OBJET :")
    c.setFont("Helvetica", 8.5); c.setFillColor(C_DARK)
    c.drawString(ML + 16*mm, yo, OBJET["intitule"])
    c.setFont("Helvetica", 8); c.setFillColor(C_MID)
    c.drawString(ML, yo - 5*mm, f"Date : {OBJET['date_presta']}    |    Lieu : {OBJET['lieu']}")

    # 4. TABLEAU
    y4 = yo - 8*mm
    col_w = [W - ML - MR - 55*mm, 14*mm, 27*mm, 24*mm]
    th = 9*mm
    c.setFillColor(C_BLACK); c.rect(ML, y4 - th, sum(col_w), th, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 8); c.setFillColor(C_WHITE)
    xp = ML
    for i, (hdr, cw) in enumerate(zip(["DÉSIGNATION", "QTÉ", "PRIX UNIT.", "TOTAL"], col_w)):
        cy = y4 - th + 3.2*mm
        c.drawString(xp + 3*mm, cy, hdr) if i == 0 else c.drawCentredString(xp + cw/2, cy, hdr)
        xp += cw
    row_y = y4 - th
    for ligne in v["lignes"]:
        rh = max(10*mm, (len(ligne["description"]) + 1) * 5*mm)
        c.setFillColor(C_WHITE); c.rect(ML, row_y - rh, sum(col_w), rh, fill=1, stroke=0)
        c.setStrokeColor(C_BORDER); c.setLineWidth(0.4)
        c.rect(ML, row_y - rh, sum(col_w), rh, fill=0, stroke=1)
        xd = ML + col_w[0]
        for cw in col_w[1:]:
            c.line(xd, row_y, xd, row_y - rh); xd += cw
        c.setFont("Helvetica-Bold", 8.5); c.setFillColor(C_DARK)
        c.drawString(ML + 3*mm, row_y - 4.5*mm, ligne["titre"])
        c.setFont("Helvetica", 7.5); c.setFillColor(C_MID)
        for j, dl in enumerate(ligne["description"]):
            c.drawString(ML + 3*mm, row_y - 8.5*mm - j*4*mm, dl)
        mid_y = row_y - rh/2 + 1*mm
        c.setFont("Helvetica", 8.5); c.setFillColor(C_DARK)
        c.drawCentredString(ML + col_w[0] + col_w[1]/2, mid_y, str(ligne["qte"]))
        c.drawCentredString(ML + col_w[0] + col_w[1] + col_w[2]/2, mid_y, fmt_xof(ligne["prix"]))
        c.setFont("Helvetica-Bold", 8.5)
        c.drawCentredString(ML + col_w[0] + col_w[1] + col_w[2] + col_w[3]/2, mid_y,
                            fmt_xof(ligne["qte"] * ligne["prix"]))
        row_y -= rh

    # 5. TOTAL
    total = sum(l["qte"] * l["prix"] for l in v["lignes"])
    y5 = row_y - 5*mm
    re = W - MR; lbl = re - 72*mm
    c.setFont("Helvetica", 8.5); c.setFillColor(C_MID)
    c.drawString(lbl, y5, "SOUS-TOTAL"); c.drawRightString(re, y5, fmt_xof(total))
    c.drawString(lbl, y5 - 7*mm, "TAXES / TVA"); c.drawRightString(re, y5 - 7*mm, "—")
    c.setStrokeColor(C_BORDER); c.setLineWidth(0.4); c.line(lbl - 3*mm, y5 - 11*mm, re, y5 - 11*mm)
    y_box = y5 - 11*mm - 11*mm
    c.setFillColor(C_BLACK); c.rect(lbl - 3*mm, y_box, re - lbl + 3*mm, 11*mm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 10); c.setFillColor(C_WHITE)
    c.drawString(lbl, y_box + 3.5*mm, "TOTAL NET À PAYER")
    c.drawRightString(re, y_box + 3.5*mm, fmt_xof(total))

    # 6. CONDITIONS + DÉLAIS (compact, tient sur toutes les versions)
    y6 = y_box - 9*mm
    c.setFont("Helvetica-Bold", 8.5); c.setFillColor(C_BLACK)
    c.drawString(ML, y6, "CONDITIONS & LIVRAISON")
    c.setFont("Helvetica", 8); c.setFillColor(C_MID)
    c.drawString(ML, y6 - 5*mm, "Acompte 50% obligatoire à la signature — solde avant livraison du fichier final.")
    c.drawString(ML, y6 - 9*mm, "Paiement : Wave / Orange Money / virement.  Livraison : lien Google Drive.")
    delais = objet.get("delais", "Délais : capsules 10s le jour J — récap 30s sous 48h — récap 60s & photos sous 5–7 jours.")
    c.drawString(ML, y6 - 13*mm, delais)

    # 7. FOOTER
    c.setStrokeColor(C_BORDER); c.setLineWidth(0.5); c.line(ML, 18*mm, W - MR, 18*mm)
    c.setFont("Helvetica", 7.5); c.setFillColor(C_MID)
    c.drawCentredString(W/2, 12*mm,
        'Studios 700 — "VOTRE IMAGE, EN MIEUX" — team@studios700.com — +225 07 77 22 52 77')


if __name__ == "__main__":
    for v in VERSIONS:
        out = os.path.join(OUTPUT_DIR, f"DEVIS_COCACOLAFEST_{v['tag']}.pdf")
        c = canvas.Canvas(out, pagesize=A4)
        _draw(c, v)
        c.save()
        total = sum(l["qte"] * l["prix"] for l in v["lignes"])
        print(f"OK  {v['tag']:12s} total={total:>10,} XOF  ->  {os.path.basename(out)}")
