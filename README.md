# sc_aguas

O projeto SC Águas disponibiliza uma API, a fim de facilitar o acesso aos dados de qualidade das águas em todo o Estado de Santa Catarina.

## Requirements

O **SC Águas** pode ser executado em diversas distribuições de SO, utilizando as seguintes dependências:
* [Bs4](https://pypi.python.org/pypi/bs4/0.0.1)  == 0.0.1
* [Django](https://www.djangoproject.com/) == 1.9.7
* [Djangorestframework](http://www.django-rest-framework.org/) == 3.3.3
* [Git](http://git-scm.com/)
* [Python](https://www.python.org/) >= 3
* [Pip](http://www.pip-installer.org/en/latest/)
* [Virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/)

## Configuração de Ambiente

#### **Virtualenv**
Mapeamento das libs Python3 pelo virtualenvwrapper.
```
$ sudo pip install virtualenvwrapper
$ export WORKON_HOME=$HOME/.virtualenvs
$ export PROJECT_HOME=$HOME/devel
$ . /usr/local/bin/virtualenvwrapper.sh
```
Pode ser inserido esses comandos no arquivo *bashrc* do sistema.

#### **Instalando todas as dependências**

```
$ mkvirtualenv sc-aguas -p /usr/bin/python3
$ pip install -r requirements.txt
```

## Importando os Dados
```
$ python project/manage.py import
```


## Executando a API
```
$ python project/manage.py migrate
$ python project/manage.py runserver
```
Após subir o Django, verifique na porta 8000:
*http://localhost:8000/*
