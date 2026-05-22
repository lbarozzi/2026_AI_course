'''
'''

class Collo1d:
    contatore = 0
    def __init__(self,kg,cliente:str):
        self._kg=kg
        self._cliente=cliente
        Collo1d.contatore += 1
        self._id=Collo1d.contatore

    @property
    def kg(self):
        return self._kg

    @property
    def cliente(self):
        return self._cliente

    @property
    def id(self):
        return self._id
    
    def __str__(self):
        return f"Collo {self.id} da {self.kg} kg per il cliente {self.cliente}"
    

class Collo4d(Collo1d):
    def __init__(self,kg,cliente:str,lunghezza,larghezza,altezza):
        super().__init__(kg,cliente)
        self._lunghezza=lunghezza
        self._larghezza=larghezza
        self._altezza=altezza

    @property
    def lunghezza(self):
        return self._lunghezza
    
    @property
    def larghezza(self):
        return self._larghezza
    
    @property
    def altezza(self):
        return self._altezza
    
    def __str__(self):
        return f"Collo {self.id} da {self.kg} kg per il cliente {self.cliente} con dimensioni {self.lunghezza}x{self.larghezza}x{self.altezza}"