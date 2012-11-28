# coding: utf-8
import sys
import urllib2
import csv
import json
from itertools import ifilter

import cmdln
import mbb_webservices
from utils import memoize


ALLOWED_FORMATS = ('CSV', 'JSON')

class MBBClient(cmdln.Cmdln):
    """Uso:
        mbb_client SUBCOMANDO [ARGS...]
        mbb_client help SUBCOMANDO

    ${command_list}
    ${help_list}
    """

    name = 'mbbclient'

    _webservice_methods_cache = {}

    def __init__(self, *args, **kwargs):
        cmdln.Cmdln.__init__(self, *args, **kwargs)
        cmdln.Cmdln.do_help.aliases.append("h")

    def _available_webservices(self):
        return mbb_webservices.DEFINED_WEBSERVICES.keys()


    def _webservice_methods(self, webservice):
        assert(webservice in mbb_webservices.DEFINED_WEBSERVICES.keys())

        return mbb_webservices.find_methods(urllib2.urlopen(mbb_webservices.DEFINED_WEBSERVICES[webservice]).read())

    webservice_methods = memoize(_webservice_methods, _webservice_methods_cache, 1)

    def do_list(self, subcmd, opts, *args):
        """ Imprimir los web services disponibles """
        print '\n'.join(self._available_webservices())

    def do_info(self, subcmd, opts, *args):
        """ Imprimir información sobre un webservice (descripción, métodos disponibles, etc) """
        def print_usage_and_exit():
            print "Uso %s info <web_service>" % self.name
            print "Web services disponibles:"
            print '\n'.join(map(lambda ws: '\t%s' % ws, self._available_webservices()))
            return 1
        
        if len(args) != 1 or args[0] not in self._available_webservices(): print_usage_and_exit()

        methods = self.webservice_methods(args[0])
        
        print "Métodos disponibles en el webservice `%s`" % args[0]
        print
        for method in methods:
            print method.method_name
#            import pdb; pdb.set_trace()
            print "     Descripcion: %s" % (unicode(method.documentation).encode('utf-8') if method.documentation != '' else '<sin documentacion>')
            print "      Argumentos: %s" % ', '.join(method.arguments)
            print

    @cmdln.option('-f', '--format', metavar='FORMAT', help='Formato de salida de los datos (%s). Default: CSV' % ', '.join(ALLOWED_FORMATS), default='CSV')
    @cmdln.option('-o', '--output', metavar='OUTPUT', help="Destino de la salida. Nombre de archivo o '-' para stdout. Default: stdout", default='-')
    def do_call(self, subcmd, opts, *args):
        """Llama a un método de un webservice

           Uso: call <web_service> <method> [arg=val ...]

           ${cmd_option_list}
        """ 

        def print_usage():
            print "Uso: call <web_service> <method> [arg=val ...]" % (self.name)

        if len(args) < 2:
            print_usage()
            return 1
        
        web_service = args[0]
        if web_service not in self._available_webservices():
            print "El webservice `%s` no existe" % web_service
            print "Web services disponibles:"
            print '\n'.join(map(lambda ws: '\t%s' % ws, self._available_webservices()))
            return 1

        method = next(ifilter(lambda m: m.method_name == args[1], self.webservice_methods(web_service)))
        if method is None:
            print "El webservice `%s` no contiene al método `%s`" % (web_service, method)
            print "Métodos disponibles:"
            for method in self.webservice_methods(web_service):
                print "%20s args: %s" % (method.method_name, ', '.join(method.arguments))

            return 1

        if set(method.arguments) != set(map(lambda a: a.split('=')[0], args[2:])):
            print "Parámetros incorrectos para el método `%s`" % method.method_name
            return 1

        if opts.format not in ALLOWED_FORMATS:
            print "Formato desconocido. Formatos válidos: " + ', '.join(ALLOWED_FORMATS)
            return 1

        # ahora si, llamo al método
        ws_result = method(**dict(map(lambda a: a.split('='), args[2:])))
        
        output_stream = sys.stdout if opts.output == '-' else open(opts.output, 'wb')

        if opts.format == 'CSV':
            if len(ws_result) < 1: return 0
            writer = csv.DictWriter(output_stream, ws_result[0].keys())
            writer.writer.writerow(ws_result[0].keys())
            for row in ws_result:
                writer.writerow(dict(zip(row.keys(), map(lambda v: v.encode('utf-8') if type(v) == unicode else v, row.values()))))
        elif opts.format == 'JSON':
            json.dump(ws_result, output_stream)

        output_stream.close()

def main():
    mbb_client = MBBClient()
    sys.exit(mbb_client.main())



        
