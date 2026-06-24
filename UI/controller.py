import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
    def fillDDCategory(self):
        cat = (self._model.getCat())
        for c in cat:
            self._view._ddcategory.options.append(
                ft.dropdown.Option(key=c.category_id, text=c.category_name)
            )
        self._view.update_page()

    def handleCreaGrafo(self, e):
        s = self._view._ddcategory.value
        di = self._view._dp1.value
        df = self._view._dp2.value

        if s is None:
            self._view.txt_result.controls.append(ft.Text("SELEZIONARE UNA CATEGORIA!!!", color="red"))
            self._view.update_page()

        if di is None or df is None:
            self._view.txt_result.controls.append(ft.Text("SELEZIONARE UN RANGE DI DATE VALIDO!!!", color="red"))
            self._view.update_page()


        self._model.buildGraph(s,di,df)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("grafo creato correttamente", color="green"))
        self._view.txt_result.controls.append(ft.Text(f'il grafo ha {self._model.get_numnodi()} nodi'))
        self._view.txt_result.controls.append(ft.Text(f'il grafo ha {self._model.get_numarchi()} archi'))
        self._view.update_page()

    def handleBestProdotti(self, e):
        self._view.txt_result.controls.append(ft.Text(f'i 5 prodotti  più venduti sono:'))
        for n in self._model.get_top5_Prodotti():
            self._view.txt_result.controls.append(ft.Text(f'{n}'))
        self._view.update_page()

    def handleCercaCammino(self, e):
        pass



    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)
