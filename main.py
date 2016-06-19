# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2


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

    # populate the dict
    municipios_index = dict()
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
    query = "http://www.fatma.sc.gov.br/laboratorio/gravar.php?operacao=selecionarBalnearios&oid=" + str(id_municipio)
               
    print('QUERY: ', query)               
               
    request = urllib2.urlopen(query).read()
    
    list_request = str.split(request, '|')

    municipio_areas = dict()    
    for i in range(1, len(list_request) - 1, 2):
        area = list_request[i+1]
        area_code = list_request[i] 
        municipio_areas[area] = area_code

    return municipio_areas


def get_balneabilidade_for_area(municipio_name, municipio_id, area_id):
    """
    http://www.fatma.sc.gov.br/laboratorio/balneabilidade.php?municipio=FLORIANOPOLIS&m=2&b=77
    """
    query = 'http://www.fatma.sc.gov.br/laboratorio/balneabilidade.php?municipio=%s&m=%i&b=%i' % (municipio_name, municipio_id, area_id)
    request = urllib2.urlopen(query).read()

    soup = BeautifulSoup(request, 'html.parser')
    lines = soup.find_all('tr')

    locais = list() 
    for line in lines:
        tds = line.find_all('td')
        img = tds[0].find('img')       
        if img is not None:
            local = tds[0].text
            condicao = tds[1].text.encode('utf-8')        
            img = str(img['onclick'])
            latitude, longitude = getLatLongFromImage(img)            
            
            print('LOCAL: ', local)
            print('CONDICAO: ', condicao)
            print('LATITUDE: ', latitude) 
            print('LONGITUDE: ', longitude)
            
            locais.append({'local' : local,
                           'condicao' : condicao,
                           'latitude' : latitude,
                           'longitude' : longitude})
    return locais
            
            
            
def getLatLongFromImage(stringImg):
    """
    
    """
    begin = stringImg.find('(')
    end = stringImg.find(')')
    
    if begin < 0 or end < 0:
        return None
    
    geoData = stringImg[begin+1:end]
    
    latitude, longitude = geoData.split(',')    
    
    return latitude, longitude

if __name__ == "__main__":
    # site urls
    fatma_link = 'http://www.fatma.sc.gov.br/laboratorio/dlg_balneabilidade.php'
    
    # request info from site and read as str
    request = urllib2.urlopen(fatma_link)
    page_content = request.read()

    #
    soup = BeautifulSoup(page_content, 'html.parser')

    # Get
    municipios_index = get_municipios(soup)
    for i in municipios_index:
        print(i)

    floripa_id = municipios_index['FLORIANÓPOLIS']
    floripa = get_municipio_areas(2)
    print(floripa)

    baln = get_balneabilidade_for_area('FLORIANOPOLIS', 2, 77)
    
    for i in baln:
        print i
