import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = self._model.getAllYears()
        self._listShape = []

    def fillDDShape(self, e):
        self._view.ddshape.options.clear()
        self._view.ddshape.value = ''
        year = e.control.data
        self._listShape = self._model.getAllShapes(int(year))
        for s in self._listShape:
            self._view.ddshape.options.append(ft.dropdown.Option(s))
        self._view.btn_graph.disabled = False
        self._view.update_page()

    def fillDD(self):
        for y in self._listYear:
            self._view.ddyear.options.append(ft.dropdown.Option(text=y,
                                                                data=y,
                                                                on_click=self.fillDDShape))


    def handle_graph(self, e):
        self._view.txt_result.controls.clear()

        year = self._view.ddyear.value
        shape = self._view.ddshape.value
        if year is None or shape == '':
            self._view.create_alert('seleziona i campi richiesti')
            return
        stats = self._model.creaGrafo(year, shape)
        self._view.txt_result.controls.append(ft.Text(stats))
        self._view.btn_path.disabled = False
        self._view.update_page()

    def handle_path(self, e):
        self._view.txtOut2.controls.clear()
        sol, dist = self._model.get_path()
        self._view.txtOut2.controls.append(ft.Text(f'Percorso di nodi = {len(sol)} con distanza totale = {dist}'))
        for i in range(len(sol) - 1):
            self._view.txtOut2.controls.append(ft.Text(f"{sol[i]} --> {sol[i+1]} peso = "
                                                       f"{self._model.grafo[sol[i]][sol[i+1]]['weight']} "
                                                       f"distanza = {self._model.getDist(sol[i:i+2])}"))
        self._view.update_page()
