'''
Qui si gestisce il cuore della logistica
'''
from colli import collo1d, collo4d
from veicoli import Veicolo,Bici,Moto, Auto, Camion
from anagrafiche import * 

class Gestore:
    def __init__(self, colli_per_veicolo:int=20):
        self._mezzi= []
        self._guidatori = []
        self._colli = []
        self._colli_per_veicolo = colli_per_veicolo

    def __str__(self):
        return f"Gestore con {len(self._mezzi)} mezzi, {len(self._guidatori)} guidatori e {len(self._colli)} colli"    
    
    @property
    def lista_bici(self, spare=False, rotte=False):
        #return [m for m in self._mezzi if isinstance(m, Bici) and  m.isSpare== spare and m.isRotto==rotte]
        return self.lista_mezzi_by_type(Bici, spare, rotte)
        
    @property
    def lista_moto(self, spare=False, rotte=False):
        return self.lista_mezzi_by_type(Moto, spare, rotte)
    
    @property
    def lista_auto(self, spare=False, rotte=False):
        return self.lista_mezzi_by_type(Auto, spare, rotte)
    
    @property
    def lista_camion(self, spare=False, rotte=False):
        return self.lista_mezzi_by_type(Camion, spare, rotte)
    
    def lista_mezzi_by_type(self, tipo, spare=False, rotte=False):
        return [m for m in self._mezzi if isinstance(m, tipo) and  m.isSpare== spare and m.isRotto==rotte]
    
    def lista_mezzi_by_name(self, tipo:str="", spare=False, rotte=False):
        return [m for m in self._mezzi if m.tipo == tipo and  m.isSpare== spare and m.isRotto==rotte]
        
    @property
    def lista_guidatori(self, licenza:str=""):
        return [g for g in self._guidatori if g.licenza == licenza]
    
    #Rogna: carichiamo dalle bici fino ai camion
    #Promemoria cambierà 
    # distanze
    def crea_liste_consegna(self):
        if not self._colli or not self._mezzi or not self._guidatori:
            raise ValueError("Non ci sono colli, mezzi o guidatori disponibili per creare le liste di consegna")
        
        for lic in ["","A","B","C"]:
            guidatori = self.lista_guidatori(lic)
            for g in guidatori:
                mezzi= self.lista_bici() if lic=="" else self.list_moto() if lic=="A" else self.lista_auto() if lic=="B" else self.lista_camion()
                mezzi_disponibili = [m for m in mezzi if not m.isRotto]
                if not mezzi_disponibili:
                    raise ValueError(f"Non ci sono mezzi disponibili per la licenza {lic}")
                mezzo= mezzi_disponibili[0]  #Prendo il primo disponibile, potrei implementare una logica più complessa
                mezzo._guidatore = g
                colli_adattabili = [c for c in self._colli if c.kg <= mezzo._capacità// self._colli_per_veicolo]

                while colli_adattabili and len(mezzo.colli) < self._colli_per_veicolo:
                    collo = colli_adattabili.pop(0)
                    try:
                        mezzo.carica(collo.kg)
                        self._colli.remove(collo)
                    except ValueError:
                        #Se il collo è troppo pesante, lo metto in fondo alla lista
                        colli_adattabili.append(collo)
                        # break  #Esco dal ciclo per passare al prossimo mezzo
            


    def _rompi_mezzi(self, lista, percentuale_rotti:float=0.2):
        if not lista:
            return
        
        import random
        _tmp_rotti= random.sample(lista, int(len(lista)*percentuale_rotti))
        for m in _tmp_rotti:
            if isinstance(m, Veicolo):
                m.segnalaguasto()
    
    def save_to_file(self, filename:str):
        import pickle
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load_from_file(cls, filename:str):
        from pathlib import Path
        import pickle
        if Path("gestore.pkl").exists():
            with open("gestore.pkl", "rb") as f:
                return pickle.load(f)
        else:
            return None

    @classmethod
    def crea_gestore(cls, numero_veicoli:int=15, 
                     numero_guidatori:int=10,
                     percentuale_rotti:float=0.2,
                     colli_per_veicolo:int=20,
                     numero_clienti:int=150,
                     licenze=["","A","B", "C", "D"]):
        #PRO
        tmp= cls.load_from_file("gestore.pkl")
        if tmp:
            return tmp
        
        tmp= cls(colli_per_veicolo)

        for p in licenze:
            for g in range(numero_guidatori):
                tmp._guidatori.append(Guidatore(f"Nome{g}", f"Cognome{g}", f"CF{g}", p))          

            for v in range(numero_veicoli):
                foo= None
                match p:
                    case "":
                        foo= Bici()
                    case "A":
                        foo= Moto(f"MT{p}{v}")
                    case "B":
                        foo= Auto(f"AT{p}{v}")
                    case "C":
                        foo= Camion(f"CM{p}{v}")
                    
                if foo:
                    tmp._mezzi.append(foo)
        
        #Spacca i veicoli
        tmp._rompi_mezzi(tmp.lista_bici(), percentuale_rotti)
        tmp._rompi_mezzi(tmp.lista_moto(), percentuale_rotti)
        tmp._rompi_mezzi(tmp.lista_auto(), percentuale_rotti)
        tmp._rompi_mezzi(tmp.lista_camion(), percentuale_rotti)

        #Creo clienti casuali
        import random
        tmp_clienti = [Cliente(f"Nome{c}", f"Cognome{c}", f"CF{c}", f"Indirizzo{c}",
                        random.randint(1, 100), random.randint(1, 100)) for c in range(numero_clienti)]
        
        #Colli
        tot_colli= numero_guidatori * colli_per_veicolo

        for c in range(tot_colli):
            cliente= random.choice(tmp_clienti)
            peso= random.randint(1, 100)  #Occhio che ci potrebbero essere colli non consegnabili
            tmp._colli.append(collo1d(peso, cliente))
        
        tmp.save_to_file("gestore.pkl")
        return tmp  

    
