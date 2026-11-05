from django.db import models
from decimal import Decimal
from django.db.models import Q
# Create your models here.


class Produs(models.Model):
    TIP_FILET_CHOICES = [
        ('METRIC', 'Metric'),
        ('UNC', 'UNC'),
        ('UNF', 'UNF'),
        ('BSW', 'BSW'),
        ('NPT', 'NPT'),
        ('TR', 'TR'),
    ]

    nume_produs = models.CharField(max_length=50, unique = True, null = False, error_messages = {
            'unique': 'Un produs cu acest nume exista deja',
            'max_length': 'Numele produsului nu poate depasi 50 de caractere'
            
        })
    denumire = models.CharField(max_length = 100, null = False, error_messages={
            'max_length': 'Denumirea nu poate depasi 100 de caractere',
            'blank': 'Denumirea produsului este obligatorie',
        })
    pret = models.DecimalField(max_digits = 10, decimal_places = 2, null = True, default=0,         error_messages={
            'max_digits': 'Pretul nu poate avea mai mult de 10 cifre',
            'max_decimal_places': 'Pretul poate avea maximum 2 zecimale',
            'invalid': 'Introduceti un pret valid',
        })
    stoc = models.IntegerField(default=0, error_messages={
            'invalid': 'Stocul trebuie să fie un numar intreg',
            'min_value': 'Stocul nu poate fi negativ',
        })
    diametru_mm = models.DecimalField(max_digits=10, decimal_places=2,
        null=True,
        help_text='Diametrul exterior al produsului, exprimat in milimetri',
        error_messages={
            'max_digits': 'Diametrul nu poate avea mai mult de 10 cifre',
            'invalid': 'Introduceti un diametru valid',
        }
    )
    lungime_mm = models.DecimalField(max_digits=10, decimal_places=2,
        null=True,
        help_text='Lungimea totala a produsului, exprimat in milimetri',
        error_messages={
            'max_digits': 'Lungimea nu poate avea mai mult de 10 cifre',
            'invalid': 'Introduceti o lungime valida',
        }
    )
    material = models.CharField(max_length=100, null=True, blank=True, default='Otel')
    tip_filet = models.CharField(
        max_length=100,
        choices=TIP_FILET_CHOICES,
        null=True,
        help_text='Selectati standardul filetului utilizat de produs`',
    )
    tip_cap = models.CharField(max_length=100, null=True)
    este_disponibil = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(pret__gte=0), name='pret_pozitiv'),
            models.CheckConstraint(condition=models.Q(stoc__gte=0), name='stoc_pozitiv'),
            models.CheckConstraint(condition=models.Q(diametru_mm__gt=0) | models.Q(diametru_mm__isnull=True), 
                                   name='diametru_valid'),
            models.CheckConstraint(condition=models.Q(lungime_mm__gt=0) | models.Q(lungime_mm__isnull=True),
                                   name='lungime_valida'),
        ]
    
        indexes = [
            models.Index(fields=['nume_produs'], name='index_nume_produs'),
            models.Index(fields=['pret'], name='index_pret'),
            models.Index(fields=['stoc'], name='index_stoc'),
            models.Index(fields=['este_disponibil'], name='index_disponibil'),
        ]

        verbose_name = 'Produs'
        verbose_name_plural = 'Produse'



    brand = models.ForeignKey('Brand', on_delete = models.SET_NULL, null = True, blank = True, related_name='produse')
    ambalaj = models.ForeignKey('Ambalaj', on_delete = models.SET_NULL, null=True, related_name='produse')
    categorie = models.ForeignKey('Categorie', on_delete = models.SET_NULL, null=True, related_name='produse')



    furnizori = models.ManyToManyField('Furnizor', related_name='produse')
    raioane = models.ManyToManyField('Raion', related_name='produse')
    evenimente_promotionale = models.ManyToManyField('EvenimentPromotional', related_name='produse')

    imagine = models.ImageField(upload_to='images/', null=True, blank=True)


    def __str__(self):
        return self.nume_produs


