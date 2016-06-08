from bs4 import BeautifulSoup
import urllib2


def get_municipio_areas(id_municipio):
	"""
	http://www.fatma.sc.gov.br/laboratorio/gravar.php?operacao=selecionarBalnearios&oid=2
	"""
	query = 'http://www.fatma.sc.gov.br/laboratorio/gravar.php?operacao=selecionarBalnearios&oid=' + str(id_municipio)
	request = urllib2.urlopen(query).read()

	return request

def get_balneabilidade_for_municipio(municipio_name, municipio_id, area_id):
	"""
	http://www.fatma.sc.gov.br/laboratorio/balneabilidade.php?municipio=FLORIANOPOLIS&m=2&b=77
	"""
	query = 'http://www.fatma.sc.gov.br/laboratorio/balneabilidade.php?municipio=%s&m=%i&b=%i' % (municipio_name, municipio_id, area_id)
	request = urllib2.urlopen(query).read()

	soup = BeautifulSoup(request, 'html.parser')
	lines = soup.find_all('tr')

	for line in lines:
		tds = line.find_all('td')
		img = tds[0].find('img')
		font = tds[1].text
		print 'LINE: ', line
		print 'IMG: ', img
		print 'FONT: ', font
		# print 'onClick: ', img.onclick
		print


if __name__ == "__main__":
	# site urls
	fatma_link = 'http://www.fatma.sc.gov.br/laboratorio/dlg_balneabilidade.php'
	v2 = 'http://www.fatma.sc.gov.br/laboratorio/gravar.php?operacao=selecionarBalnearios&oid=2'

	# request info from site and read as str
	request = urllib2.urlopen(fatma_link)
	page_content = request.read()

	#
	soup = BeautifulSoup(page_content, 'html.parser')

	#
	combo_municipio = soup.find('select', id='combo_municipio')

	#
	combo_municipio_values = combo_municipio.find_all('option')

	# Get 
	municipios_index = dict()
	for i in combo_municipio_values:
		print i
		print i.text
		print i['value']
		municipios_index[i.text] = i['value']


	floripa = get_municipio_areas(2)
	print floripa

	baln = get_balneabilidade_for_municipio('FLORIANOPOLIS', 2, 77)
