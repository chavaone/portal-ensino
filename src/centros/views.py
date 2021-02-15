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
            "concello": centro.concello.nome,
            "provincia": centro.concello.provincia,
        	"coordenadas": {
        		"lat": centro.coorlat,
        		"lon": centro.coorlon
        	},
            "tlf": centro.telefono,
            "enderezo": centro.enderezo,
            "cp": centro.cp,
            "web": centro.web,
        	"ensinanzas": [
                {
                    "nome": ensinanza.nome,
                    "tipo": ensinanza.tipo,
                    "grado":ensinanza.grado
                } for ensinanza in centro.ensinanzas.iterator()
            ],
        } for centro in centros
    ]

    data = json.dumps(centros)
    return HttpResponse(data, content_type='application/json')
