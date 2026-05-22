'''
Classi di utilità per la gestione dei veicoli.
'''
from abc import ABC, abstractmethod

class Veicolo(ABC):
    conteggio: int = 0

    def __init__(self,tipo:str, licenza:str, capacità:int,
                  guidatore=None, tecnico=None, 
                 ):
        self._tipo = tipo
        if (licenza not in ["","A","B", "C", "D"]) :
            raise ValueError("Licenza non valida")  
        
        self._licenza = licenza
        self._capacità = capacità
        self.colli = []
        self._guidatore = guidatore
        self._tecnico = tecnico
        self._carico_corrente=0
        self._rotto = False
        self_spare = False
        Veicolo.conteggio += 1
    
    @property
    def ready(self):
        return self._guidatore and not self._rotto
    
    @property
    def isRotto(self):
        return self._rotto  
    
    @property
    def isSpare(self):
        return self._spare
    
    def setSpare(self, value:bool):
        self._spare = value

    def segnalaguasto(self, tecnico:str=""):
        self._tecnico = tecnico
        self._rotto = True

    def __str__(self):
        return f"Veicolo {self.tipo} con licenza {self.licenza} e capacità {self.capacità}"
    
    def carica(self, colli:int):
        if self._carico_corrente + colli > self._capacità:
            raise ValueError("Capacità superata")
        self.carico_corrente += colli
        self.colli.append(colli)

    def scarica(self, colli:int):
        if colli > self._carico_corrente:
            raise ValueError("Non ci sono abbastanza colli da scaricare")
        self._carico_corrente -= colli
        self.colli.remove(colli)

    @property
    def licenza(self):
        return self._licenza
        
    @property
    def giudatore(self):
        return self._guidatore
    
    @giudatore.setter
    def guidatore(self, value):
        if(value.licenza != self.licenza): #TODO: se la licenza è superiore a quella richiesta, dovrebbe essere comunque valida
            raise ValueError("Il guidatore non ha la licenza adatta per questo veicolo")
        self.guidatore = value

    @property
    def tecnico(self):
        return self._tecnico
    
    @tecnico.setter
    def tecnico(self, value):
        self._tecnico = value

    @tecnico.deleter
    def tecnico(self):
        self._tecnico = None


class Bici(Veicolo):
    def __init__(self, capacità:int=10,
                  guidatore=None, tecnico=None):
        super().__init__("Bici", "", capacità, guidatore, tecnico)

class Moto(Veicolo):
    def __init__(self, targa:str, capacità:int=50,
                  guidatore=None, tecnico=None):
        super().__init__("Moto", "A", capacità, guidatore, tecnico)
        self.targa = targa

class Auto(Veicolo):
    def __init__(self, targa:str,capacità:int=250,
                  guidatore=None, tecnico=None):
        super().__init__("Auto", "B", capacità, guidatore, tecnico)
        self.targa = targa


class Camion(Veicolo):
    def __init__(self, targa:str, capacità:int=1000,
                  guidatore=None, tecnico=None):
        super().__init__("Camion", "C", capacità, guidatore, tecnico)
        self.targa = targa
