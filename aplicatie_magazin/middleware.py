from datetime import datetime
from django.utils.http import urlencode
from urllib.parse import urlparse
import locale


class Accesare:
    last_id = 0
    logs = []

    counter = {}


    def __init__(self, ip_client, url, parametri = None):

        self.id = Accesare.last_id
        Accesare.last_id += 1
        self.ip_client = ip_client
        self.url = url 
        self.parametri = {}
        self.data_accesare = self.calculeaza_data()
        
        for i in parametri:
            self.parametri[i[0]] = i[1]
        self.data = datetime.now()
        Accesare.logs.append(self)
        print(self.parametri)
        print("Pagina este:" + str(self.pagina()))

        Accesare.counter[self.pagina()] = Accesare.counter.get(self.pagina(), 0) + 1


    def __str__(self):
        return f"""
            id: {self.id}
            ip_client: {self.ip_client}
            string_url: {self.string_url()}
            pagina: {self.pagina()}
            data_accesare: {self.data_accesare}
            lista_parametri: {self.lista_parametri()}
            """

    
    def __iter__(self):
        return iter(Accesare.logs)



    def lista_parametri(self):
        return [(i, j) for i, j in self.parametri.items()]

    def string_url(self):
        if not self.parametri:
            return self.url

        query_string = urlencode(self.parametri)

        return self.url + '?' + query_string   


        
    def pagina(self):
        path = urlparse(self.url).path
        return path.split('/')[-2] + '/' if path else '/'
    
    def calculeaza_data(self, format = "%A %B %Y %H:%M:%S"):
        locale.setlocale(locale.LC_TIME, 'ro_RO.UTF-8')
        return datetime.now().strftime(format)

    def get_ip(request):
        req_headers = request.META
        str_lista_ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if str_lista_ip:
            return str_lista_ip.split(',')[-1].strip()
        else:
            return request.META.get('REMOTE_ADDR')

    def get_url(self):
        return self.url

    def get_parametri(self):
        return self.parametri

    def data(self):
        return self.data_accesare


class Middleware_accesarePagina:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        accesare = Accesare(Accesare.get_ip(request), request.path, request.GET.lists())
        request.accesare = accesare
        
        response = self.get_response(request)      


        print(accesare)
        # print(accesare.calculeaza_data())
        # print(accesare.ip_client)

        
        

        return response

