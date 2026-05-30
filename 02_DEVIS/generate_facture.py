from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.platypus import Image
import os

OUTPUT = "/home/user/Studios700-workspace/02_DEVIS/FACTURE_MAGASIN_2026-001.pdf"
LOGO = "/home/user/Studios700-workspace/00_IDENTITE_MARQUE/logos/studios700_logo_blanc.png"

JAUNE = colors.HexColor("#FDD63A")
BLEU  = colors.HexColor("#3970B7")
NOIR  = colors.HexColor("#1A1A1A")
GRIS  = colors.HexColor("#F5F5F5")
GRIS2 = colors.HexColor("#CCCCCC")

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=15*mm,
    leftMargin=15*mm,
    topMargin=12*mm,
    bottomMargin=15*mm,
)

W = A4[0] - 30*mm
story = []

styles = getSampleStyleSheet()

def style(name="Normal", **kw):
    return ParagraphStyle(name, parent=styles["Normal"], **kw)

# ── HEADER : fond sombre + nom studio ────────────────────────────────────────
header_data = [[
    Paragraph(
        '<font color="#FDD63A"><b>STUDIOS 700</b></font>',
        style("H1", fontSize=20, textColor=JAUNE, alignment=TA_LEFT, leading=24)
    ),
    Paragraph(
        '<font color="#FDD63A"><b>FACTURE</b></font>',
        style("H", fontSize=26, textColor=JAUNE, alignment=TA_RIGHT, leading=30)
    )
]]
header_table = Table(header_data, colWidths=[W*0.5, W*0.5])
header_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), NOIR),
    ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
    ("LEFTPADDING",(0,0), (-1,-1), 8*mm),
    ("RIGHTPADDING",(0,0),(-1,-1), 8*mm),
    ("TOPPADDING", (0,0), (-1,-1), 6*mm),
    ("BOTTOMPADDING",(0,0),(-1,-1), 6*mm),
    ("LINEBELOW", (0,0), (-1,-1), 3, JAUNE),
]))
story.append(header_table)
story.append(Spacer(1, 6*mm))

# ── ÉMETTEUR / CLIENT ────────────────────────────────────────────────────────
em = style("EM", fontSize=9, leading=13, textColor=NOIR)
em_label = style("EL", fontSize=7, textColor=colors.HexColor("#888888"), leading=10)
em_bold  = style("EB", fontSize=9, leading=13, textColor=NOIR, fontName="Helvetica-Bold")

emetteur = [
    Paragraph("DE", em_label),
    Paragraph("<b>Studios 700</b>", em_bold),
    Paragraph("Alex Koffi", em),
    Paragraph("Abidjan, Côte d'Ivoire", em),
    Paragraph("team@studios700.com", em),
    Paragraph("+225 07 77 22 52 77", em),
    Paragraph("studios700.com", em),
]

client = [
    Paragraph("FACTURÉ À", em_label),
    Paragraph("<b>Magasin</b>", em_bold),
    Paragraph("(Nom du client à compléter)", em),
    Paragraph("Abidjan, Côte d'Ivoire", em),
]

meta = [
    Paragraph("DÉTAILS", em_label),
    Paragraph("<b>N° Facture :</b> FAC-2026-001", em),
    Paragraph("<b>Date :</b> 30/05/2026", em),
    Paragraph("<b>Valide :</b> 30 jours", em),
]

info_data = [[
    [p for p in emetteur],
    [p for p in client],
    [p for p in meta],
]]

def cell(items):
    return [i for i in items]

info_table = Table(
    [[cell(emetteur), cell(client), cell(meta)]],
    colWidths=[W*0.33, W*0.34, W*0.33]
)
info_table.setStyle(TableStyle([
    ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING",   (0,0), (-1,-1), 0),
    ("RIGHTPADDING",  (0,0), (-1,-1), 4*mm),
    ("TOPPADDING",    (0,0), (-1,-1), 0),
    ("BOTTOMPADDING", (0,0), (-1,-1), 0),
]))
story.append(info_table)
story.append(Spacer(1, 7*mm))
story.append(HRFlowable(width="100%", thickness=0.5, color=GRIS2))
story.append(Spacer(1, 5*mm))

