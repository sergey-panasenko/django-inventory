'''
inventory views
'''
from django.views.generic.base import View
from .pdf import code_labels


class QRCodesPDFView(View):
    """ qrcodes view, return pdf with codes """

    def get(self, request):
        ''' print codes use GET as string with comma separated codes'''
        codes = request.GET.get('codes').split(',')
        self.kwargs['codes'] = [int(c) for c in codes]
        return self.post(request)

    def post(self, request):
        ''' print codes use POST as array of integer '''
        codes = self.kwargs['codes'] if 'codes' in self.kwargs else []
        return code_labels(codes, request)