class Raion(models.Model):
    denumire = models.CharField(max_length=100, unique=True)
    descriere = models.TextField(null=True, blank=True)
    etaj = models.PositiveIntegerField()
    pozitie = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(etaj__gte = 0), name = 'etaj_valid'),
        ]
        verbose_name = 'Raion'
        verbose_name_plural = 'Raioane'


    sediu_companie = models.ForeignKey('SediuCompanie', on_delete = models.CASCADE, related_name = 'raioane')

    def __str__(self):
        return f"{self.denumire} - Etajul {self.etaj}"



class Ambalaj(models.Model):
    MARIME_CHOICES = [
        ('S', 'Mic'),
        ('M', 'Mediu'),
        ('L', 'Mare'),
        ('XL', 'Foarte mare'),
    ]

    denumire = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    marime = models.CharField(max_length=2, choices=MARIME_CHOICES)
    este_reciclabil = models.BooleanField(default=False)


    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(marime__in=['S', 'M', 'L', 'XL']),
                                   name='marime_ambalaj_valida'),
        ]
        verbose_name = 'Ambalaj'
        verbose_name_plural = 'Ambalaje'



    def __str__(self):
        return f"{self.denumire} ({self.get_marime_display()})"


class SediuCompanie(models.Model):
    denumire = models.CharField(max_length=200)
    adresa = models.CharField(max_length=255)
    oras = models.CharField(max_length=100)
    telefon = models.CharField(max_length=20)
    program = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Sediu companie'
        verbose_name_plural = 'Sedii companie'

    def __str__(self):
        return f"{self.denumire} - {self.oras}"


class EvenimentPromotional(models.Model):
    denumire = models.CharField(max_length=200)
    descriere = models.TextField(null=True, blank=True)
    data_inceput = models.DateTimeField(auto_now_add=True)
    data_sfarsit = models.DateTimeField()
    buget = models.DecimalField(max_digits=12, decimal_places=2)
    este_activ = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(data_sfarsit__gt=models.F('data_inceput')),
                                name='data_sfarsit_dupa_inceput'),
            models.CheckConstraint(condition=models.Q(buget__gte=0),
                                name='buget_pozitiv'),
        ]    
        verbose_name = 'Eveniment promoțional'
        verbose_name_plural = 'Evenimente promoționale'

    def __str__(self):
        return f"{self.denumire} ({self.data_inceput.strftime('%d.%m.%Y')})"



class Furnizor(models.Model):
    nume = models.CharField(max_length=200)
    email = models.EmailField()
    telefon = models.CharField(max_length=20)
    adresa = models.CharField(max_length=255)
    termen_estimativ_livrare = models.PositiveIntegerField(
        help_text='Numarul estimat de zile lucrătoare pana la livrare',
    )

    class Meta:
        ordering = ['nume']
        constraints = [
        models.CheckConstraint(condition=models.Q(termen_estimativ_livrare__gt=0),
                               name='termen_livrare_valid'),
        ]
        verbose_name = 'Furnizor'
        verbose_name_plural = 'Furnizori'



    def __str__(self):
        return self.nume
    


class Brand(models.Model):
    nume = models.CharField(max_length=200)
    descriere = models.TextField(null=True, blank=True)
    tara_origine = models.CharField(max_length=100)
    website = models.URLField(
        help_text='Adresa web oficiala a brandului',
    )

    class Meta:
        ordering = ['nume']
        verbose_name = 'Brand'
        verbose_name_plural = 'Branduri'


    def __str__(self):
        return f"{self.nume} - {self.tara_origine}"





class Categorie(models.Model):
    nume = models.CharField(max_length=200)
    culoare = models.CharField(max_length=100)
    sigla = models.CharField(max_length=255)
    descriere = models.TextField(null=True, blank=True)


    class Meta:
        verbose_name = 'Categorie'
        verbose_name_plural = 'Categorii'
    
    def __str__(self):
        return self.nume