# ── TABLEAU PRESTATIONS ──────────────────────────────────────────────────────
th = style("TH", fontSize=8, fontName="Helvetica-Bold", textColor=colors.white, alignment=TA_CENTER)
td = style("TD", fontSize=9, textColor=NOIR, leading=13)
td_c = style("TDC", fontSize=9, textColor=NOIR, leading=13, alignment=TA_CENTER)
td_r = style("TDR", fontSize=9, textColor=NOIR, leading=13, alignment=TA_RIGHT)

prestation_data = [
    # Header
    [
        Paragraph("DÉSIGNATION", th),
        Paragraph("QTÉ", th),
        Paragraph("PRIX UNITAIRE", th),
        Paragraph("TOTAL", th),
    ],
    # Ligne 1
    [
        Paragraph("Captation vidéo — Couverture 2 jours\n<font size='8' color='#666666'>Tournage terrain + direction artistique</font>", td),
        Paragraph("2 jours", td_c),
        Paragraph("100 000 XOF", td_r),
        Paragraph("200 000 XOF", td_r),
    ],
    # Ligne 2
    [
        Paragraph("Montage vidéo (livraison 48h)\n<font size='8' color='#666666'>Montage + exports réseaux sociaux inclus</font>", td),
        Paragraph("1", td_c),
        Paragraph("Inclus", td_r),
        Paragraph("—", td_r),
    ],
]

col_w = [W*0.50, W*0.13, W*0.18, W*0.19]
prest_table = Table(prestation_data, colWidths=col_w, repeatRows=1)
prest_table.setStyle(TableStyle([
    # Header
    ("BACKGROUND",    (0,0), (-1,0), NOIR),
    ("TEXTCOLOR",     (0,0), (-1,0), colors.white),
    ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",      (0,0), (-1,0), 8),
    ("TOPPADDING",    (0,0), (-1,0), 5*mm),
    ("BOTTOMPADDING", (0,0), (-1,0), 5*mm),
    ("LEFTPADDING",   (0,0), (-1,-1), 4*mm),
    ("RIGHTPADDING",  (0,0), (-1,-1), 4*mm),
    # Lignes alternées
    ("BACKGROUND",    (0,1), (-1,1), GRIS),
    ("BACKGROUND",    (0,2), (-1,2), colors.white),
    ("TOPPADDING",    (0,1), (-1,-1), 4*mm),
    ("BOTTOMPADDING", (0,1), (-1,-1), 4*mm),
    # Bordure basse header
    ("LINEBELOW",     (0,0), (-1,0), 2, JAUNE),
    # Bordure lignes
    ("LINEBELOW",     (0,1), (-1,-1), 0.3, GRIS2),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
]))
story.append(prest_table)
story.append(Spacer(1, 8*mm))

# ── RÉCAPITULATIF FINANCIER ──────────────────────────────────────────────────
recap_data = [
    ["Sous-total",       "200 000 XOF"],
    ["Taxes applicables","—"],
    ["TOTAL NET À PAYER","200 000 XOF"],
]

recap_label_style = [
    style("RL",  fontSize=9, textColor=NOIR, alignment=TA_RIGHT),
    style("RL",  fontSize=9, textColor=NOIR, alignment=TA_RIGHT),
    style("RLB", fontSize=11, fontName="Helvetica-Bold", textColor=colors.white, alignment=TA_RIGHT),
]
recap_val_style = [
    style("RV",  fontSize=9, textColor=NOIR, alignment=TA_RIGHT),
    style("RV",  fontSize=9, textColor=colors.HexColor("#999999"), alignment=TA_RIGHT),
    style("RVB", fontSize=11, fontName="Helvetica-Bold", textColor=colors.white, alignment=TA_RIGHT),
]

