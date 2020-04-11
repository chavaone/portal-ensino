#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import codecs
import centros.models as mods
import requests
from bs4 import BeautifulSoup

session = requests.Session()
session.get("https://www.edu.xunta.es/centroseducativos")

TIPO_ENSINANZAS = {
    'Ciclos formativos': 'FP',
    'Educación secundaria obrigatoria': 'ESO',
    'Ensinanzas básicas iniciais': 'EBI',
    'Educación secundaria para persoas adultas': 'ESA',
    'Educación primaria': 'PRI',
    'Educación infantil': 'INF',
    'Ensinanzas de idiomas': 'IDI',
    'Ensinanzas de danza': 'DAN',
    'Educación Especial': 'ESP',
    'Bacharelato': 'BAC',
    'Ensinanzas de música': 'MUS'
}

TIPO_GRADO = {
    u"ciclos formativos de grao medio": 'M',
    u"formación profesional básica": 'B',
    u"ciclos formativos de grao superior": "S",
    u"ensinanzas superiores de música": "S",
    u"grao superior música": "S",
    u"grao medio música": "M",
}

def get_data_centro (centro):
    cod = centro.codigo

    r = session.get("https://www.edu.xunta.es/centroseducativos/CargarOfertaCentro.do?codigo=" + str(cod))
    soup = BeautifulSoup(r.text, "html.parser")
    lista = soup.find_all("tr")[1:]

    item = lista.pop(0)
    try:
        while True:
            tipoensinanza = item.find_all("td")[0].text
            rexime = item.find_all("td")[2].text

            if item["class"][1] == "arbolNivel0" and (not lista or lista[0]["class"] == "arbolNivel0"):
                if tipoensinanza not in TIPO_ENSINANZAS:
                    item = lista.pop(0)
                    continue
                ensinanza = mods.Ensinanza.objects.get_or_create(nome=tipoensinanza, tipo=TIPO_ENSINANZAS[tipoensinanza])
                centro.ensinanzas.add(ensinanza)
                print("Engadido '{} - {}' a {}".format(TIPO_ENSINANZAS[tipoensinanza], tipoensinanza, centro.nome))
                item = lista.pop(0)
                continue

            item = lista.pop(0)
            while item["class"][1] == "arbolNivel1":
                if tipoensinanza == "Bacharelato":
                    nomeensinanza = item.find("td").text
                    codtipoensinanza = 'BACA' if rexime == 'Réxime de adultos' else 'BAC'
                    ensinanza = mods.Ensinanza.objects.get_or_create(nome=nomeensinanza, tipo=codtipoensinanza)
                    centro.ensinanzas.add(ensinanza)
                    print("Engadido '{} - {}' a {}".format(codtipoensinanza, nomeensinanza, centro.nome))
                    item = lista.pop(0)
                    continue

                if tipoensinanza == 'Ensinanza de idiomas':
                    nomeensinanza = item.find("td").text
                    codtipoensinanza = 'IDI'
                    ensinanza = mods.Ensinanza.objects.get_or_create(nome=nomeensinanza, tipo=codtipoensinanza)
                    centro.ensinanzas.add(ensinanza)
                    print("Engadido '{} - {}' a {}".format(codtipoensinanza, nomeensinanza, centro.nome))
                    item = lista.pop(0)
                    continue

                if tipoensinanza == 'Ciclos formativos':
                    codgrado = TIPO_GRADO[item.find().text.lower()]
                    codtipoensinanza = 'FP'
                    item = lista.pop(0)
                    while item["class"][1] == "arbolNivel2":
                        nomeensinanza = item.find("td").text
                        ensinanza = mods.Ensinanza.objects.get_or_create(nome=nomeensinanza, grado=codgrado, tipo=codtipoensinanza)
                        centro.ensinanzas.add(ensinanza)
                        print("Engadido '{} - {}    ' a {}".format(codtipoensinanza, nomeensinanza, centro.nome))
                        item = lista.pop(0)
                        continue
                item = lista.pop(0)

    except IndexError:
        pass
    centro.save()

centros = mods.Centro.objects.all()
fst = 0
STEP = 10

while True:
    print ("{} de {}".format(fst,len(centros)))
    for index in range (fst, fst+STEP):
        print ("hola")
        try:
            centro = centros[index]
        except IndexError:
            break
        print("{} - {}".format(index,centro.nome))
        get_data_centro(centro)
    fst = fst + STEP
    if (fst > len(centros)):
        break
