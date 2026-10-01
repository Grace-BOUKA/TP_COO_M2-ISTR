# Create your models here.
from django.db import models


class Pays(models.Model):
    nom = models.CharField(max_length=100)
    tva = models.FloatField()
    tarif_electrique = models.FloatField()
    salaire_minimum = models.FloatField()

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

    def costs(self):
        somme = 0
        for lieu in self.lieu_set.all():
            somme += lieu.costs()
        return somme


class Machine(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.FloatField()
    duree_de_vie = models.FloatField()
    cout_maintenance = models.FloatField()
    superficie = models.FloatField(default=0)
    # Ajout du lien vers Lieu pour que self.machine_set fonctionne dans Lieu
    lieu = models.ForeignKey(
        'Lieu',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.nom

    def costs(self):
        return self.prix


class QuantiteMachine(models.Model):
    machine = models.ForeignKey(
        Machine,
        on_delete=models.PROTECT,
    )
    nombre = models.FloatField()

    def __str__(self):
        return f"{self.machine.nom}: {self.nombre}"


class Lieu(models.Model):
    nom = models.CharField(max_length=100)
    ville = models.ForeignKey(
        Ville,
        on_delete=models.PROTECT,
    )
    superficie = models.FloatField()
    quantite_machines = models.ManyToManyField(QuantiteMachine, blank=True)
    consommation_electrique = models.FloatField()

    def __str__(self):
        return self.nom

    def costs(self):
        cout_immo = self.superficie * self.ville.prix_m2
        cout_energie = self.consommation_electrique * self.ville.pays.tarif_electrique

        # Somme des machines rattachées
        cout_machines = 0
        for machine in self.machine_set.all():
            cout_machines += machine.costs()

        # Coût des stocks rattachés
        cout_stocks = 0
        for stock in self.stock_set.all():
            cout_stocks += stock.costs()

        return cout_immo + cout_energie + cout_machines + cout_stocks


class QuantiteProduit(models.Model):
    nombre = models.FloatField()
    produit = models.ForeignKey(
        'Produit',
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f"{self.produit.nom}: {self.nombre}"

    def costs(self):
        # Correction de la syntaxe Python (pas d'accolades !)
        return self.nombre * self.produit.prix_de_vente


class Stock(models.Model):
    quantite_produits = models.ManyToManyField(QuantiteProduit)
    palettes_max = models.FloatField()
    lieu = models.ForeignKey(
        Lieu,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"quantité palettes: {self.palettes_max}"

    def costs(self):
        somme = 0
        # Correction : accès QuerySet ManyToMany avec .all()
        for qp in self.quantite_produits.all():
            somme += qp.costs()
        return somme


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
        return f"Depart: {self.depart}; Arrivée: {self.arrivee}"

    def costs(self):
        return self.cout


class Operation(models.Model):
    nom = models.CharField(max_length=100)
    Operation_suivante = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    cout = models.FloatField()
    machine = models.ForeignKey(
        Machine,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    quantite_produits = models.ManyToManyField(QuantiteProduit)
    heures_de_travail = models.FloatField(default=0)
    consommation_electrique = models.FloatField()

    def __str__(self):
        return self.nom

    def costs(self):
        cout_machine = 0
        if self.machine:
            cout_machine = self.machine.costs()

        cout_mo = 0
        cout_energie = 0
        return cout_machine + cout_mo + cout_energie


class Produit(models.Model):
    nom = models.CharField(max_length=100)
    prix_de_vente = models.FloatField()
    duree_de_vie = models.FloatField()
    nombre_par_palette = models.FloatField()

    def __str__(self):
        return self.nom

    def costs(self):
        return self.prix_de_vente


class PrixProduit(models.Model):
    produit = models.ForeignKey(
        Produit,
        on_delete=models.PROTECT,
    )
    prix_achat = models.FloatField()

    def __str__(self):
        return self.produit.nom

    def costs(self):
        return self.prix_achat


class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    prix_produits = models.ManyToManyField(PrixProduit)

    def __str__(self):
        return self.nom


class PointDeVente(models.Model):
    nom = models.CharField(max_length=100)
    lieu = models.ForeignKey(
        Lieu,
        on_delete=models.PROTECT,
    )
    heures_de_travail = models.FloatField()
    stock = models.ForeignKey(
        Stock,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.nom

    def costs(self):
        cout_lieu = 0
        if self.lieu:
            cout_lieu = self.lieu.costs()

        cout_transports = 0
        for transport in self.transport_set.all():
            cout_transports += transport.costs()

        return cout_lieu + cout_transports


class Facture(models.Model):
    quantite_produits = models.ManyToManyField(QuantiteProduit)
    reduction = models.FloatField()
    point_de_vente = models.ForeignKey(
        PointDeVente,
        on_delete=models.PROTECT,
    )
    client = models.CharField(max_length=100)

    def __str__(self):
        return f"Facture du client: {self.client}"















# from django.db import models
# class Pays(models.Model):
#     nom = models.CharField(max_length=100)
#     tva = models.FloatField()
#     tarif_electrique = models.FloatField()
#     salaire_minimum=models.FloatField()

#     def __str__(self):
#         return self.nom



# class Ville(models.Model):
#     nom = models.CharField(max_length=100)
#     taxe_immobiliere = models.FloatField()
#     prix_m2 = models.FloatField()
#     pays = models.ForeignKey(
#         Pays,
#         on_delete=models.PROTECT,
#     )

#     def __str__(self):
#         return self.nom

    
#     def costs(self):
#         somme = 0
#         for lieu in self.lieu_set.all():
#             somme = somme + lieu.costs()
#         return somme


# class Machine(models.Model):
#     nom = models.CharField(max_length=100)
#     prix = models.FloatField()
#     duree_de_vie = models.FloatField()
#     cout_maintenance = models.FloatField()
#     superficie = models.FloatField()

#     def __str__(self):
#         return self.nom

#     def costs(self):
#         return self.prix


# class QuantiteMachine(models.Model):
#     machine = models.ForeignKey(
#         Machine,
#         on_delete=models.PROTECT,
#     )
#     nombre = models.FloatField()

#     def __str__(self):
#         return f"{self.machine.nom}: {self.nombre}"


        


# class Lieu(models.Model):
#     nom = models.CharField(max_length=100)
#     ville = models.ForeignKey(
#         Ville,
#         on_delete=models.PROTECT,
#     )
#     superficie = models.FloatField()
#     quantite_machines = models.ManyToManyField(QuantiteMachine)
#     consommation_electrique = models.FloatField()

#     def __str__(self):
#         return self.nom

#     def costs(self):
#         cout_immo = self.superficie * self.ville.prix_m2
#         cout_energie = self.consommation_electrique * self.ville.pays.tarif_electrique
        
#         # Cout somme des machines du lieu
#         cout_machines = 0
#         for machine in self.machine_set.all():
#             cout_machines = cout_machines + machine.costs()

#         # Coût de stocks
#         cout_stocks = 0
#         for stock in self.stock_set.all():
#             cout_stocks = cout_stocks + stock.costs()
            
#         return cout_immo + cout_energie + cout_machines + cout_stocks

# class Transport(models.Model):
#     nombre_palettes = models.FloatField()
#     cout = models.FloatField()
#     delai = models.FloatField()
#     depart = models.ForeignKey(
#         Lieu,
#         on_delete=models.PROTECT,
#     )
#     arrivee = models.ForeignKey(
#         Ville,
#         on_delete=models.PROTECT,
#     )

#     def __str__(self):
#         return f"Depart: {self.depart}; Arrivée: {self.arrivee}"

#     def costs(self):
#         # Retourne le coût de transport de tout les produits
#         return {self.cout}


# class Operation(models.Model):
#     nom = models.CharField(max_length=100)
#     Operation_suivante = models.ForeignKey(
#         "self",
#         on_delete=models.PROTECT,
#     )
#     cout = models.FloatField()
#     machine = models.ForeignKey(
#         Machine,
#         on_delete=models.PROTECT,
#     )

#     quantite_produits = models.ManyToManyField("QuantiteProduit")
#     heures_de_travail = models.CharField()
#     consommation_electrique = models.FloatField()

#     def __str__(self):
#         return self.nom

#     def costs(self):
#         cout_machine = 0
#         if self.machine:
#             cout_machine = self.machine.costs()
            
#         cout_mo = self.heures_de_travail * self.lieu.ville.pays.salaire_minimum
#         cout_energie = self.consommation_electrique * self.lieu.ville.pays.tarif_electrique
        
#         return cout_machine + cout_mo + cout_energie


# class Produit(models.Model):
#     nom = models.CharField(max_length=100)
#     prix_de_vente = models.FloatField()
#     duree_de_vie = models.FloatField()
#     nombre_par_palette = models.FloatField()
#     operations = models.ForeignKey(
#         Operation,
#         on_delete=models.PROTECT,
#     )

#     def __str__(self):
#         return self.nom

#     def costs(self):
#         somme = 0
#         for operation in self.operations.all():
#             somme = somme + operation.costs()
#         return somme


# class PrixProduit(models.Model):
#     produit = models.ForeignKey(
#         Produit,
#         on_delete=models.PROTECT,
#     )
#     prix_achat = models.FloatField()

#     def __str__(self):
#         return self.produit.nom
    
#     def costs(self):
#         return self.prix_achat


# class Fournisseur(models.Model):
#     nom = models.CharField(max_length=100)
#     prix_produits = models.ManyToManyField(PrixProduit)

#     def __str__(self):
#         return self.nom

#     def costs(self):
#         return self.prix_produits


# class QuantiteProduit(models.Model):
#     nombre = models.FloatField()
#     produit = models.ForeignKey(
#         Produit,
#         on_delete=models.PROTECT,
#     )

#     def __str__(self):
#         return f"{self.produit.nom}: {self.nombre}"

#     def costs(self):
#         # Retourne le cout de la somme de la quantité de produit
#         return self.nombre*self.produit.prix_de_vente


# class Stock(models.Model):
#     quantite_produits = models.ManyToManyField(QuantiteProduit)
#     palettes_max = models.FloatField()

#     def __str__(self):
#         return f"quantité palettes: {self.palettes_max}"

    
#     def costs(self):
#         # Retourne le coût du stock sommee
#         somme=0
#         for qp in self.quantite_produits:
#             somme=somme+qp.costs()
#         return somme


# class PointDeVente(models.Model):
#     nom = models.CharField(max_length=100)
#     lieu = models.ForeignKey(
#         Lieu,
#         on_delete=models.PROTECT,
#     )
#     heures_de_travail = models.FloatField()
#     stock = models.ForeignKey(
#         Stock,
#         on_delete=models.PROTECT,
#     )

#     def __str__(self):
#         return self.nom

    
#     def costs(self):
#         cout_lieu = 0
#         if self.lieu:
#             cout_lieu = self.lieu.costs()
            
#         cout_transports = 0
#         for transport in self.transport_set.all():
#             cout_transports = cout_transports + transport.costs()
            
#         return cout_lieu + cout_transports


# class Facture(models.Model):
#     quantite_produits = models.ManyToManyField(QuantiteProduit)
#     reduction = models.FloatField()
#     point_de_vente = models.ForeignKey(
#         PointDeVente,
#         on_delete=models.PROTECT,
#     )
#     client = models.CharField(max_length=100)

#     def __str__(self):
#         return f"Facture du client: {self.client}"
