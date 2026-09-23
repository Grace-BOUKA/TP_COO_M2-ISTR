# Create your models here.
from django.db import models


class Pays(models.Model):
    nom = models.CharField(max_length=100)
    tva = models.IntegerField()
    tarif_electrique = models.IntegerField()


class Ville(models.Model):
    nom = models.CharField(max_length=100)
    taxe_immobiliere = models.IntegerField()
    prix_m2 = models.IntegerField()
    pays = models.ForeignKey(
        Pays,
        on_delete=models.PROTECT,
    )


class Machine(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.IntegerField()
    duree_de_vie = models.IntegerField()
    cout_maintenance = models.IntegerField()
    superfice = models.IntegerField()


class QuantiteMachine(models.Model):
    machine = models.ForeignKey(
        Machine,
        on_delete=models.PROTECT,
    )
    nombre = models.IntegerField()


class Lieu(models.Model):
    nom = models.CharField(max_length=100)
    ville = models.ForeignKey(
        Ville,
        on_delete=models.PROTECT,
    )
    superficie = models.IntegerField()
    quantite_machines = models.ManyToManyField(QuantiteMachine)
    consommation_electrique = models.IntegerField()


class Transport(models.Model):
    nombre_palettes = models.IntegerField()
    cout = models.IntegerField()
    delai = models.IntegerField()
    depart = models.ForeignKey(
        Lieu,
        on_delete=models.PROTECT,
    )
    arrivee = models.ForeignKey(
        Ville,
        on_delete=models.PROTECT,
    )


class Operation(models.Model):
    nom = models.CharField(max_length=100)
    Operation_suivante = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
    )
    cout = models.IntegerField()
    machine = models.ForeignKey(
        Machine,
        on_delete=models.PROTECT,
    )

    quantite_produits = models.ManyToManyField("QuantiteProduit")
    heures_de_travail = models.CharField()
    consommation_electrique = models.IntegerField()


class Produit(models.Model):
    nom = models.CharField(max_length=100)
    prix_de_vente = models.IntegerField()
    duree_de_vie = models.IntegerField()
    nombre_par_palette = models.IntegerField()
    operations = models.ForeignKey(
        Operation,
        on_delete=models.PROTECT,
    )


class PrixProduit(models.Model):
    produit = models.ForeignKey(
        Produit,
        on_delete=models.PROTECT,
    )
    prix_achat = models.IntegerField()


class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    prix_produits = models.ManyToManyField(PrixProduit)


class QuantiteProduit(models.Model):
    nombre = models.IntegerField()
    produit = models.ForeignKey(
        Produit,
        on_delete=models.PROTECT,
    )


class Stock(models.Model):
    quantite_produits = models.ManyToManyField(QuantiteProduit)
    palettes_max = models.IntegerField()


class PointDeVente(models.Model):
    nom = models.CharField(max_length=100)
    lieu = models.ForeignKey(
        Lieu,
        on_delete=models.PROTECT,
    )
    heures_de_travail = models.IntegerField()
    stcok = models.ForeignKey(
        Stock,
        on_delete=models.PROTECT,
    )


class Facture(models.Model):
    quantite_produits = models.ManyToManyField(QuantiteProduit)
    reduction = models.IntegerField()
    point_de_vente = models.ForeignKey(
        PointDeVente,
        on_delete=models.PROTECT,
    )
    client = models.CharField(max_length=100)
