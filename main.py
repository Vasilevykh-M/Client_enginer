import flet as ft
import os, shutil
from Interface.SendFileControl import SendFile as SendForm
from Interface.GetDataControl import GetData as GetDataForm
from Interface.ModelControl import Model as ModelForm

def create_dir():
    if os.path.exists('weights_model'):
        dir = 'weights_model'
        shutil.rmtree(dir)
    os.mkdir('weights_model')
    os.mkdir('weights_model/torch')
    os.mkdir('weights_model/cat_boost')

class MainApp(ft.UserControl):
    def __init__(self, accept, show_banner_click):
        super(MainApp, self).__init__()
        self.accept = accept
        self.show_banner_click = show_banner_click


    def build(self):
        self.snack_bar = ft.SnackBar(ft.Text("Выполнено"), bgcolor=ft.colors.GREEN, action="Alright!")
        self.tabs = ft.Tabs(tabs = [
            ft.Tab(text = "Отправить файл на сервер"),
            ft.Tab(text = "Получить данные"),
            ft.Tab(text = "Построить модель"),
        ],
            on_change=self.on_select_tab
        )
        self.send_file_component = SendForm(self.accept)
        self.get_data = GetDataForm(self.accept, self.in_data_to_model)
        self.create_model = ModelForm(self.accept, self.show_banner_click)
        self.get_data.visible = False
        self.create_model.visible = False
        return ft.Column(controls=[
            self.tabs,
            self.send_file_component,
            self.get_data,
            self.create_model
        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        width=1200,
                         )

    def in_data_to_model(self, data_set):
        self.create_model.data_set = data_set
        self.update()

    def on_select_tab(self, e):
        status = self.tabs.tabs[self.tabs.selected_index].text
        if status == "Отправить файл на сервер":
            self.send_file_component.visible = True
            self.get_data.visible = False
            self.create_model.visible = False

        if status == "Получить данные":
            self.send_file_component.visible = False
            self.get_data.visible = True
            self.create_model.visible = False

        if status == "Построить модель":
            self.send_file_component.visible = False
            self.get_data.visible = False
            self.create_model.visible = True

        self.update()

def main(page: ft.Page):

    create_dir()

    page.snack_bar = ft.SnackBar(
        content=ft.Text("Hello, world!"),
        action="Alright!",
    )

    def close_banner(e):
        page.banner.open = False
        page.update()

    def show_banner_click():
        page.banner.open = True
        page.update()

    page.banner = ft.Banner(
        bgcolor=ft.colors.AMBER_100,
        leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
        content=ft.Text(
            "Проверьте заполнены ли все поля, и проверьте что все выходы предыдущего слоя совпадают с входами следующего"
        ),
        actions=[
            ft.TextButton("ОК", on_click=close_banner),
        ],
    )

    def accept(code):
        if code == 1:
            page.snack_bar = ft.SnackBar(ft.Text("Выполнено"), bgcolor=ft.colors.GREEN)
        if code == -1:
            page.snack_bar = ft.SnackBar(ft.Text("Ошибка"), bgcolor=ft.colors.RED)
        page.snack_bar.open = True
        page.update()

    main_component = MainApp(accept, show_banner_click)
    page.window_height = 600
    page.window_width = 1200
    page.window_resizable = False
    page.window_maximizable = False
    page.spacing = 50
    page.add(main_component)

ft.app(target=main)