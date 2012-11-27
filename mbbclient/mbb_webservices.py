import sys
import urllib, urllib2, urlparse
from collections import namedtuple
from lxml import etree

WEBSERVICE_HOST = 'www.bahiablanca.gov.ar'
DEFINED_WEBSERVICES = {
    'SGRV':            'http://www.bahiablanca.gov.ar/wsMBB/sgrv_v1.asmx?WSDL',
    'compras':         'http://www.bahiablanca.gov.ar/wsMBB/compras.asmx?WSDL',
    'digesto':         'http://www.bahiablanca.gov.ar/wsMBB/digesto.asmx?WSDL',
    'aire':            'http://www.bahiablanca.gov.ar/wsMBB/aire.asmx?WSDL',
    'personal':        'http://www.bahiablanca.gov.ar/wsMBB/personal.asmx?WSDL',
    'ayudas':          'http://www.bahiablanca.gov.ar/wsMBB/ayudas.asmx?WSDL',
    'proyectosHCD':    'http://www.bahiablanca.gov.ar/wsMBB/proyectosHCD.asmx?WSDL',
    'ambiente':        'http://www.bahiablanca.gov.ar/wsMBB/ambiente.asmx?WSDL',
    'noticias':        'http://www.bahiablanca.gov.ar/wsMBB/noticias.asmx?WSDL',
    'sigemi_comercio': 'http://www.bahiablanca.gov.ar/wsMBB/sigemi_comercio1.asmx?WSDL'
}

def _optional_node(element, fallback_value=''):
    return fallback_value if len(element) == 0 else element[0]


class WebServiceMethod(namedtuple('WebServiceMethod', ('method_name', 'arguments', 'url', 'documentation'))):
    __slots__ = ()

    _result = {}

    def __call__(self, **kwargs):
        """ Retorna una secuencia de `dict` cuyas keys son los nombres de los campos """
        url = self.url + '?' + urllib.urlencode(kwargs)
        print >>sys.stderr, "REQUESTING URL: %s" % url
        return self._parseResult(urllib2.urlopen(url).read())

    def _parseResult(self, result):
        dataset = etree.fromstring(result)
        result = []
        dataset_element = dataset.xpath('//NewDataSet')
        if len(dataset_element) < 1: return []
        for row in dataset_element[0].getchildren():
            result.append(dict(map(lambda e: (e.tag, e.text), row.getchildren())))
        return result

    
def find_method_endpoint(wsdl):
    """ Retorna el endpoint (URL) para los metodos definidos en `wsdl` """
    root = etree.fromstring(wsdl)
    parsed_url = urlparse.urlparse(root.xpath('//http:address/@location',
                                               namespaces={'http': 'http://schemas.xmlsoap.org/wsdl/http/'})[0])
    return urlparse.urlunparse(urlparse.ParseResult._make(('http', WEBSERVICE_HOST) + parsed_url[2:]))


def find_methods(wsdl):
    """ Retorna los metodos definidos en `wsdl` """

    return map(lambda element:
               WebServiceMethod(method_name=element.attrib['name'][:-9],
                                 arguments=element.xpath('wsdl:part/@name', namespaces={'wsdl': 'http://schemas.xmlsoap.org/wsdl/'}),
                                 url=urlparse.urljoin(find_method_endpoint(wsdl) + '/', element.attrib['name'][:-9]),
                                 documentation=_optional_node(element.xpath("//wsdl:operation[@name='%s']/wsdl:documentation/text()" % element.attrib['name'][:-9],
                                                                            namespaces={'wsdl': 'http://schemas.xmlsoap.org/wsdl/'}))),
               etree.fromstring(wsdl).xpath("//wsdl:message[contains(@name, 'GetIn')]", namespaces={'wsdl': 'http://schemas.xmlsoap.org/wsdl/'}))
