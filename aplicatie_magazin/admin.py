from django.contrib import admin
from django.core import serializers
from django.http import HttpResponse
from django.utils.html import format_html
from .models import Produs, Ambalaj, Brand, Furnizor, Raion, SediuCompanie, Categorie, EvenimentPromotional


admin.site.site_title = 'Administrare Magazin'
admin.site.site_header = 'Administrarea Magazinului Online'
admin.site.index_title = 'Panoul de administrare al magazinului'
admin.site.site_url = '/aplicatie_magazin/'


class ProdusAdmin(admin.ModelAdmin):
    list_display = ('nume_produs_formatat', 'brand_nume', 'categorie', 'pret', 'stoc', 'este_disponibil')
    ordering = ('nume_produs',)
    list_per_page = 5
    list_filter = ('este_disponibil', 'brand', 'categorie')
    search_fields = ('nume_produs', 'denumire')
    search_help_text = 'Cautati dupa numele sau denumirea produsului.'
    fieldsets = (
        ('Date principale', {
            'fields': ('nume_produs', 'denumire', 'pret', 'stoc', 'este_disponibil',
                        'brand', 'ambalaj', 'categorie', 'furnizori', 'raioane', 'evenimente_promotionale'),
        }),
        ('Caracteristici optionale', {
            'fields': ('diametru_mm', 'lungime_mm', 'material', 'tip_filet', 'tip_cap', 'imagine'),
            'classes': ('collapse',),
        })
    )
    actions = ['exporta_produse_json', 'marcheaza_disponibile']

    @admin.action(description='Exporta produsele selectate in format JSON')
    def exporta_produse_json(self, request, queryset):
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="produse.json"'
        serializers.serialize('json', queryset, stream=response)
        return response

    @admin.action(description='Marcheaza produsele selectate ca disponibile')
    def marcheaza_disponibile(self, request, queryset):
        produse_actualizate = queryset.update(este_disponibil=True)
        self.message_user(request, f'{produse_actualizate} produs(e) au fost marcate ca disponibile.')

    @admin.display(description='Nume produs', ordering='nume_produs')
    def nume_produs_formatat(self, obj):
        return format_html('<b style="color: cyan;">{}</b>', obj.nume_produs)

    @admin.display(description='Brand', ordering='brand__nume')
    def brand_nume(self, obj):
        return obj.brand.nume


class AmbalajAdmin(admin.ModelAdmin):
    search_fields = ('denumire', 'material')
    search_help_text = 'Cautati dupa denumirea sau materialul ambalajului'



class BrandAdmin(admin.ModelAdmin):
    search_fields = ('nume', 'tara_origine')
    search_help_text = 'Cautati dupa numele brandului sau tara de origine'


class FurnizorAdmin(admin.ModelAdmin):
    search_fields = ('nume', 'email')
    search_help_text = 'Cautati dupa numele sau adresa de email a furnizorului'


class RaionAdmin(admin.ModelAdmin):
    search_fields = ('denumire', 'pozitie')
    search_help_text = 'Cautati dupa denumirea sau pozitia raionului'



class SediuCompanieAdmin(admin.ModelAdmin):
    search_fields = ('denumire', 'adresa')
    search_help_text = 'Cautati dupa denumirea sau adresa sediului'



class CategorieAdmin(admin.ModelAdmin):
    search_fields = ('nume', 'sigla')
    search_help_text = 'Cautati dupa numele sau sigla categoriei'


class EvenimentPromotionalAdmin(admin.ModelAdmin):
    search_fields = ('denumire', 'descriere')
    search_help_text = 'Cautati dupa denumirea sau descrierea evenimentului'


admin.site.register(Produs, ProdusAdmin)
admin.site.register(Ambalaj, AmbalajAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Furnizor, FurnizorAdmin)
admin.site.register(Raion, RaionAdmin)
admin.site.register(SediuCompanie, SediuCompanieAdmin)
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(EvenimentPromotional, EvenimentPromotionalAdmin)