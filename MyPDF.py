from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont
import datetime


def generar_pdf(data):
    registerFont(TTFont('Calibri', './Fonts/calibri.ttf')) # Just some Ft imports
    registerFont(TTFont('Calibri-Bold', './Fonts/calibrib.ttf'))
    
    Story=[]
    logo = "logo_utn.png"
    name = data.pop("name", "")
    surname = data.pop("surname", "")
    dni = data.pop("dni", "")
    teachers = data.pop("teachers", "")
    course = data.pop("course", "")
    dates = data.pop("dates", "")
    
    cert_name = course + " - " + name + " - " + str(datetime.datetime.now().time()).replace(":", "").replace(".", "")
    doc = SimpleDocTemplate(f"./certificados/{cert_name}.pdf",pagesize=landscape(letter),
                            rightMargin=72,leftMargin=72,
                            topMargin=72,bottomMargin=18)

    im = Image(logo, 250, 110)
    Story.append(im)
    
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_CENTER))

    Story.append(Spacer(1, 12))
    ptext = '<font face=Calibri-Bold size=35>CERTIFICADO DE FINALIZACIÓN</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))       
    
    Story.append(Spacer(1, 50))
    ptext = f'<font face=Calibri size=20>Este certificado se presenta a:</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))

    Story.append(Spacer(1, 28))
    ptext = f'<font face=Calibri-Bold size=20>{name} {surname}<font face=Calibri size=20> - DNI: </font>{dni}</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))

    Story.append(Spacer(1, 28))
    ptext = f'<font face=Calibri size=20>Por completar el curso:</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))

    Story.append(Spacer(1, 28))
    ptext = f'<font face=Calibri-Bold size=20>{course}</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))

    Story.append(Spacer(1, 28))
    ptext = f'<font face=Calibri size=20>A cargo de:</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))

    Story.append(Spacer(1, 28))
    ptext = f'<font face=Calibri-Bold size=20>{teachers}</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))

    Story.append(Spacer(1, 28))
    ptext = f'<font face=Calibri size=20>En fecha <font face=Calibri-Bold size=20>{dates}</font></font>'
    Story.append(Paragraph(ptext, styles["Justify"]))


    doc.build(Story)