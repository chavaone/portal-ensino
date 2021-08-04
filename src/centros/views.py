from .models import Concello, Ensinanza, Centro, ListaCentros
from django.http import HttpResponse
import simplejson as json
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
def listas_usuario(request, pk_lista=False):
    response = {
        "result": "ok"
    }

    if not request.user.is_authenticated:
        response["result"] = "not-authenticated"
    elif request.method == 'GET':
        pass
    elif request.method == 'POST':
        body = json.loads(request.body)
        lista = ListaCentros(titulo=body["titulo"], centros=body["centros"], usuario=request.user)
        lista.save()
    elif request.method == 'DELETE' and pk_lista:
        lista = ListaCentros.objects.get(pk=pk_lista)
        if lista.usuario == request.user:
            lista.delete()
    else:
        response["result"] =  "method-not-valid"

    if response["result"] == "ok":
        listas = ListaCentros.objects.filter(usuario__pk=request.user.pk)
        response["list"] = [
            {
                "pk": lista.pk,
                "titulo": lista.titulo,
                "centros": lista.centros,
                "data": lista.data,
                "deletable": lista.deletable
            } for lista in listas
        ]

    data = json.dumps(response, default=str)
    return HttpResponse(data, content_type='application/json')
