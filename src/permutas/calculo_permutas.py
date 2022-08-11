
from django.db import connection
from .especialidades import ESPECIALIDADES
from .models import PreferenciasPermutas, Permuta
from profe.models import Profe


def _registra_permuta_1(permuta):
    pk1,pk2 = permuta
    profe_1 = PreferenciasPermutas.objects.get(pk=pk1)
    profe_2 = PreferenciasPermutas.objects.get(pk=pk2)
    per = Permuta(profe_1=profe_1, profe_2=profe_2)
    per.save()
    return per

def _registrar_permuta_n(permuta_multiple):
    permutas_creadas = [_registra_permuta_1(permuta) for permuta in permuta_multiple]

    for index, permuta in enumerate(permutas_creadas):
        if index == 0: continue
        permuta_ant = permutas_creadas[index-1]
        permuta.permuta_ant = permuta_ant
        permuta_ant.permuta_seg = permuta

    for permuta in permutas_creadas:
        permuta.save()
    return permutas_creadas

def _eliminar_permutas(esp, sit):
    Permuta.objects.all().filter(profe_1__especialidad=esp, profe_1__situacion=sit).delete()

def _registrar_permutas (lista_busca):
    pks_engadidos = []

    for profe in lista_busca:
        for permuta in profe["completas"]:
            print("\n\n permuta")
            print(permuta)
            indexes = permuta[0]
            pks = [lista_busca[ind]["pk"] for ind in indexes]

            if sorted(pks) in pks_engadidos: continue

            pk_inicial = pks.pop(0)
            permuta_multiple = [(pk_inicial, pk) for pk in pks]
            _registrar_permuta_n(permuta_multiple)
            pks_engadidos.append(sorted(pks))

    return len(pks_engadidos)



def _buscar_permutas_esp_sit (esp, sit, niveles=2):
    profes = PreferenciasPermutas.objects.all().filter(especialidad=esp, situacion=sit, activar_permutas=True)

    lista_busca = [ {
        "pk": prof_profe.pk,
        "centro_actual": str(prof_profe.centro_actual.codigo),
        "incompletas": [
            ([index],
             [str(prof_profe.centro_actual.codigo)])
        ],
        "novas_incompletas": [],
        "completas": [],
        "peticions": " ".join(map(lambda s: s["codigos"], prof_profe.lista_peticiones.centros))
    } for index, prof_profe in enumerate(profes)]


    for nivel_actual in range(niveles):

        #Recorremos os profesores
        for index_1, profe_1 in enumerate(lista_busca):
            print()
            print("profe1")
            print(profe_1)

            #Recorremos as permutas incompletas
            for incompleta in profe_1["incompletas"]:

                profes, centros = incompleta
                ultimo_centro = centros[-1]

                for index_2,profe_2 in enumerate(lista_busca):

                    if (index_2 < index_1) or (index_2 in profes) or (profe_2["centro_actual"] in centros):
                        continue
                    print("profe2")
                    print(profe_2)

                    coinc12 = ultimo_centro in profe_2["peticions"]
                    coinc21 = profe_2["centro_actual"] in profe_1["peticions"]

                    if coinc12 and coinc21: #Habemus permuta completa
                        novos_profes = list(profes)
                        novos_profes.append(index_2)
                        novos_centros = list(centros)
                        novos_centros.append(profe_2["centro_actual"])
                        profe_1["completas"].append((novos_profes, novos_centros))
                        print("0")
                        print(profe_1)
                    elif coinc12: #Engadimos outra permuta incompleta
                        novos_profes = list(profes)
                        novos_profes.append(index_2)
                        novos_centros = list(centros)
                        novos_centros.append(profe_2["centro_actual"])
                        profe_1["novas_incompletas"].append((novos_profes, novos_centros))
                        print("1")
                        print(profe_1)
                    elif coinc21 and not nivel_actual: #Só no primeiro nivel, engadimos permuta incompleta ao profe_2
                        novos_profes = [index_2, index_1]
                        novos_centros = [profe_2["centro_actual"], ultimo_centro]
                        profe_2["novas_incompletas"].append((novos_profes, novos_centros))
                        print("2")
                        print(profe_2)

        #Reseteamos a lista de permutas incompletas
        for profe in lista_busca:
            profe["incompletas"] = profe["novas_incompletas"]
            profe["novas_incompletas"] = []

    #Registramos as permutas
    creadas = _registrar_permutas(lista_busca)

    return creadas


def buscar_e_crear_permutas():
    log = ""

    pares_con_profes = []

    with connection.cursor() as c:
        c.execute('''SELECT especialidad, situacion
                    FROM permutas_preferenciaspermutas
                    WHERE activar_permutas = 1
                    GROUP BY especialidad, situacion
                    HAVING count(*) > 1''')
        pares_con_profes = c.fetchall()

    log += "Hai {0} pares especialidade e situación con polo menos dúas persoas.\n".format(len(pares_con_profes))

    for (esp, sit) in pares_con_profes:
        _eliminar_permutas(esp,sit)
        log += "Eliminadas permutas anteriores para a especialidade {0} e a situación {1}.\n".format(esp, sit)
        log+= "Buscando permutas para a especialidade {0} e a situación {1}.\n".format(esp, sit)
        num = _buscar_permutas_esp_sit(esp, sit)
        log+= "Encontradas {0} permutas.\n".format(num)
    return log
