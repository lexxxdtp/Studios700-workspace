"""
Studios 700 — FACTURE D'ACOMPTE — Conférence Golden Impact (ANB Corporate)
=========================================================================
Acompte 50% reçu : 150 000 XOF sur prestation totale 300 000 XOF.
Basé sur la charte facture officielle Studios 700 (Noir & Blanc).
Usage :  python3 facture_acompte_goldenimpact.py
"""

from PIL import Image, ImageFile, ImageOps
ImageFile.LOAD_TRUNCATED_IMAGES = True
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
import io, os

DATA = {
    "numero": "FACT-AC-2026-007",
    "date":   "20 juin 2026",
    "client": {"nom": "Golden Impact",
               "adresse": "Abidjan, Côte d'Ivoire"},
    "objet": "Couverture vidéo & montage récap — Conférence Golden Impact",
    "total_prestation": 300000,
    "acompte": 150000,
    "ligne": {
        "titre": "Acompte 50% — Prestation Golden Impact",
        "description": ["Couverture vidéo & montage récap (Conférence Golden Impact)",
                        "Acompte versé le 20/06/2026 par transfert mobile money"],
    },
}

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


def _draw(c, d):
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
    y = H - hh - 15*mm
    c.setFont("Helvetica-Bold", 24); c.setFillColor(C_BLACK); c.drawString(ML, y, "FACTURE D'ACOMPTE")
    y2 = y - 8*mm
    c.setFont("Helvetica-Bold", 9); c.setFillColor(C_DARK)
    c.drawString(ML, y2, f"N° :  {d['numero']}")
    c.drawRightString(W - MR, y2, f"Date : {d['date']}")
    c.setStrokeColor(C_BLACK); c.setLineWidth(1); c.line(ML, y2 - 3*mm, W - MR, y2 - 3*mm)

    # 3. DE / FACTURER À
    y3 = y2 - 7*mm; bh = 32*mm
    c.setFillColor(C_LIGHT); c.roundRect(ML, y3 - bh, W - ML - MR, bh, 3, fill=1, stroke=0)
    lx = ML + 5*mm; rx = W/2 + 5*mm; ty = y3 - 5*mm
    c.setFont("Helvetica-Bold", 8); c.setFillColor(C_DARK); c.drawString(lx, ty, "DE :")
    c.setFont("Helvetica-Bold", 9.5); c.drawString(lx, ty - 5.5*mm, "Studios 700")
    c.setFont("Helvetica", 8.5); c.setFillColor(C_MID)
    for i, t in enumerate(["Alex Vianney Koffi", "Abidjan, Côte d'Ivoire",
                            "team@studios700.com", "+225 07 77 22 52 77"]):
        c.drawString(lx, ty - 11*mm - i*4.3*mm, t)
    c.setFont("Helvetica-Bold", 8); c.setFillColor(C_DARK); c.drawString(rx, ty, "FACTURER À :")
    c.setFont("Helvetica-Bold", 9.5); c.drawString(rx, ty - 5.5*mm, "Golden Impact")
    c.setFont("Helvetica", 8.5); c.setFillColor(C_MID)
    for i, t in enumerate(["Abidjan, Côte d'Ivoire",
                            "Suivi comptable : ANB Corporate"]):
        c.drawString(rx, ty - 11*mm - i*4.3*mm, t)

    # 3b. OBJET
    yo = y3 - bh - 6*mm
    c.setFont("Helvetica-Bold", 8); c.setFillColor(C_BLACK); c.drawString(ML, yo, "OBJET :")
    c.setFont("Helvetica", 8.5); c.setFillColor(C_DARK); c.drawString(ML + 16*mm, yo, d["objet"])

    # 4. TABLEAU (ligne unique acompte)
    y4 = yo - 9*mm
    col_w = [W - ML - MR - 55*mm, 14*mm, 27*mm, 24*mm]
    th = 9*mm
    c.setFillColor(C_BLACK); c.rect(ML, y4 - th, sum(col_w), th, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 8); c.setFillColor(C_WHITE)
    xp = ML
    for i, (hdr, cw) in enumerate(zip(["DÉSIGNATION", "QTÉ", "PRIX UNIT.", "TOTAL"], col_w)):
        cy = y4 - th + 3.2*mm
        c.drawString(xp + 3*mm, cy, hdr) if i == 0 else c.drawCentredString(xp + cw/2, cy, hdr)
        xp += cw
    rh = 18*mm
    row_y = y4 - th
    c.setFillColor(C_WHITE); c.rect(ML, row_y - rh, sum(col_w), rh, fill=1, stroke=0)
    c.setStrokeColor(C_BORDER); c.setLineWidth(0.4); c.rect(ML, row_y - rh, sum(col_w), rh, fill=0, stroke=1)
    xd = ML + col_w[0]
    for cw in col_w[1:]:
        c.line(xd, row_y, xd, row_y - rh); xd += cw
    c.setFont("Helvetica-Bold", 9); c.setFillColor(C_DARK)
    c.drawString(ML + 3*mm, row_y - 6*mm, d["ligne"]["titre"])
    c.setFont("Helvetica", 7.5); c.setFillColor(C_MID)
    for j, dl in enumerate(d["ligne"]["description"]):
        c.drawString(ML + 3*mm, row_y - 11*mm - j*4*mm, dl)
    mid_y = row_y - rh/2 + 1*mm
    c.setFont("Helvetica", 9); c.setFillColor(C_DARK)
    c.drawCentredString(ML + col_w[0] + col_w[1]/2, mid_y, "1")
    c.drawCentredString(ML + col_w[0] + col_w[1] + col_w[2]/2, mid_y, fmt_xof(d["acompte"]))
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(ML + col_w[0] + col_w[1] + col_w[2] + col_w[3]/2, mid_y, fmt_xof(d["acompte"]))
    row_y -= rh

    # 5. RÉCAP ACOMPTE / SOLDE
    solde = d["total_prestation"] - d["acompte"]
    y5 = row_y - 8*mm
    re = W - MR; lbl = re - 78*mm
    c.setFont("Helvetica", 8.5); c.setFillColor(C_MID)
    c.drawString(lbl, y5, "MONTANT TOTAL PRESTATION"); c.drawRightString(re, y5, fmt_xof(d["total_prestation"]))
    c.drawString(lbl, y5 - 7*mm, "ACOMPTE VERSÉ (50%)"); c.drawRightString(re, y5 - 7*mm, "- " + fmt_xof(d["acompte"]))
    c.setStrokeColor(C_BORDER); c.setLineWidth(0.4); c.line(lbl - 3*mm, y5 - 11*mm, re, y5 - 11*mm)
    c.setFont("Helvetica-Bold", 9); c.setFillColor(C_DARK)
    c.drawString(lbl, y5 - 16*mm, "SOLDE RESTANT DÛ"); c.drawRightString(re, y5 - 16*mm, fmt_xof(solde))

    # Box : ACOMPTE REÇU
    y_box = y5 - 20*mm - 11*mm
    c.setFillColor(C_BLACK); c.rect(lbl - 3*mm, y_box, re - lbl + 3*mm, 11*mm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 10); c.setFillColor(C_WHITE)
    c.drawString(lbl, y_box + 3.5*mm, "ACOMPTE REÇU")
    c.drawRightString(re, y_box + 3.5*mm, fmt_xof(d["acompte"]))

    # 6. NOTES
    y6 = y_box - 12*mm
    c.setFont("Helvetica-Bold", 8.5); c.setFillColor(C_BLACK); c.drawString(ML, y6, "STATUT & CONDITIONS")
    c.setFont("Helvetica", 8); c.setFillColor(C_MID)
    c.drawString(ML, y6 - 5*mm, "Acompte de 150 000 XOF reçu le 20/06/2026 — statut : PAYÉ.")
    c.drawString(ML, y6 - 9*mm, "Solde de 150 000 XOF à régler avant la livraison du fichier final.")
    c.drawString(ML, y6 - 13*mm, "Paiement : Wave / Orange Money / virement.  Livraison : lien Google Drive.")

    # 7. FOOTER
    c.setStrokeColor(C_BORDER); c.setLineWidth(0.5); c.line(ML, 18*mm, W - MR, 18*mm)
    c.setFont("Helvetica", 7.5); c.setFillColor(C_MID)
    c.drawCentredString(W/2, 12*mm,
        "Merci pour votre confiance ! Pour toute question, contactez-nous à team@studios700.com.")


if __name__ == "__main__":
    out = os.path.join(OUTPUT_DIR, "FACTURE_ACOMPTE_GOLDENIMPACT_150K.pdf")
    c = canvas.Canvas(out, pagesize=A4); _draw(c, DATA); c.save()
    print(f"OK  ->  {os.path.basename(out)}")
