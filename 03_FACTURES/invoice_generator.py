"""
Studios 700 — Générateur de factures
=====================================
Identité visuelle : Noir & Blanc | Logo officiel studios700.
Usage : modifier INVOICE_DATA puis exécuter  →  python3 invoice_generator.py
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
#  DONNÉES  ← seule section à modifier à chaque facture
# ─────────────────────────────────────────────────────────────────
INVOICE_DATA = {
    "numero": "FACT-2026-006",
    "date":   "12 juin 2026",
    "client": {
        "nom":     "M. Moloko Pierre",
        "adresse": "Abidjan, Côte d'Ivoire",
    },
    "lignes": [
        {
            "titre":       "Couverture photo — 2 jours",
            "description": ["Captation photo complète de l'événement",
                            "150 000 XOF / jour"],
            "qte":   2,
            "prix":  150000,
        },
        {
            "titre":       "Couverture vidéo — 2 jours",
            "description": ["Captation vidéo complète de l'événement",
                            "150 000 XOF / jour"],
            "qte":   2,
            "prix":  150000,
        },
        {
            "titre":       "Post-production",
            "description": ["Tri et retouche photos, montage vidéo,",
                            "étalonnage et livraison des fichiers finaux"],
            "qte":   1,
            "prix":  100000,
        },
    ],
    "tva": None,   # None = sans TVA | ex: 18 pour 18%
}

LOGO_PATH  = os.path.join(os.path.dirname(os.path.abspath(__file__)),
             "../00_IDENTITE_MARQUE/logos/studios700_logo_noir.png")
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Charte graphique (ne pas modifier) ───────────────────────────
C_BLACK  = colors.HexColor("#111111")
C_DARK   = colors.HexColor("#222222")
C_MID    = colors.HexColor("#555555")
C_LIGHT  = colors.HexColor("#f4f4f4")
C_BORDER = colors.HexColor("#cccccc")
C_WHITE  = colors.white
W, H = A4
ML = 20*mm; MR = 20*mm


def fmt_xof(n):
    return f"{n:,.0f}".replace(",", " ") + " XOF"


def load_logo_white(path):
    """Charge le logo noir et le convertit en blanc pour fond sombre."""
    img = Image.open(path).convert("RGBA")
    r, g, b, a = img.split()
    white = Image.merge("RGBA", (ImageOps.invert(r), ImageOps.invert(g), ImageOps.invert(b), a))
    buf = io.BytesIO(); white.save(buf, format="PNG"); buf.seek(0)
    return ImageReader(buf)


def generate_invoice(data, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    _draw(c, data)
    c.save()
    print(f"✓  {output_path}")


def _draw(c, d):
    # ── 1. HEADER ────────────────────────────────────────────────
    hh = 42*mm
    c.setFillColor(C_BLACK)
    c.rect(0, H - hh, W, hh, fill=1, stroke=0)

    logo_img = load_logo_white(LOGO_PATH)
    logo_w = 58*mm; logo_h = logo_w * (256/882)
    c.drawImage(logo_img, ML, H - hh/2 - logo_h/2, width=logo_w, height=logo_h, mask='auto')

    c.setFont("Helvetica", 6.5); c.setFillColor(colors.HexColor("#999999"))
    c.drawRightString(W - MR, H - 10*mm, "VOTRE IMAGE, EN MIEUX")
    for i, line in enumerate(["team@studios700.com", "+225 07 77 22 52 77", "studios700.com"]):
        c.setFont("Helvetica-Bold" if i==0 else "Helvetica", 7.5)
        c.setFillColor(C_WHITE)
        c.drawRightString(W - MR, H - 15*mm - i*5*mm, line)

    # ── 2. TITRE ─────────────────────────────────────────────────
    y = H - hh - 15*mm
    c.setFont("Helvetica-Bold", 28); c.setFillColor(C_BLACK)
    c.drawString(ML, y, "FACTURE")

    y2 = y - 8*mm
    c.setFont("Helvetica-Bold", 9); c.setFillColor(C_DARK)
    c.drawString(ML, y2, f"N° :  {d['numero']}")
    c.drawRightString(W - MR, y2, f"Date : {d['date']}")
    c.setStrokeColor(C_BLACK); c.setLineWidth(1)
    c.line(ML, y2 - 3*mm, W - MR, y2 - 3*mm)

    # ── 3. DE / FACTURER À ───────────────────────────────────────
    y3 = y2 - 7*mm; bh = 32*mm
    c.setFillColor(C_LIGHT)
    c.roundRect(ML, y3 - bh, W - ML - MR, bh, 3, fill=1, stroke=0)
    lx = ML + 5*mm; rx = W/2 + 5*mm; ty = y3 - 5*mm

    c.setFont("Helvetica-Bold", 8); c.setFillColor(C_DARK); c.drawString(lx, ty, "DE :")
    c.setFont("Helvetica-Bold", 9.5); c.drawString(lx, ty - 5.5*mm, "Studios 700")
    c.setFont("Helvetica", 8.5); c.setFillColor(C_MID)
    for i, t in enumerate(["Alex Vianney Koffi","Abidjan, Côte d'Ivoire",
                            "team@studios700.com","+225 07 77 22 52 77"]):
        c.drawString(lx, ty - 11*mm - i*4.3*mm, t)

    c.setFont("Helvetica-Bold", 8); c.setFillColor(C_DARK); c.drawString(rx, ty, "FACTURER À :")
    c.setFont("Helvetica-Bold", 9.5); c.drawString(rx, ty - 5.5*mm, d["client"]["nom"])
    c.setFont("Helvetica", 8.5); c.setFillColor(C_MID)
    c.drawString(rx, ty - 11*mm, d["client"]["adresse"])

    # ── 4. TABLEAU ────────────────────────────────────────────────
    y4 = y3 - bh - 8*mm
    col_w = [W - ML - MR - 55*mm, 14*mm, 27*mm, 24*mm]
    th = 9*mm

    c.setFillColor(C_BLACK)
    c.rect(ML, y4 - th, sum(col_w), th, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 8); c.setFillColor(C_WHITE)
    xp = ML
    for i, (hdr, cw) in enumerate(zip(["DESCRIPTION","QTÉ","PRIX UNITAIRE","TOTAL"], col_w)):
        cy = y4 - th + 3.2*mm
        c.drawString(xp + 3*mm, cy, hdr) if i==0 else c.drawCentredString(xp + cw/2, cy, hdr)
        xp += cw

    row_y = y4 - th
    for ligne in d["lignes"]:
        rh = max(20*mm, (len(ligne["description"]) + 2) * 5*mm)
        c.setFillColor(C_WHITE)
        c.rect(ML, row_y - rh, sum(col_w), rh, fill=1, stroke=0)
        c.setStrokeColor(C_BORDER); c.setLineWidth(0.4)
        c.rect(ML, row_y - rh, sum(col_w), rh, fill=0, stroke=1)
        xd = ML + col_w[0]
        for cw in col_w[1:]:
            c.line(xd, row_y, xd, row_y - rh); xd += cw

        c.setFont("Helvetica-Bold", 9); c.setFillColor(C_DARK)
        c.drawString(ML + 3*mm, row_y - 6*mm, ligne["titre"])
        c.setFont("Helvetica", 8); c.setFillColor(C_MID)
        for j, dl in enumerate(ligne["description"]):
            c.drawString(ML + 3*mm, row_y - 11.5*mm - j*4.5*mm, dl)

        mid_y = row_y - rh/2 + 1.5*mm
        c.setFont("Helvetica", 9); c.setFillColor(C_DARK)
        c.drawCentredString(ML + col_w[0] + col_w[1]/2, mid_y, str(ligne["qte"]))
        c.drawCentredString(ML + col_w[0] + col_w[1] + col_w[2]/2, mid_y, fmt_xof(ligne["prix"]))
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(ML + col_w[0] + col_w[1] + col_w[2] + col_w[3]/2, mid_y,
                            fmt_xof(ligne["qte"] * ligne["prix"]))
        row_y -= rh

    # ── 5. TOTAUX ─────────────────────────────────────────────────
    sous_total = sum(l["qte"] * l["prix"] for l in d["lignes"])
    tva_amt = round(sous_total * d["tva"] / 100) if d["tva"] else None
    total = sous_total + (tva_amt or 0)

    y5 = row_y - 7*mm
    re = W - MR; lbl = re - 72*mm
    row_gap = 9*mm; box_h = 11*mm; pad = 3.5*mm

    c.setFont("Helvetica", 8.5); c.setFillColor(C_MID)
    c.drawString(lbl, y5, "SOUS-TOTAL")
    c.drawRightString(re, y5, fmt_xof(sous_total))

    y_tva = y5 - row_gap
    c.drawString(lbl, y_tva, f"TVA ({d['tva']}%)" if d["tva"] else "TAXES / TVA")
    c.drawRightString(re, y_tva, fmt_xof(tva_amt) if tva_amt else "—")

    c.setStrokeColor(C_BORDER); c.setLineWidth(0.4)
    c.line(lbl - 3*mm, y_tva - 4*mm, re, y_tva - 4*mm)

    y_box = y_tva - 4*mm - box_h
    c.setFillColor(C_BLACK)
    c.rect(lbl - 3*mm, y_box, re - lbl + 3*mm, box_h, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 10); c.setFillColor(C_WHITE)
    c.drawString(lbl, y_box + pad, "TOTAL À PAYER")
    c.drawRightString(re, y_box + pad, fmt_xof(total))

    # ── 6. PAIEMENT ───────────────────────────────────────────────
    y6 = y_box - 12*mm
    c.setFont("Helvetica-Bold", 9); c.setFillColor(C_BLACK)
    c.drawString(ML, y6, "MODALITÉS DE PAIEMENT")
    c.setFont("Helvetica", 8.5); c.setFillColor(C_MID)
    c.drawString(ML, y6 - 6*mm, "Paiement par virement mobile money ou espèces.")

    # ── 7. FOOTER ─────────────────────────────────────────────────
    c.setStrokeColor(C_BORDER); c.setLineWidth(0.5)
    c.line(ML, 18*mm, W - MR, 18*mm)
    c.setFont("Helvetica", 7.5); c.setFillColor(C_MID)
    c.drawCentredString(W/2, 12*mm,
        "Merci pour votre confiance ! Pour toute question, contactez-nous à team@studios700.com.")


# ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    num  = INVOICE_DATA["numero"]
    slug = INVOICE_DATA["client"]["nom"].replace(" ", "").upper()
    out  = os.path.join(OUTPUT_DIR, f"FACTURE_{slug}_{num.replace('-','_')}.pdf")
    generate_invoice(INVOICE_DATA, out)
