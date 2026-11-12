from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import render 
from django.contrib import messages
from django.conf import settings
from django.http import Http404
from datetime import datetime
from .middleware import Accesare
from .models import Produs
import locale

WEEK_DAY_ROMANIAN = (
	"Luni",
	"Marti",
	"Miercuri",
	"Joi",
	"Vineri",
	"Sambata",
	"Duminica"
)  

MONTH_DAY_ROMANIAN = (
	"Ianuarie",
	"Februarie",
	"Martie",
	"Aprilie",
	"Mai",
	"Iunie",
	"Iulie",
	"August",
	"Septembrie",
	"Octombrie",
	"Noiembrie",
	"Decembrie"
)

REQUESTS = 0


def trimite_email():
    send_mail(
        subject='Salutare!',
        message='Salut. Ce mai faci?',
        html_message='<h1>Salut</h1><p>Ce mai faci?</p>',
        from_email='naspa <Emanuel.Corduneanu@gmail.com>',
        recipient_list=['corduneanuemanuel1@gmail.com'],
        fail_silently=False,
    )


def index(request):
	trimite_email()
	return render(request, "aplicatie_magazin/pagina_principala.html")


def produse(request):
	produse_site = Produs.objects.select_related('categorie', 'brand').all()
	return render(request, "aplicatie_magazin/produse.html", {"produse": produse_site, "title": "Produsele noastre"})


def calculeaza_data(data = ''):
	d = datetime.now()
	
	if data == 'zi':
		return '<p>'+ d.strftime("%A %B %Y") + '</p>'
	elif data == 'timp':
		return '<p>' + d.strftime("%H:%M:%S") + '</p>'
	
	return '<p>' + d.strftime("%A %B %Y %H:%M:%S") + '</p>'


def info(request):
	# locale.setlocale(locale.LC_TIME, 'ro_RO.UTF-8')
	# curent_day = datetime.now().strftime("%A, %-d %B %Y") #.split(' ')
	# curent_day[0] = WEEK_DAY_ROMANIAN[int(curent_day[0])]
	# curent_day[2] = MONTH_DAY_ROMANIAN[int(curent_day[2])]

	# curent_day_romanian = curent_day[0] + ', ' + " ".join(curent_day[1:])

	# data_request = request.GET.get("data")
	
	request.accesare.data_accesare = calculeaza_data(request.GET.get("data"))

	html = f"""
	<!DOCTYPE html>
	<html>
		<head>
	    
	    	<title>Informatii despre server</title>
		</head>
		<body>
	    	<h1>Informatii despre server</h1>
		
			<h2>Data si ora despre server: {calculeaza_data(request.GET.get("data")) } </h2>
			
		</body>
	</html>
	"""
	return render(request, "aplicatie_magazin/info.html")



# Pagina log, exercitiu 1

