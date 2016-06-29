    # -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from aguas.models import Place

import requests
from bs4 import BeautifulSoup


def get_municipios(soup):
    """ returns a dict of municipios

    Args:
        soup (Beautifulsoup): the FATMA page content

    Returns:
        dict: a dict of municipios where the key is the municipio name and the
        value is the municipio id

    """

    # get 'select' tags with id == 'combo_municipio'
    combo_municipio = soup.find('select', id='combo_municipio')

    # get all 'option' tags
    combo_municipio_values = combo_municipio.find_all('option')

    municipios_index = {}
    for i in combo_municipio_values:
        municipios_index[i.text.encode('utf-8')] = i['value']

    return municipios_index


def get_municipio_areas(id_municipio):
    """ Returns a list of areas from a municipio

    Args:
        id_municipio (int): the municipio id at FATMA page

    Returns:
        dict: a dict of areas where the key is the area name and the value is
        the area id

    Note:
        The URL to request the municipio areas

        http://www.fatma.sc.gov.br/laboratorio/gravar.php?operacao=
        selecionarBalnearios&oid=2
    """
    url = "http://www.fatma.sc.gov.br/laboratorio/gravar.php?operacao=selecionarBalnearios&oid=" + str(id_municipio)

    municipio_areas = {}
    response = requests.get(url)

    if response.status_code == 200:
        list_request = response.text.split('|')

        for i in range(1, len(list_request) - 1, 2):
            area = list_request[i+1]
            area_code = list_request[i]
            municipio_areas[area] = area_code

    return municipio_areas


def get_balneabilidade_for_area(municipio_name, municipio_id, area_id):
    """
    http://www.fatma.sc.gov.br/laboratorio/balneabilidade.php?municipio=FLORIANOPOLIS&m=2&b=77
    """
    url = 'http://www.fatma.sc.gov.br/laboratorio/balneabilidade.php?municipio=%s&m=%i&b=%i' % (municipio_name, municipio_id, area_id)
    response = requests.get(url)
    locais = []

    if response.status_code == 200:

        soup = BeautifulSoup(response.text, 'html.parser')
        lines = soup.find_all('tr')

        for line in lines:
            tds = line.find_all('td')
            img = tds[0].find('img')
            if img is not None:
                local = tds[0].text
                condicao = tds[1].text
                img = str(img['onclick'])
                latitude, longitude = getLatLongFromImage(img)

                locais.append({'local' : local,
                               'condicao' : condicao,
                               'latitude' : latitude,
                               'longitude' : longitude})
    return locais


def getLatLongFromImage(stringImg):
    begin = stringImg.find('(')
    end = stringImg.find(')')

    if begin < 0 or end < 0:
        return None

    geoData = stringImg[begin+1:end]

    latitude, longitude = geoData.split(',')

    return latitude, longitude


class Command(BaseCommand):
    help = 'import data'

    def handle(self, *args, **options):
        url = 'http://www.fatma.sc.gov.br/laboratorio/dlg_balneabilidade.php'

        response = requests.get(url)
        if response.status_code != 200:
            return

        page_content = response.text

        soup = BeautifulSoup(page_content, 'html.parser')

        municipios_index = get_municipios(soup)
        floripa_id = municipios_index['FLORIANÓPOLIS']
        floripa = get_municipio_areas(2)

        baln = get_balneabilidade_for_area('FLORIANOPOLIS', 2, 77)

        for i in baln:
            Place.objects.get_or_create(
                lat=i['latitude'],
                lon=i['longitude'],
                place=i['local'],
                proper=i['condicao'] == u'PRÓPRIA'
            )

        print "DATA IMPORTED!"
