from django.shortcuts import render
from django.views import generic
from .forms import FormPreferenciasPermutas
from .models import PreferenciasPermutas, Permuta
from django.urls import reverse_lazy
from centros.models import Centro
from .calculo_permutas import buscar_e_crear_permutas
from django.http import HttpResponse
from ensinopublico.settings import PASSWORD_BUSCAR_PERMUTAS
from django.db.models import Q

class ModificarPreferenciasPermutas (generic.UpdateView):
    model = PreferenciasPermutas
    form_class = FormPreferenciasPermutas
    template_name = 'permutas_preferences_edit.html'
    success_url = reverse_lazy('edit_profe_permutas')

    #get object
    def get_object(self, queryset=None):
        (instancia, _) = PreferenciasPermutas.objects.get_or_create(usuario=self.request.user)
        return instancia

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["centros"] = Centro.objects.all()
        return context

    def get_form_kwargs(self):
        kwargs = super(ModificarPreferenciasPermutas, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

def calcular_permutas (request, codigo):
    if codigo != PASSWORD_BUSCAR_PERMUTAS:
        return HttpResponse('Unauthorized', status=401)

    log = buscar_e_crear_permutas().replace("\n","</br>")
    return render(request, 'log_busca_permutas.html', {"log": log})


def _get_permuta (permuta):
    if permuta.permuta_ant:
        return _get_permuta(permuta.permuta_ant)
    else:
        ret_permuta = [{
            "profe1": permuta.profe_1,
            "profe2": permuta.profe_2,
            "centro1": permuta.profe_1.centro_actual.nome,
            "centro2": permuta.profe_2.centro_actual.nome
        }]
        per_seg = permuta.permuta_seg

        while per_seg:
            ret_permuta.append({
                "profe1": per_seg.profe_1,
                "profe2": per_seg.profe_2,
                "centro1": per_seg.permuta_ant.profe_2.centro_actual.nome,
                "centro2": per_seg.profe_2.centro_actual.nome
            })
            per_seg = per_seg.permuta_seg

        return ret_permuta

def _buscar_centro_def (permuta_compuesta, user):
    find_index = -1
    for ind, per in enumerate(permuta):
        if user == per["profe1"] or user == per["profe2"]:
            find_index = ind
            break

    if find_index == -1:
        return






def ver_permutas (request):

    if not request.user.is_authenticated:
        return render(request, 'ver_permutas_encontradas.html', {"authenticated": False})

    permutas_raw = Permuta.objects.all().filter(Q(profe_1__usuario=request.user.pk) | Q(profe_2__usuario=request.user))

    permutas = [_get_permuta(permuta) for permuta in permutas_raw]

    return render(request, 'ver_permutas_encontradas.html', {"authenticated": True, "permutas":permutas, "usuario":request.user})