recap_fmt = []
for i, (label, val) in enumerate(recap_data):
    recap_fmt.append([Paragraph(label, recap_label_style[i]), Paragraph(val, recap_val_style[i])])

recap_w = [W*0.70, W*0.30]
recap_table = Table(recap_fmt, colWidths=recap_w)
recap_table.setStyle(TableStyle([
    ("ALIGN",         (0,0), (-1,-1), "RIGHT"),
    ("TOPPADDING",    (0,0), (-1,-1), 3*mm),
    ("BOTTOMPADDING", (0,0), (-1,-1), 3*mm),
    ("LEFTPADDING",   (0,0), (-1,-1), 4*mm),
    ("RIGHTPADDING",  (0,0), (-1,-1), 4*mm),
    ("LINEABOVE",     (0,2), (-1,2), 0.5, GRIS2),
    ("BACKGROUND",    (0,2), (-1,2), NOIR),
    ("ROUNDEDCORNERS",(0,2), (-1,2), [3,3,3,3]),
]))
story.append(recap_table)
story.append(Spacer(1, 8*mm))
story.append(HRFlowable(width="100%", thickness=0.5, color=GRIS2))
story.append(Spacer(1, 5*mm))

# ── CONDITIONS DE PAIEMENT ───────────────────────────────────────────────────
cond_style = style("COND", fontSize=8, textColor=NOIR, leading=12)
cond_bold  = style("CONDB", fontSize=8, fontName="Helvetica-Bold", textColor=NOIR, leading=12)

cond_data = [[
    [
        Paragraph("<b>MODALITÉS DE PAIEMENT</b>", cond_bold),
        Spacer(1, 2*mm),
        Paragraph("Virement / Mobile Money (Orange Money · Wave · MTN)", cond_style),
        Spacer(1, 1*mm),
        Paragraph("• Acompte 50% à la commande", cond_style),
        Paragraph("• Solde avant livraison du fichier final", cond_style),
    ],
    [
        Paragraph("<b>LIVRAISON</b>", cond_bold),
        Spacer(1, 2*mm),
        Paragraph("Lien Google Drive partagé", cond_style),
        Spacer(1, 1*mm),
        Paragraph("• Vidéos MP4 HD / 4K : 48h après tournage", cond_style),
        Paragraph("• 1 révision incluse (demande sous 7 jours)", cond_style),
    ],
]]

cond_table = Table(cond_data, colWidths=[W*0.50, W*0.50])
cond_table.setStyle(TableStyle([
    ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ("BACKGROUND",    (0,0), (-1,-1), GRIS),
    ("LEFTPADDING",   (0,0), (-1,-1), 5*mm),
    ("RIGHTPADDING",  (0,0), (-1,-1), 5*mm),
    ("TOPPADDING",    (0,0), (-1,-1), 5*mm),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5*mm),
    ("LINEAFTER",     (0,0), (0,-1), 0.5, GRIS2),
]))
story.append(cond_table)
story.append(Spacer(1, 8*mm))

# ── FOOTER ───────────────────────────────────────────────────────────────────
footer_style = style("FT", fontSize=7.5, textColor=colors.white, alignment=TA_CENTER, leading=11)
footer_data = [[
    Paragraph(
        'Studios 700 — "VOTRE IMAGE, EN MIEUX"   ·   team@studios700.com   ·   +225 07 77 22 52 77   ·   studios700.com',
        footer_style
    )
]]
footer_table = Table(footer_data, colWidths=[W])
footer_table.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), NOIR),
    ("TOPPADDING",    (0,0), (-1,-1), 4*mm),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4*mm),
    ("LINEABOVE",     (0,0), (-1,-1), 2, JAUNE),
]))
story.append(footer_table)

doc.build(story)
print(f"PDF généré : {OUTPUT}")
