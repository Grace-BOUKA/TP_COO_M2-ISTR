# Create your tests here.
from django.test import TestCase
from .models import (
    Lieu,
    Machine,
    Pays,
    Produit,
    QuantiteProduit,
    Stock,
    Ville,
)

class MachineModelTests(TestCase):

    def test_machine_creation(self):
        Machine.objects.create(
            nom="CNC",
            prix=28000,
            duree_de_vie=5,
            cout_maintenance=5000,
            superficie=20,
        )
        self.assertEqual(Machine.objects.count(), 1)


class TestUnitaireCosts(TestCase):

    def test_unitaire(self):
        pays = Pays.objects.create(
            nom="France",
            tva=20,
            tarif_electrique=0.2,
            salaire_minimum=12,
        )

        ville = Ville.objects.create(
            nom="Labège",
            taxe_immobiliere=1000,
            prix_m2=2000,
            pays=pays,
        )

        lieu = Lieu.objects.create(
            nom="Entrepot de Labège",
            superficie=50,
            consommation_electrique=5000,
            ville=ville,
        )

        Machine.objects.create(
            nom="Machine 1", prix=10000, duree_de_vie=5, cout_maintenance=100, superficie=10, lieu=lieu
        )
        Machine.objects.create(
            nom="Machine 2", prix=5000, duree_de_vie=5, cout_maintenance=100, superficie=10, lieu=lieu
        )

        tubes = Produit.objects.create(
            nom="Tubes d'acier",
            prix_de_vente=1000,
            duree_de_vie=10,
            nombre_par_palette=100,
        )
        cables = Produit.objects.create(
            nom="Câbles",
            prix_de_vente=3000,
            duree_de_vie=10,
            nombre_par_palette=100,
        )

        qp1 = QuantiteProduit.objects.create(produit=tubes, nombre=2)
        qp2 = QuantiteProduit.objects.create(produit=cables, nombre=1)

        stock = Stock.objects.create(palettes_max=10, lieu=lieu)
        stock.quantite_produits.add(qp1, qp2)

        lieu_teste = Lieu.objects.first()
        self.assertEqual(lieu_teste.costs(), 121000)

        # if(self.assertEqual(lieu_teste.costs(), 111000)=="OK"):
        #     print(f"SUCCES! | Valeur retournée: [{lieu_teste}] | Valeur attendue: 111000")
            
        # else:
        #     print(f"ECHEC! | Valeur retournée: {lieu_teste}")





































# from django.test import TestCase
# from .models import *


# class MachineModelTests(TestCase):

#     def test_machine_creation(self):
#         Machine.objects.create(
#             nom="CNC",
#             prix=28000,
#             duree_de_vie=5,
#             cout_maintenance=5000,
#             superficie=20,
#         )

#         self.assertEqual(Machine.objects.count(), 1)



# class TestUnitaireCosts(TestCase):

#     def test_unitaire(self):
#         # Remplissage de la BDD

#         pays = Pays.objects.create(
#             nom="France",
#             tva=20,
#             tarif_electrique=0.2,
#             salaire_minimum=12,
#         )

#         ville = Ville.objects.create(
#             nom="Labège",
#             taxe_immobiliere=1000,
#             prix_m2=2000,
#             pays=pays,
#         )

#         lieu = Lieu.objects.create(
#             nom="Entrepot de Labège",
#             superficie=50,
#             consommation_electrique=5000,
#             ville=ville,
#         )

#         # Création des machines
#         Machine.objects.create(nom="Machine 1", prix=10000, lieu=lieu)
#         Machine.objects.create(nom="Machine 2", prix=5000, lieu=lieu)

#         # Création des Produits
#         tubes=Produit.objects.create(nom="Tubes d'acier", prix_de_vente=1000)
#         cables=Produit.objects.create(nom="Câbles", prix_de_vente=3000)

#         # Création quantité de produits
#         qte_tubes=QuantiteProduit.objects.create(produit=tubes, nombre=2)
#         qte_cables=QuantiteProduit.objects.create(produit=cables, nombre=1)


#         # Création des stocks
#         stock = Stock.objects.create(palettes_max=10, lieu=lieu)
#         stock.quantite_produits.add(qte_tubes, qte_cables)

#         # Controle du résultat (Oracle)
#         lieu_teste = Lieu.objects.first()


#         self.assertEqual(lieu_teste.costs(), 111000)

#         # if(self.assertEqual(lieu_teste.costs(), 111000)=="OK"):
#         #     print(f"SUCCES! | Valeur retournée: [{lieu_teste}] | Valeur attendue: 111000")
            
#         # else:
#         #     print(f"ECHEC! | Valeur retournée: {lieu_teste}")