def log(request):

	DEBUG = True
	if not settings.DEBUG:
		raise Http404("Pagina nu exista")

	messages.debug(request, 'Suntem in mediul debug.')	
	messages.info(request, "Site-ul este inca in functione, s-ar putea ca logging-ul sa nu functioneze cum e de dorit")
	mesaj = ''




	numar_accesari = len(Accesare.logs)

	if 'ultimele' in request.GET:
		ultimele_request = request.GET.get('ultimele')
		
		try:
			n = int(ultimele_request)
			

			if n < 0:
				messages.error(request, "Eroare, parametrul 'ultimele' trebuie sa fie pozitiv")
				mesaj = 'Eroare, parametrul "ultimele" trebuie sa fie pozitiv'
			
			elif n > numar_accesari:
				mesaj += "".join(f'<p>{str(accesare)}</p>' for accesare in Accesare.logs)
				mesaj += f'\nExista {numar_accesari} accesari fata de {n} accesari cerute.\n'
			
			else:
				mesaj += "".join(f'<p>{str(accesare)}</p>' for accesare in Accesare.logs[numar_accesari - n :])
		except:
			messages.error(request, "Eroare, nu ai introdus corect url-ul. Parametrul 'ultimele' trebuie sa fie numar intreg")
			mesaj = 'Eroare, nu ai introdus corect url-ul. Parametrul \'ultimele\' trebuie sa fie numar intreg'


	elif 'iduri' in request.GET:
		id_request = request.GET.getlist('iduri')
		DUBLURI = False
		if request.GET.get('dubluri') == 'true':
			DUBLURI = True


		lista_id = [int(x) for y in id_request for x in y.split(',')]
		try:
			if DUBLURI:

				mesaj += "".join(f'<p>{Accesare.logs[id]}</p>' for id in lista_id)	
			else:
				mesaj += "".join(f'<p>{Accesare.logs[id]}</p>' for id in list(dict.fromkeys(lista_id)))	
		except:
			mesaj += '<p>Nu exista id-ul specificat(inca)</p>'
		
	else:
		mesaj += "".join(f'<p>{str(accesare)}</p>' for accesare in Accesare.logs)

	if request.GET.get('accesari') == 'nr':
		mesaj += f'<section>Numarul de accesari pe server de pana acum: {numar_accesari}</section>\n'


	if 'detalii' in request.GET.getlist('accesari'):
		mesaj += '<h2> Detalii accesari:</h2>\n<ul>\n'

		mesaj += "\n".join(f'<li>{accesare.id}: ora {accesare.data_accesare}</li>' for accesare in Accesare.logs)
		mesaj += '</ul>\n'


		mesaj += '<section><h2>Parametrii:</h2>\n<ul>\n'
		# numar_parametri = 0
		for i, j in request.accesare.parametri.items():
			mesaj += f"<li>{i}: {j}</li>"

		mesaj += '</section>'


	if request.GET.get('tabel') == 'tot':
		mesaj += """<table border="1">\n
		<tr>
        <th>ID</th>
        <th>IP client</th>
        <th>URL</th>
        <th>Parametri</th>
        <th>Data accesare</th>
		</tr>"""
		mesaj += ''.join(f"""<tr><td>{obiect.id}</td>
        	<td>{obiect.ip_client}</td>
        	<td>{obiect.url}</td>
        	<td>{obiect.parametri}</td>
        	<td>{obiect.data_accesare}</td></tr>""" for obiect in Accesare.logs)


		mesaj += '</table>'

	elif request.GET.get('tabel'):
		try:
			parametri_map = {
				"id" : 'id',
				'ip' : 'ip_client',
				'url' : 'url',
				'data' : 'data_accesare'
			}
			lista_parametri = request.GET.get('tabel').split(',')
			mesaj += "<table border='1'>\n<thead><tr>"
			mesaj += "".join(f"<th>{str(i).upper()}</th>\n" for i in lista_parametri)
			mesaj += "</tr>\n</thead>\n<tbody>\n<tr>"		
			for accesare in Accesare.logs:
				mesaj += '<tr>'
				for i in lista_parametri:
					mesaj += f"<td>{getattr(accesare, parametri_map[i])}</td>"

				mesaj += '</tr>'
			# mesaj += ''.join(f"<td>{getattr(accesare, parametri_map[i])}</td>"  for accesare in Accesare.logs for i in lista_parametri)
			
			mesaj += '</tr>\n</tbody>\n'
			mesaj += "</table>"
		except:
			pass

	valoare_maxim_accesari = max(Accesare.counter.values())
	pagini_maxim_accesari = [x for x, y in Accesare.counter.items() if y == valoare_maxim_accesari]
	
	valoare_minim_accesari = min(Accesare.counter.values())
	pagini_minim_accesari = [x for x, y in Accesare.counter.items() if y == valoare_minim_accesari]
	
	
	mesaj += '<section><h3> Paginile cele mai putin accesate: ' + ", ".join(pagini_minim_accesari) + '</h3>'\
		+ '<h3>Paginile cele mai accesate: ' + ', '.join(pagini_maxim_accesari) + '</h3></section>' 


	
	# html = f"""
	# 			{mesaj}
				
	# 		</body>
	# 	</html>
	# 	"""
	# {mesaj}
	
	context = {
		"mesaj" : mesaj
	}
	messages.success(request, "S-au afisat informatii corespunzator.")
	return render(request, 'aplicatie_magazin/log.html', context)



def istoric(request):
	html = """
        <h1>Istoricul magazinului</h1>

        <p>Magazinul nostru a fost creat din dorinta
        de a oferi clientilor produse de calitate
        pentru reparatii si proiecte de bricolaj.</p>

        <p>Oferim o gama variata de suruburi, piulite,
        saibe si accesorii de fixare.</p>

        
    	"""

	return render(request, "pagina_principala/istoric.html")


def despre(request):
	html = """
        <h1>Despre magazinul nostru</h1>

        <section id="povestea-noastra">
            <h2>Povestea Noastra</h2>
            <p>Suntem un magazin specializat in produse
            de surubarie si bricolaj.</p>

            <p>Oferim suruburi de diferite dimensiuni,
            piulite, saibe, dibluri, scule si accesorii
            necesare pentru reparatii si constructii.</p>
        </section>

        <section id="misiune-valori">
            <h2>Misiunea si Valorile</h2>
            <p>Scopul nostru este sa ajutam clientii
            sa gaseasca produsele potrivite pentru
            proiectele lor.</p>
        </section>

       
    """

	return render(request, 'aplicatie_magazin/despre.html')


def accesare(request, id):
	if not settings.DEBUG:
			raise Http404("Pagina nu exista")
	
	messages.debug(request, 'Suntem in mediul debug.')	
	# messages.debug(request, "Acesta este un mesaj de depanare. :( ")
	messages.info(request, "Site -ul este inca in functiune :) ")

	
	try:
		id = int(id)

		rasp = ''
		if id >= len(Accesare.logs):
			messages.warning(request, "Nu incerca sa pui un id prea mare, comportament nepredictibil")
		for accesare in Accesare.logs:	
			if accesare.id == id:
				rasp = str(accesare)
				break

	except:
		messages.error(request, "Id invalid")
		

	messages.success(request, "Actiunea a avut succes! :D ")
	# messages.warning(request, "Acesta este un avertisment. :| ")

		
	return render(request, 'aplicatie_magazin/accesare.html', {'rasp' : rasp, 'titlu' : "Accesare"})




def in_lucru(request):
	PARAMS = {
		'title' : 'In lucru'

	}
	return render(request, "aplicatie_magazin/in_lucru.html", PARAMS)

	