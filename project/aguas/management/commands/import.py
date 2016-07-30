from django.core.management.base import BaseCommand
from aguas.models import Place

import requests
from bs4 import BeautifulSoup


def get_balneabilidade_for_area(municipio_name, municipio_id, area_id):
    """
    http://www.fatma.sc.gov.br/laboratorio/balneabilidade.php?municipio=FLORIANOPOLIS&m=2&b=77
    """
    url = 'http://www.fatma.sc.gov.br/laboratorio/balneabilidade.php?municipio'
    url += '={}&m={}&b={}'.format(municipio_name, municipio_id, area_id)
    response = requests.get(url)
    locais = []

    if response.status_code == 200:

        soup = BeautifulSoup(response.text, 'html.parser')
        lines = soup.find_all('tr')
        local = soup.find_all('b')[0].text[:-1]

        for line in lines:
            tds = line.find_all('td')
            img = tds[0].find('img')
            if img is not None:
                spot = tds[0].text[2:]
                condicao = tds[1].text
                img = str(img['onclick'])
                latitude, longitude = getLatLongFromImage(img)

                locais.append({'local': local,
                               'spot': spot,
                               'condicao': condicao,
                               'latitude': latitude,
                               'longitude': longitude})
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
        for x in range(0,220):
            baln = get_balneabilidade_for_area('FLORIANOPOLIS', 2, x)

            for i in baln:
                Place.objects.get_or_create(
                    lat=i['latitude'],
                    lon=i['longitude'],
                    place=i['local'],
                    spot=i['spot'],
                    proper=i['condicao']
                )

        print("DATA IMPORTED!")
