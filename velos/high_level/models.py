# Create your models here.
from django.db import models


class Pays(models.Model):
    nom = models.CharField(max_length=100)
    tva = models.FloatField()
    tarif_electrique = models.FloatField()

    def __str__(self):
        return self.nom


class Ville(models.Model):
    nom = models.CharField(max_length=100)
    taxe_immobiliere = models.FloatField()
    prix_m2 = models.FloatField()
    pays = models.ForeignKey(
        Pays,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.nom


class Machine(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.FloatField()
    duree_de_vie = models.FloatField()
    cout_maintenance = models.FloatField()
    superfice = models.FloatField()

    def __str__(self):
        return self.nom


class QuantiteMachine(models.Model):
    machine = models.ForeignKey(
        Machine,
        on_delete=models.PROTECT,
    )
    nombre = models.FloatField()

    def __str__(self):
        return self.nom


class Lieu(models.Model):
    nom = models.CharField(max_length=100)
    ville = models.ForeignKey(
        Ville,
        on_delete=models.PROTECT,
    )
    superficie = models.FloatField()
    quantite_machines = models.ManyToManyField(QuantiteMachine)
    consommation_electrique = models.FloatField()

    def __str__(self):
        return self.nom


class Transport(models.Model):
    nombre_palettes = models.FloatField()
    cout = models.FloatField()
    delai = models.FloatField()
    depart = models.ForeignKey(
        Lieu,
        on_delete=models.PROTECT,
    )
    arrivee = models.ForeignKey(
        Ville,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.nom


class Operation(models.Model):
    nom = models.CharField(max_length=100)
    Operation_suivante = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
    )
    cout = models.FloatField()
    machine = models.ForeignKey(
        Machine,
        on_delete=models.PROTECT,
    )

    quantite_produits = models.ManyToManyField("QuantiteProduit")
    heures_de_travail = models.CharField()
    consommation_electrique = models.FloatField()

    def __str__(self):
        return self.nom


class Produit(models.Model):
    nom = models.CharField(max_length=100)
    prix_de_vente = models.FloatField()
    duree_de_vie = models.FloatField()
    nombre_par_palette = models.FloatField()
    operations = models.ForeignKey(
        Operation,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.nom


class PrixProduit(models.Model):
    produit = models.ForeignKey(
        Produit,
        on_delete=models.PROTECT,
    )
    prix_achat = models.FloatField()

    def __str__(self):
        return self.nom


class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    prix_produits = models.ManyToManyField(PrixProduit)

    def __str__(self):
        return self.nom


class QuantiteProduit(models.Model):
    nombre = models.FloatField()
    produit = models.ForeignKey(
        Produit,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.nom


class Stock(models.Model):
    quantite_produits = models.ManyToManyField(QuantiteProduit)
    palettes_max = models.FloatField()

    def __str__(self):
        return self.nom


class PointDeVente(models.Model):
    nom = models.CharField(max_length=100)
    lieu = models.ForeignKey(
        Lieu,
        on_delete=models.PROTECT,
    )
    heures_de_travail = models.FloatField()
    stcok = models.ForeignKey(
        Stock,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.nom


class Facture(models.Model):
    quantite_produits = models.ManyToManyField(QuantiteProduit)
    reduction = models.FloatField()
    point_de_vente = models.ForeignKey(
        PointDeVente,
        on_delete=models.PROTECT,
    )
    client = models.CharField(max_length=100)

    def __str__(self):
        return self.nom
