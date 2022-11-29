from django import forms

from calls.models import Called


class AuthorCalledForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Called
        fields = 'title', 'user_requester', 'priority','appliedsolution', 'call_defect', 'description', 'pendencies', 'category','is_resolved',
        labels = {
            'title':'Titulo',
            'user_requester':'Us. Solicitante: ',
            'priority':'Prioridade: ',
            'appliedsolution':'Solução Aplicada Em: ',
            'call_defect':'Defeito relatado',
            'description':'Solução Aplicada',
            'pendencies':'Pendencias',
            'category':'Setor: ',
            'is_resolved':'Resolvido: ',
        }