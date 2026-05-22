'''
Anagrafiche clienti, guidatori
'''

class Anagrafica:
    def __init__(self, nome:str, cognome:str,
                 codice_fiscale:str):
        self._nome = nome
        self._cognome = cognome
        self._codice_fiscale = codice_fiscale

    @property
    def nome(self):
        return self._nome
    
    @property
    def cognome(self):
        return self._cognome    
    
    @property
    def codice_fiscale(self):
        return self._codice_fiscale
    
    @property
    def nome_completo(self):
        return f"{self._nome} {self._cognome}"
    
    @property
    def cognome_nome(self):
        return f"{self._cognome} {self._nome}"
    
    def __str__(self):  
        return f"{self._nome} {self._cognome} ({self._codice_fiscale})"
    

class Guidatore(Anagrafica):
    def __init__(self, nome:str, cognome:str,
                 codice_fiscale:str, licenza:str):
        super().__init__(nome, cognome, codice_fiscale)
        self._licenza = licenza

    @property
    def licenza(self):
        return self._licenza
    
class Cliente(Anagrafica):
    def __init__(self, nome:str, cognome:str,
                 codice_fiscale:str, indirizzo:str,
                 lat, lng):
        super().__init__(nome, cognome, codice_fiscale)
        self._indirizzo = indirizzo
        self._lat = lat
        self._lng = lng

    @property
    def indirizzo(self):
        return self._indirizzo
    @indirizzo.setter
    def indirizzo(self, value):
        self._indirizzo = value

    @property
    def lat(self):
        return self._lat

    @lat.setter
    def lat(self, value):
        self._lat = value

    @property
    def lng(self):
        return self._lng

    @lng.setter
    def lng(self, value):
        self._lng = value