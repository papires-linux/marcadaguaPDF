# Exemplo de comando:
# python script_waterpaper-docs.py \
#   -i "documento.pdf" \
#   -t "Gerar o texto" \
#   -o "documento_withwatermark.pdf"

from PyPDF2 import PdfWriter, PdfReader
import argparse
from pdf2image  import convert_from_path

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True)
parser.add_argument("-t", "--text", required=True)
parser.add_argument("-o", "--output", required=True)
args = parser.parse_args()

INPUT_FILE     = str(args.input)
TEXTO          = str(args.text)
OUTPUT_FILE    = str(args.output)

def gerar_linha_backgroud(TEXTO):
    CARACTERES_LIMIT = 180
    REPETICOES = round(CARACTERES_LIMIT/len(TEXTO))
    valor = TEXTO
    for i in range(REPETICOES):
         valor += TEXTO
    return valor[:CARACTERES_LIMIT]

def gerar_texto_backgroud(TEXTO):    
    valor = TEXTO
    for i in range(90):
        valor += gerar_linha_backgroud(TEXTO) + "\n"
    return valor

def gerar_html(TEXTO):
    file_html = open("template.html", "w")
    file_html.write("<html><span style=\"opacity: 0.1;\">")
    file_html.write("<font color=\"black\" face=\"arial\" size=\"1\">" + gerar_texto_backgroud(TEXTO) +"</font>")
    file_html.write("</html>")
    file_html.close()
    gerar_html_pdf()

def gerar_html_pdf():
    import os
    from pyhtml2pdf import converter
    path = os.path.abspath('template.html')
    converter.convert(f'file:///{path}', 'sample.pdf')

def gerar_pdf_to_jpeg(SOURCE):
    images = convert_from_path(SOURCE)
    for i, image in enumerate(images):
        image.save(SOURCE+str(i)+'.jpeg', 'JPEG')   

def gerar_jpeg_to_pdf(FILE_PDF):
    from PIL import Image
    image_1 = Image.open(FILE_PDF+'0.jpeg')
    im_1 = image_1.convert('RGB')
    im_1.save(FILE_PDF)

def gerar_pdf_watermark(INPUT_FILE,OUTPUT_FILE):    
    watermark = PdfReader("sample.pdf")
    writer = PdfWriter()
    reader = PdfReader(INPUT_FILE)
    for page in reader.pages:        
        page.merge_page(watermark.pages[0])
        writer.add_page(page)
    with open(OUTPUT_FILE, "wb") as fp:
        writer.write(fp)
    
    #Sistema de regerar o pdf como figura.
    gerar_pdf_to_jpeg(OUTPUT_FILE)
    gerar_jpeg_to_pdf(OUTPUT_FILE)

gerar_html("LGPD - "+TEXTO+" - documento digital - ")
print("Será salvo no "+OUTPUT_FILE)
gerar_pdf_watermark(INPUT_FILE,OUTPUT_FILE)
