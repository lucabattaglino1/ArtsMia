import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    # abilito il pulsante
    def handleAnalizzaOggetti(self, e):
        self._model.buildGraph()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato"))
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo contiene {self._model.getNumNodes()} nodi e {self._model.getNumEdges()} archi")
        )
        self._view._txtIdOggetto.disabled = False
        self._view._btnCompConnessa.disabled = False
        self._view.update_page()

    def handleCompConnessa(self,e):
        # recupera input utente
        txtIdOggetto = self._view._txtIdOggetto.value

        if txtIdOggetto == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione, inserire un valore nel campo id", color="red"))
            self._view.update_page()
            return

        try:
            idOggetto = int(txtIdOggetto)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione, inserire un valore numerico nel campo id", color="red"))
            self._view.update_page()
            return

        if not self._model.hasNode(idOggetto):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione, l'id inserito non è presente nel grafo", color="orange"))
            self._view.update_page()
            return

        sizeCompConn = self._model.getInfoCompConnessa(idOggetto)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"La componente connessa contenente l'oggetto con id {idOggetto} è composta di {sizeCompConn} nodi", color="green"))
        self._view.update_page()

        # abilito l'utente a poter scegliere la lunghezza
        self._view._ddLun.disabled = True
        self._view._btnCerca.disabled = True

        lunValues = range(2, sizeCompConn)

        for v in lunValues:
            self._view._ddLun.options.append(ft.Dropdown.Option(v))

        # altro metodo, data una lista vecchia mi crea una lista nuova a cui applico una funzione
        lunValuesDD = map(lambda x: ft.Dropdown.Option(x), lunValues)



        self._view.update_page()


    def handleCerca(self,e):
        # mi basta chiamarlo semplicemente cosi perche i controlli
        # sono stati fatti nella componente connessa
        source = self._model.getNodeFromId(int(sef._view._txtIdOggetto.value))

        if lun is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, selezionare un valore di lunghezza fra le scelte proposte"))
            self._view.update_page()
            return

        lunInt = int(lun)

        path, cost = self._model.getOptPath(source,lun)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Ho trovato un camminio che parte da {source} e che ha un peso totale pari a {cost}"))
        self._view.txt_result.controls.append(
            ft.Text(f"Di seguito i nodi che compongono questo cammino:"))

        for p in path:
            self._view.txt_result.controls.append(ft.text(p))

        self._view.update_page()








