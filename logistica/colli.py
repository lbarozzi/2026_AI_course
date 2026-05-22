'''
'''

class collo1d:
    contatore = 0
    def __init__(self,kg,cliente:str):
        self._kg=kg
        self._cliente=cliente
        collo1d.contatore += 1
        self._id=collo1d.contatore

    @property
    def kg(self):
        return self._kg
    
    def __str__(self):
        return f"Collo {self._id} da {self._kg} kg per il cliente {self._cliente}"
    

class collo4d(collo1d):
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
        return f"Collo {self._id} da {self._kg} kg per il cliente {self._cliente} con dimensioni {self._lunghezza}x{self._larghezza}x{self._altezza}"