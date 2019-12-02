import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
 
doc = SimpleDocTemplate("form_letter.pdf",pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)
Story=[]
logo = "logo_utn.png"
name = "Kevin Edgardo".upper()
surname = "Juarez Desch".upper()
dni = "37.261.933"
course = "Introducción a Nuevas Tecnologías".upper()
dates = [{"year"= "2019", "month"= "Octube", "days":["28","29","30","31"]}]
 
im = Image(logo, 250, 110)
Story.append(im)
 
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
""" ptext = '<font size=12>%s</font>' % formatted_time """
 
""" Story.append(Paragraph(ptext, styles["Normal"])) """
Story.append(Spacer(1, 12))
 
# Create return address
ptext = '<font size=12>CERTIFICADO DE FINALIZACIÓN</font>'
Story.append(Paragraph(ptext, styles["Normal"]))       
 
Story.append(Spacer(1, 12))
ptext = f'<font size=12>Este certificado se presenta a: {name} {surname} - DNI:{dni}</font>'
Story.append(Paragraph(ptext, styles["Normal"]))
Story.append(Spacer(1, 12))

""" Story.append(Paragraph(ptext, styles["Justify"]))"""
Story.append(Spacer(1, 12))
 
""" ptext = '<font size=12>Thank you very much and we look forward to serving you.</font>'
Story.append(Paragraph(ptext, styles["Justify"]))
Story.append(Spacer(1, 12))
ptext = '<font size=12>Sincerely,</font>'
Story.append(Paragraph(ptext, styles["Normal"]))
Story.append(Spacer(1, 48))
ptext = '<font size=12>Ima Sucker</font>'
Story.append(Paragraph(ptext, styles["Normal"]))
Story.append(Spacer(1, 12))"""
doc.build(Story)