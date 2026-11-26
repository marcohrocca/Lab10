import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self.threshold_selezionato = None
        self._view = view
        self._model = model

    def mostra_collegamenti(self, e):
        """
        Funzione che controlla prima se il valore dell'importo inserito sia valido (es. non deve essere una stringa) e
        poi popola "self._view.lista_visualizzazione" con le seguenti info
        * Numero di Filiali presenti
        * Numero di Collegamenti
        * Lista di Collegamenti che superano l'importo indicato come soglia
        """
        #Per prima cosa controllo che valore importo inserito sia vaido,ovvero sia un float e sia>0
        try:
            self.threshold_selezionato = float(self._view.importo_medio_minimo.value)
            if self.threshold_selezionato<0: #Metto <0 perchè interpreto 0 come valido,ovvero l'utente vuole che
                                             #mostri tutti gli archi
                self._view.show_alert("Inserire un valore positivo")
                return

        except ValueError:
            self._view.show_alert("Inserire un valore valido")
            return
        # Resetto la lista di visualizzazione nel caso utente clicchi 2 volte o più
        self._view.lista_visualizzazione.controls.clear()
        # Chiedo al model di costruire il grafo
        self._model.costruisci_grafo(self.threshold_selezionato)
        #Popolo con il numero di nodi
        self._view.lista_visualizzazione.controls.append(
            ft.Text(f"Il numero di filiali presenti è: {self._model.get_num_nodes()}")
        )
        # Popolo con il numero di archi
        self._view.lista_visualizzazione.controls.append(
            ft.Text(f"Il numero di collegamenti è: {self._model.get_num_edges()}")
        )
        #Popolo con lista collegamenti
        for filiale1,filiale2,peso in self._model.get_all_edges():
            self._view.lista_visualizzazione.controls.append(
                ft.Text(f"{filiale1.nome} - {filiale2.nome} - Importo medio per bonifico {peso:.2f} €")
            )

        self._view.lista_visualizzazione.update()

