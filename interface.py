import flet as ft
import grpc
import pandas as pd

import RemouteSmartRieltor_pb2_grpc

import SendFileForm

class MainApp(ft.UserControl):
    def build(self):
        self.tabs = ft.Tabs(tabs = [
            ft.Tab(text = "Отправить файл на сервер"),
            ft.Tab(text = "Получить прогноз")
        ],
            on_change=self.on_select_tab
        )
        self.send_file_component = SendFileForm.SendFile(self.accept)
        self.state_bar = ft.Container(content=ft.Text("Состояние", width=1146, height=40, text_align=ft.TextAlign.CENTER, bgcolor=ft.colors.GREY),width=1146, height=40, bgcolor=ft.colors.GREY)
        return ft.Column(controls=[
            self.tabs,
            self.send_file_component,
            self.state_bar
        ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=1200,
        )

    def accept(self, i):
        if i == 1:
            self.state_bar.bgcolor = ft.colors.GREEN
            self.state_bar.content.bgcolor = ft.colors.GREEN
            self.state_bar.content.value = "Данные отправлены"
        if i == -1:
            self.state_bar.bgcolor = ft.colors.RED
            self.state_bar.content.bgcolor = ft.colors.RED
            self.state_bar.content.value = "Ошибка сервера"
        if i == -2:
            self.state_bar.bgcolor = ft.colors.RED
            self.state_bar.content.bgcolor = ft.colors.RED
            self.state_bar.content.value = "Содержание файла не корректно"
        self.update()

    def on_select_tab(self, e):
        status = self.tabs.tabs[self.tabs.selected_index].text
        if status == "Отправить файл на сервер":
            self.send_file_component.visible = True

        if status == "Получить прогноз":
            self.send_file_component.visible = False

        self.update()