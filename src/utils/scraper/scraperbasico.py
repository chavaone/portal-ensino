#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import codecs
import centros.models as mods

PROVINCIAS = {
    "A Coruña": "AC",
    "Lugo": "LU",
    "Ourense": "OU",
    "Pontevedra": "PO"
}

with codecs.open('utils/scraper/centros.json', "r",'utf-8') as f:
    centros = json.load(f)

for centro in centros:
    cen_obj = mods.Centro()
    cen_obj.codigo = centro["Código"]
    cen_obj.nome = centro["Nome"]
    cen_obj.enderezo = centro["Enderezo"]
    cen_obj.cp = centro["Cód. postal"]
    cen_obj.telefono = centro["Teléfono"]
    cen_obj.coorlat = centro["COORDENADA_X"]
    cen_obj.coorlon = centro["COORDENADA_Y"]
    concello,_ = mods.Concello.objects.get_or_create(
        nome=centro["Concello"],
        provincia=PROVINCIAS[centro["Provincia"]])
    cen_obj.concello = concello
    cen_obj.save()
