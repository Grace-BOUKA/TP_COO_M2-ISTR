# Register your models here.

from django.contrib import admin

from . import models

admin.site.register(models.QuantiteProduit)
admin.site.register(models.QuantiteMachine)
admin.site.register(models.PointDeVente)
admin.site.register(models.Lieu)
admin.site.register(models.PrixProduit)
admin.site.register(models.Operation)
admin.site.register(models.Machine)
admin.site.register(models.Ville)
admin.site.register(models.Facture)
admin.site.register(models.Fournisseur)
admin.site.register(models.Pays)
admin.site.register(models.Stock)
admin.site.register(models.Transport)
admin.site.register(models.Produit)
