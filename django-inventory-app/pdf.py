'''
print pdf with code labels
'''
import math
import io
from django.http import FileResponse, HttpResponseNotFound
from django.conf import settings
from reportlab.graphics.barcode import qr
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from reportlab.lib import pagesizes
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth


def code_labels(codes, request):
    ''' print codes use POST as array of integer '''
    page_format = getattr(settings, 'PAGE_FORMAT', 'A4')
    page_margin = getattr(settings, 'PAGE_MARGIN', 15) * mm
    codes_in_line = getattr(settings, 'CODES_IN_LINE', 6)
    codes_spacing = getattr(settings, 'CODES_SPACING', 5) * mm
    buffer = io.BytesIO()

    if not codes:
        return HttpResponseNotFound('<h1>No codes in list</h1>')

    # page width and height
    pagesize = getattr(pagesizes, page_format, pagesizes.A4)
    page = canvas.Canvas(buffer, pagesize=pagesize)
    page_width, page_height = pagesize

    # qrcode width and height
    string = hex(0x7FFFFFFF)[2:]
    url = request.build_absolute_uri('/' + string)
    qr_code = qr.QrCodeWidget(url)
    bounds = qr_code.getBounds()
    code_width = bounds[2] - bounds[0]
    code_height = bounds[3] - bounds[1]

    # place width and height
    space = page_margin * 2 + codes_spacing * (codes_in_line - 1)
    place_width = (page_width - space) / codes_in_line
    place_height = code_height * place_width / code_width
    font_size = place_width / len(string)
    line_height = place_height + font_size + codes_spacing
    rows_in_page = int((page_height - page_margin * 2 + codes_spacing) \
                    // line_height)
    on_page = rows_in_page * codes_in_line

    for cpage in range(0, math.ceil(len(codes)/on_page)):
        for i in range(0, on_page):
            cid = cpage * on_page + i
            if len(codes) <= cid:
                break
            string = hex(codes[cid])[2:]
            url = request.build_absolute_uri('/' + string)
            qr_code = qr.QrCodeWidget(url)
            bounds = qr_code.getBounds()
            width = bounds[2] - bounds[0]
            height = bounds[3] - bounds[1]
            drawing = Drawing(
                place_width,
                place_width,
                transform=[
                    place_width / width,
                    0,
                    0,
                    place_height / height,
                    0,
                    0
                ]
            )
            drawing.add(qr_code)
            code_x = page_margin + (i % codes_in_line) * \
                (place_width + codes_spacing)
            code_y = page_height - page_margin - line_height + codes_spacing - \
                (i // codes_in_line) * line_height
            renderPDF.draw(drawing, page, code_x, code_y)
            header = string.upper()
            text = page.beginText()
            text.setFont('Helvetica', font_size)
            text.setCharSpace(0)
            text_width = stringWidth(header, 'Helvetica', font_size)
            text_x = code_x + (place_width - text_width) / 2
            text.setTextOrigin(text_x, code_y + place_height)
            text.textLine(header)
            page.drawText(text)
        page.showPage()
    page.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='qrcodes.pdf')
