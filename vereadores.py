#!/usr/bin/python
# -*- encoding: utf-8 -*-
import re

import requests
from bs4 import BeautifulSoup
from docopt import docopt
from rows import fields, Table, export_to_xlsx
from collections import OrderedDict
from brasil import BrasilIO


URL_CAMARA = "http://www.camara.rj.gov.br/vereador_informacoes.php?m1=inform&cvd={id}"
URL_FRENTES = "http://www.camara.rj.gov.br/vereador_interna_frente.php?cvd={id}"
URL_VOTACOES = "http://www.camara.rj.gov.br/vereador_votacao.php?&cvd={id}"
URL_MANDATOS = "http://www.camara.rj.gov.br/vereador_interna_mandatos.php?cvd={id}"


IDS_CPFS=[l.strip() for l in open("ids_cpfs.txt").readlines()]

regex="<li><b>(.+?)( - |: )</b>(.+?)</li>"
pattern=re.compile(regex)

if __name__ == '__main__':
    api = BrasilIO()

    vereadores = Table(fields=OrderedDict([
       ("Nome civil", fields.TextField),
       ("Data de nascimento", fields.TextField),
       ("Partido", fields.TextField),
       ("Naturalidade", fields.TextField),
       ("Endereço", fields.TextField),
       ("Blog", fields.TextField),
       ("Facebook", fields.TextField),
       ("Instagram", fields.TextField),
       ("Twitter", fields.TextField),
       ("Frentes", fields.TextField),
       ("Votações", fields.TextField),
       ("Mandatos", fields.TextField),
       ("Docs BrasilIO", fields.TextField),
       ("Sócios BrasilIO", fields.TextField),
    ]))

    def pegar_dados_da_camara_municipal(id_ver, row_ver):
        response = requests.get(URL_CAMARA.format(id=id_ver))
        html = response.content
        if not response.status_code == requests.codes.OK:
           raise ConnectionError(u'An error was occoured while trying to get  id: {}'.format(id_ver))
        soup = BeautifulSoup(html, 'html.parser')
        div_dados = soup.find(attrs={"class": "vereainterna"})
        itens_dados = list(div_dados.find('ul').find_all('li'))

        def parse_data(data):
            link_regex = '<a [^>]*>(.+?)</a>'
            link_pattern = re.compile(link_regex)

            match = link_pattern.match(data)
            if match:
               return match.group(1)
            else:
               return data

        for item in itens_dados:
            match = pattern.match(str(item))
            if match:
               row_ver[fields.slug(match.group(1))] = parse_data(match.group(3))

        row_ver["frentes"] = URL_FRENTES.format(id=id_ver)
        row_ver["votacoes"] = URL_VOTACOES.format(id=id_ver)
        row_ver["mandatos"] = URL_MANDATOS.format(id=id_ver)

    def pegar_dados_do_brasilio(cpf_ver, row_ver):
        try:
            data = api.dataset_table_data("documentos-brasil", 'documents', document_type='CPF', document=cpf_ver)
            result = list(data)
            row_ver['docs_brasilio'] = result[0]['sources']
        except:
            row_ver['docs_brasilio'] = ''

        data = api.dataset_table_data("socios-brasil", 'socios', search="\"{}\"".format(row_ver['nome_civil'].strip()))
        result = list(data)
        row_ver['socios_brasilio'] = ' /// '.join([r['cnpj'] + ' ' + r['razao_social'] + ' (' + r['qualificacao_socio'] + ')' for r in result])

    for id_ver, cpf_ver in map(lambda i: i.strip().split('\t'), IDS_CPFS):
        row_ver = {}
        pegar_dados_da_camara_municipal(id_ver, row_ver)
        pegar_dados_do_brasilio(cpf_ver, row_ver)
        vereadores.append(row_ver)


    export_to_xlsx(vereadores, "vereadores.xlsx")
