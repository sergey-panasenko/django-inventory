'''
Some functions for inventory items view
'''
import io
import pyqrcode

def generate_qrcode(string, **kwargs):
    '''
    generate qrcode from string
    params: scale=1, module_color='#000', background=None, quiet_zone=4,
    xmldecl=True, svgns=True, title=None, svgclass='pyqrcode',
    lineclass='pyqrline', omithw=False, debug=False
    https://pythonhosted.org/PyQRCode/moddoc.html#pyqrcode.QRCode.svg
    '''
    code = pyqrcode.create(string)
    buffer = io.BytesIO()
    code.svg(buffer, **kwargs)
    return buffer.getvalue()
