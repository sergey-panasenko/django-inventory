'''
inventory views
'''
from django.views.generic.base import View, TemplateView
from django.http import Http404
from .pdf import code_labels
from .models import Box


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


class codeView(TemplateView):
    """ show item by link """
    template_name = "django_inventory_app/box.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            code = int('0x' + self.kwargs['code'], 16)
            box = Box.objects.get(code=code)
        except Box.DoesNotExist:
            raise Http404("Box does not exist")
        context['box'] = box
        return context
