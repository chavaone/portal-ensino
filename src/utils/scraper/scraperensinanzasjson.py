#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import centros.models as mods

def infantil (centro_django, ensinanza_cont):
    ensinanza,_ = mods.Ensinanza.objects.get_or_create(
        nome="Educación Infantil",
        tipo='INF')
    centro_django.ensinanzas.add(ensinanza)

def primaria (centro_django, ensinanza_cont):
    ensinanza,_ = mods.Ensinanza.objects.get_or_create(
        nome="Educación Primaria",
        tipo='PRI')
    centro_django.ensinanzas.add(ensinanza)

def eso (centro_django, ensinanza_cont):
    ensinanza,_ = mods.Ensinanza.objects.get_or_create(
        nome="Educación Superior Obrigatoria",
        tipo='ESO')
    centro_django.ensinanzas.add(ensinanza)

def esa (centro_django, ensinanza_cont):
    ensinanza,_ = mods.Ensinanza.objects.get_or_create(
        nome="Educación Secundaria para Adultos/as",
        tipo='ESA')
    centro_django.ensinanzas.add(ensinanza)

def bac (centro_django, ensinanza_cont):
    if "artes" in ensinanza_cont:
        ensinanza,_ = mods.Ensinanza.objects.get_or_create(
            nome="Bacharelato - Artes",
            tipo='BAC')
        centro_django.ensinanzas.add(ensinanza)
    if "humanidades" in ensinanza_cont:
        ensinanza,_ = mods.Ensinanza.objects.get_or_create(
            nome="Bacharelato - Humanidades",
            tipo='BAC')
        centro_django.ensinanzas.add(ensinanza)
    if "ciencias" in ensinanza_cont:
        ensinanza,_ = mods.Ensinanza.objects.get_or_create(
            nome="Bacharelato - Ciencias",
            tipo='BAC')
        centro_django.ensinanzas.add(ensinanza)

def fp (centro_django, ensinanza_cont):
    try:
        for ciclos in ensinanza_cont["superior"]:
            ensinanza,_ = mods.Ensinanza.objects.get_or_create(
                nome=ciclo,
                tipo='FP',
                grado='S')
            centro_django.ensinanzas.add(ensinanza)
    except:
        pass
    try:
        for ciclo in ensinanza_cont["básica"]:
            ensinanza,_ = mods.Ensinanza.objects.get_or_create(
                nome=ciclo,
                tipo='FP',
                grado='B')
            centro_django.ensinanzas.add(ensinanza)
    except:
        pass
    try:
        for ciclos in ensinanza_cont["medio"]:
            ensinanza,_ = mods.Ensinanza.objects.get_or_create(
                nome=ciclo,
                tipo='FP',
                grado='M')
            centro_django.ensinanzas.add(ensinanza)
    except:
        pass

def musica (centro_django, ensinanza_cont):
    if not ensinanza_cont:
        ensinanza,_ = mods.Ensinanza.objects.get_or_create(
            nome="Ensinanzas de Música",
            tipo='MUS')
        centro_django.ensinanzas.add(ensinanza)
        return
    try:
        for instrumento in ensinanza_cont["mus-med"]:
            ensinanza,_ = mods.Ensinanza.objects.get_or_create(
                nome=instrumento,
                tipo='MUS',
                grado='M')
            centro_django.ensinanzas.add(ensinanza)
    except:
        pass
    try:
        for instrumento in ensinanza_cont["mus-sup"]:
            ensinanza,_ = mods.Ensinanza.objects.get_or_create(
                nome=instrumento,
                tipo='MUS',
                grado='S')
            centro_django.ensinanzas.add(ensinanza)
    except:
        pass

def especial (centro_django, ensinanza_cont):
    ensinanza,_ = mods.Ensinanza.objects.get_or_create(
        nome="Educación Especial",
        tipo='ESP')
    centro_django.ensinanzas.add(ensinanza)


def idiomas (centro_django, ensinanza_cont):
    for idioma in ensinanza_cont:
        ensinanza,_ = mods.Ensinanza.objects.get_or_create(
            nome=idioma,
            tipo='IDI')
        centro_django.ensinanzas.add(ensinanza)

def danza (centro_django, ensinanza_cont):
    if not ensinanza_cont:
        ensinanza,_ = mods.Ensinanza.objects.get_or_create(
            nome="Ensinanzas de Danza",
            tipo='DAN')
        centro_django.ensinanzas.add(ensinanza)
    else:
        for tipo_danza in ensinanza_cont:
            ensinanza,_ = mods.Ensinanza.objects.get_or_create(
                nome=tipo_danza,
                tipo='DAN')
            centro_django.ensinanzas.add(ensinanza)

def artedramatico (centro_django, ensinanza_cont):
    if not ensinanza_cont:
        ensinanza,_ = mods.Ensinanza.objects.get_or_create(
            nome="Ensinanzas de Arte Dramático",
            tipo='ARDR')
        centro_django.ensinanzas.add(ensinanza)
    else:
        for tipo_arte in ensinanza_cont:
            ensinanza,_ = mods.Ensinanza.objects.get_or_create(
                nome=tipo_arte,
                tipo='ARDR')
            centro_django.ensinanzas.add(ensinanza)

def desenho (centro_django, ensinanza_cont):
    try:
        for arte in ensinanza_cont["med"]:
            ensinanza,_ = mods.Ensinanza.objects.get_or_create(
                nome=arte,
                tipo='ARDE',
                grado='M')
            centro_django.ensinanzas.add(ensinanza)
    except:
        pass
    try:
        for arte in ensinanza_cont["sup"]:
            ensinanza,_ = mods.Ensinanza.objects.get_or_create(
                nome=arte,
                tipo='ARDE',
                grado='S')
            centro_django.ensinanzas.add(ensinanza)
    except:
        pass

def ebi (centro_django, ensinanza_cont):
    ensinanza,_ = mods.Ensinanza.objects.get_or_create(
        nome="Ensinanzas Básicas Iniciais",
        tipo='EBI')
    centro_django.ensinanzas.add(ensinanza)

def none (centro_django, ensinanza_cont):
    pass

switcher = {
    "prof-art-des": desenho,
    "inf": infantil,
    "prim": primaria,
    "eso": eso,
    "esa": esa,
    "bac": bac,
    "esp": especial,
    "fp": fp,
    "ebi": ebi,
    "mus": musica,
    "idiomas": idiomas,
    "danza": danza,
    "drama": artedramatico,
    "sup-desenho": none,
    "prog-formativos": none,
    "deportivas": none,
    "conservacion": none
}

with open("static/db.json", "r") as json_file:
    file_txt = json_file.read()
    centros = json.loads(file_txt)

for index,centro in enumerate(centros):
    print ("%i de %i - %s" % (index, len(centros), centro["nome"]))
    django_center = mods.Centro.objects.filter(codigo=centro["cod"]).first()
    for ensinanza in centro["ensinanzas"]:
        func = switcher[ensinanza]
        cont_ensinanza = centro["ensinanzas"][ensinanza]
        func(django_center, cont_ensinanza)
