import networkx as nx
from database.dao import DAO
class Model:
    def __init__(self):
        self._abbinamento_id_filiale = {}
        self._nodes = None
        self._edges = None
        self.G = nx.Graph()
        self._dao = DAO()
        self._filiali = None
        self._bonifici = None

    def media_filiali(self,bonifici):
        #In questa funzione creiamo un dizionario,quindi ancora nessun filtro
        #Come chiave abbiamo la coppia filiali,come valore una tupla (importi,n_bonifici)
        dizionario_archi={}
        for bonifico in bonifici:
            filiale_1=bonifico.id_filiale_origine
            filiale_2=bonifico.id_filiale_destinazione

            #Logica che ho usato prima controllo se esiste coppia in un verso,se non c'è guardo se esiste nell'altro verso,se entrambi no
            #Creo nuova chiave dizionario

            if (filiale_1,filiale_2) in dizionario_archi:
                dizionario_archi[(filiale_1,filiale_2)]=(dizionario_archi[(filiale_1,filiale_2)][0]+bonifico.importo,
                                                         dizionario_archi[(filiale_1,filiale_2)][1]+1)
            elif (filiale_2,filiale_1) in dizionario_archi:
                dizionario_archi[(filiale_2,filiale_1)]=(dizionario_archi[(filiale_2,filiale_1)][0]+bonifico.importo,
                                                        dizionario_archi[(filiale_2,filiale_1)][1]+1)
            else:
                dizionario_archi[(filiale_1,filiale_2)]=(bonifico.importo,1)

       #Adesso c'è da calcolare la media,così restituiamo dizionario più efficace
        for chiave in dizionario_archi:
            dizionario_archi[chiave]=dizionario_archi[chiave][0]/dizionario_archi[chiave][1]
        #A questo punto restituisco un dizionario avente come chiave la coppia id-filiali e come valore la media dei bonifici
        #es {(a,b):300}
        return dizionario_archi


    def costruisci_grafo(self, threshold):
        """
        Costruisce il grafo (self.G) inserendo tutte le Filiali (i nodi) presenti e filtrando i Collegamenti con
        importo medio per bonifico >= threshold (euro)
        """
        #Inizio resettando il grafo e dizionario_abbinamenti
        self.G.clear()
        self._abbinamento_id_filiale.clear()
        #Inizio creando i nodi ovvero le filiali
        self._filiali = self._dao.get_filiali()
        if self._filiali is not None:
            for filiale in self._filiali: #Creo un dizionario che abbina alla chiave id(univoca)
                                          #il nome della filiale es {"id12":"Filiale Torino Centro"}
                self._abbinamento_id_filiale[filiale.id]=filiale
                self.G.add_node(filiale) #Aggiungo filiale al grafico a prescindere al max rimane punto isolato
            self._bonifici = self._dao.get_bonifici()
            #Adesso che ho anche i bonifici chiamo la funziona che li raggruppa a coppie di filiali
            #questa funzione restituisce un dizionario avente come chiave la coppia id-filiali e come valore la media dei bonifici
            #es {(a,b):300}
            #Prima però controllo restituisca qualcosa
            if self._bonifici is None:
                raise RuntimeError("Impossibile leggere i bonifici dal database")
            filiali_peso=self.media_filiali(self._bonifici)
            for id_filiali,media in filiali_peso.items():
                #Aggiungo arco solo se rispetta requisiti
                if media >= threshold: #Implica che quel collegamento è valido e devo aggiungerlo al grafo
                    #A questo punto devo collegare id_filiali a nome filiale e aggiungere archi
                    filiale_1=self._abbinamento_id_filiale[id_filiali[0]]
                    filiale_2 = self._abbinamento_id_filiale[id_filiali[1]]
                    self.G.add_edge(filiale_1,filiale_2,weight=media)
        else:
            raise RuntimeError("Impossibile leggere le filiali dal database")





    def get_num_edges(self):
        """
        Restituisce il numero di Collegamenti (edges) del grafo
        :return: numero di edges del grafo
        """
        numero_archi = self.G.number_of_edges()
        return numero_archi

    def get_num_nodes(self):
        """
        Restituisce il numero di Filiali (nodi) del grafo
        :return: numero di nodi del grafo
        """
        numero_nodi=self.G.number_of_nodes()
        return numero_nodi

    def get_all_edges(self):
        """
        Restituisce tutti i Collegamenti (gli edges) con i corrispondenti pesi
        :return: gli edges del grafo con gli attributi (il weight)
        """
        lista_edges=[]
        for nodo_1,nodo_2,peso in self.G.edges.data("weight", default=1):
            lista_edges.append((nodo_1,nodo_2,peso))
        return lista_edges


