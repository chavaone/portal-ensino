from .models import Concello, Ensinanza, Centro
from django.http import HttpResponse
import simplejson as json

# Create your views here.
def todos_os_centros(request):
    centros = Centro.objects.all()

    centros = [
        {
            "cod": centro.codigo,
            "nome": centro.nome,
            "con": centro.concello.nome,
            "prov": centro.concello.provincia,
        	"coor": {
        		"lat": centro.coorlat,
        		"lon": centro.coorlon
        	},
        	"ens": list(set(
                    [ensinanza.tipo for ensinanza in centro.ensinanzas.iterator()]
                )),
        } for centro in centros
    ]

    data = json.dumps(centros)
    return HttpResponse(data, content_type='application/json')

def datos_centro(request, codigo_req):
    try:
        centro = Centro.objects.get(codigo=codigo_req)
        centro_json = {
            "cod": centro.codigo,
            "nome": centro.nome,
            "con": centro.concello.nome,
            "prov": centro.concello.provincia,
        	"coor": {
        		"lat": centro.coorlat,
        		"lon": centro.coorlon
        	},
            "end": centro.enderezo,
            "cp": centro.cp,
        	"ens": [
                {
                    "tipo": ensinanza.tipo,
                    "grado": ensinanza.grado,
                    "nome": ensinanza.nome
                } for ensinanza in centro.ensinanzas.iterator()]
        }

        if centro.web:
            centro_json["web"] = centro.web

        if centro.telefono:
            centro_json["tlf"] = centro.telefono

        if centro.email:
            centro_json["email"] = centro.email

        data = json.dumps(centro_json)
        return HttpResponse(data, content_type='application/json')

    except ObjectDoesNotExist:
        raise Http404("Center does not exists.")
