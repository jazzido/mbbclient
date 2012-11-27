mbbclient
=========

`mbbclient` es un cliente para consumir los *web services* que publica
la [Municipalidad de Bahía Blanca](http://www.bahiablanca.gov.ar)

## Instalación

    $ pip install git+https://github.com/jazzido/mbbclient.git
    
Si no tenés `pip`, bajá el contenido de este repositorio y ejecutá

    $ python setup.py install
    
## Ejemplo de uso

    $ mbbclient
    Uso:
        mbbclient SUBCOMANDO [ARGS...]
        mbbclient help SUBCOMANDO

    Commands:
        call           Llama a un método de un webservice
        help (?, h)    give detailed help on a specific sub-command
        info           Imprimir información sobre un webservice (descripción,...
        list           Imprimir los web services disponibles
        
Para obtener la lista de los webservices disponibles:

     $ mbbclient list
     digesto
     noticias
     aire
     personal
     proyectosHCD
     SGRV
     sigemi_comercio
     ambiente
     compras
     ayudas

Métodos disponibles en un *webservice*:

    $ mbbclient info ambiente
    Métodos disponibles en el webservice `ambiente`
    
             Indicadores args: Key, IDPrograma, IDIndicador, AnioDesde, AnioHasta
    IndicadoresResumenAnual args: Key, IDPrograma, IDIndicador, AnioDesde, AnioHasta
                Empresas args: Key
          ActassEmpresas args: Key, FechaDesde, FechaHasta, CodigoEmpresa
               Denuncias args: Key, FechaDesde, FechaHasta

Para invocar un método de un *webservice*:

    $ mbbclient call --format=JSON -o /tmp/proveedores.json compras
    PadronProveedores Key=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    
El comando anterior consulta al método `PadronProveedores` del
*webservice* `compras`. Guarda los resultados en formato JSON dentro
del archivo `/tmp/proveedores.json`

El comando `call` acepta opciones para modificar el formato y destino
de la salida:

    $ mbbclient help call 
    Llama a un método de un webservice
    
    Uso: call <web_service> <method> [arg=val ...]
    
    Options:
        -h, --help          show this help message and exit
        -o OUTPUT, --output=OUTPUT
                            Destino de la salida. Nombre de archivo o '-' para
                            stdout. Default: stdout
        -f FORMAT, --format=FORMAT
                            Formato de salida de los datos (CSV, JSON). Default:
                            CSV
                            
