'''
inventory views
'''
import io
from django.http import FileResponse, HttpResponseNotFound
from reportlab.graphics.barcode import qr
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase.pdfmetrics import stringWidth
from django.shortcuts import render
from django.conf import settings
from django.views.generic.base import View


class QRCodesPDFView(View):
    """ qrcodes view, return pdf with codes """

    def get(self, request):
        ''' print codes use GET as string with comma separated codes'''
        codes = request.GET.get('codes').split(',')
        self.kwargs['codes'] = [int(c) for c in codes]
        return self.post(request)

    def post(self, request):
        ''' print codes use POST as array of integer '''
        page_format = getattr(settings, 'PAGE_FORMAT', 'A4')
        page_margin = getattr(settings, 'PAGE_MARGIN', 50)
        codes_in_line = getattr(settings, 'CODES_IN_LINE', 6)
        codes_spacing = getattr(settings, 'CODES_SPACING', 10)
        codes = self.kwargs['codes'] if 'codes' in self.kwargs else []
        buffer = io.BytesIO()

        if not codes:
            return HttpResponseNotFound('<h1>No codes in list</h1>')

        # page width and height
        if page_format == 'letter':
            page = canvas.Canvas(buffer, pagesize=letter)
        else:
            page = canvas.Canvas(buffer, pagesize=A4)
        page_width, page_height = A4 # TODO: some pages on many codes

        # qrcode width and height
        string = hex(0x7FFFFFFF)[2:]
        url = request.build_absolute_uri('/' + string)
        qr_code = qr.QrCodeWidget(url)
        bounds = qr_code.getBounds()
        code_width = bounds[2] - bounds[0]
        code_height = bounds[3] - bounds[1]

        # place width and height
        space = page_margin * 2 - codes_spacing * (codes_in_line - 1)
        place_width = (page_width - space) / codes_in_line
        place_height = code_height * place_width / code_width
        font_size = place_width / len(string)

        for i in range(0, len(codes)):
            string = hex(codes[i])[2:]
            url = request.build_absolute_uri('/' + string)
            qr_code = qr.QrCodeWidget(url)
            bounds = qr_code.getBounds()
            width = bounds[2] - bounds[0]
            height = bounds[3] - bounds[1]
            drawing = Drawing(
                place_width,
                place_width,
                transform=[
                    width / code_width,
                    0,
                    0,
                    height / code_height,
                    0,
                    0
                ]
            )
            drawing.add(qr_code)
            code_x = page_margin + (i % codes_in_line) * \
                (place_width + codes_spacing)
            code_y = page_margin + (i // codes_in_line) * \
                (place_height + font_size + codes_spacing)
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
