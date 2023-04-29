import datetime

import matplotlib
import matplotlib.pyplot as plt

import grpc
import pandas as pd

import RemouteSmartRieltor_pb2_grpc
import RemouteSmartRieltor_pb2
import flet as ft
from flet.matplotlib_chart import MatplotlibChart

import validation_data
from generator_data import genereation_data_from_server
from generator_data import genereation_data_from_file

matplotlib.rcParams['figure.figsize'] = (6,6)
class Plot_control(ft.UserControl):
    def __init__(self, back):
        super(Plot_control, self).__init__()
        self.back = back

    def on_back_button(self, e):
        self.back()
        self.update()

    def build(self):
        df = pd.DataFrame({"A": [1, 2, 3], "C": [1, 2, 3]})
        self.back_button = ft.ElevatedButton("Назад", on_click=self.on_back_button)
        fig, ax = plt.subplots()
        ax.bar(df["A"].unique(), df["A"].value_counts())
        self.plot = MatplotlibChart(fig, isolated=True)
        self.plot.original_size = True
        return ft.Column(controls=[self.back_button, self.plot])

class FeatureComponent(ft.UserControl):
    def __init__(self, feature, data_set, plot_fig):
        super(FeatureComponent, self).__init__()
        self.feature = feature
        self.data_set = data_set
        self.plot_fig = plot_fig


    def on_row_click(self, e):
        print(self.feature)
        fig, ax = plt.subplots()
        ax.bar(self.data_set.data[self.feature].unique(), self.data_set.data[self.feature].value_counts())
        ax.set_ylabel("Count")
        ax.set_xlabel("Value")
        ax.set_title(self.feature)
        self.plot_fig(fig)

    def build(self):
        return ft.Container(ft.Row(controls=[ft.Text(self.feature, width=200),
                         ft.Text(self.data_set.feature[self.feature].mean, width=200),
                         ft.Text(self.data_set.feature[self.feature].std, width=200),
                         ft.Text(self.data_set.feature[self.feature].min, width=200),
                         ft.Text(self.data_set.feature[self.feature].max, width=200)],
                                   vertical_alignment=ft.CrossAxisAlignment.CENTER),
                            on_click=self.on_row_click)


class GetData(ft.UserControl):

    def __init__(self, accept, to_model):
        super(GetData, self).__init__()
        self.accept = accept
        self.data_set = None
        self.to_model = to_model


    def get_dataset_button_click(self, e):
        try:
            with grpc.insecure_channel('localhost:15000') as channel:
                stub = RemouteSmartRieltor_pb2_grpc.EngineerServiceStub(channel)
                data = stub.getData(RemouteSmartRieltor_pb2.Response(code=1))
                self.data_set = genereation_data_from_server(data)
                self.count_values.value = self.data_set.data.shape[0]
                self.date_values.value = datetime.date.today()
                self.data.content = (ft.Column(controls=
                                               [
                                                   FeatureComponent(i, self.data_set, self.visible_plot) for i in self.data_set.feature],
                    scroll=ft.ScrollMode.HIDDEN, height=110))
                self.accept(1)
                self.next_file()
                self.update()
        except:
            self.accept(-1)


    def change_visible_plot(self):
        self.plot_component.visible = False
        self.data_table_component.visible = True
        self.update()

    def visible_plot(self, figure):
        self.plot_component.plot.figure = figure
        self.plot_component.plot.update()
        self.update()
        self.plot_component.visible = True
        self.data_table_component.visible = False
        self.update()

    def save_file(self, e: ft.FilePickerResultEvent):
        self.data_set.data.to_excel(e.path + ".xlsx")

    def next_file(self):
        self.to_model(self.data_set)

    def get_file_picker(self, e: ft.FilePickerResultEvent):
        if e.files != None:
            data = pd.read_excel(e.files[0].path)
            if validation_data.validation_(data, True):
                self.data_set = genereation_data_from_file(data)
                self.count_values.value = self.data_set.data.shape[0]
                self.date_values.value = datetime.date.today()
                self.data.content = (
                    ft.Column(
                        controls=[FeatureComponent(i, self.data_set, self.visible_plot) for i in self.data_set.feature],
                        scroll=ft.ScrollMode.HIDDEN, height=110))
                self.accept(1)
                self.next_file()
                self.update()
            else:
                self.accept(-1)
        else:
            self.accept(-1)
        self.update()

    def get_file_click(self, e):
        self.file_picker.pick_files(allow_multiple=False, allowed_extensions=["xls", "xlsx"])

    def build(self):
        self.file_pickerAdd = ft.FilePicker(on_result=self.save_file)
        self.file_picker = ft.FilePicker(on_result=self.get_file_picker)
        self.count_values = ft.Text()
        self.date_values = ft.Text()
        self.info = ft.Column(controls=
                              [
                                  ft.Text("Информация о датасете"),
                                  ft.Row(controls=[ft.Text("Кол-во записей"), self.count_values]),
                                  ft.Row(controls=[ft.Text("На какую дату"), self.date_values])
                              ])
        self.get_data = ft.ElevatedButton("Запросить данные", on_click=self.get_dataset_button_click)
        self.get_data_from_file = ft.ElevatedButton("Запросить данные из файла", on_click=self.get_file_click)
        self.head = ft.Row(controls=[self.info, ft.Column(controls=[self.get_data, self.get_data_from_file])], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        self.title_f = ft.Container(ft.Row(controls=[ft.Text("Название признака", width=200, weight=ft.FontWeight.BOLD),
                                        ft.Text("Среднее", width=200, weight=ft.FontWeight.BOLD),
                                        ft.Text("Дисперсия", width=200, weight=ft.FontWeight.BOLD),
                                        ft.Text("Минимальное значение", width=200, weight=ft.FontWeight.BOLD),
                                        ft.Text("Маскимальное значение", width=200, weight=ft.FontWeight.BOLD)],
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER),
                                    border=ft.border.only(bottom=ft.border.BorderSide(1, "black")))

        self.data = ft.Container(ft.Column(controls=[], scroll=ft.ScrollMode.HIDDEN, height=110))

        self.save_dataset = ft.OutlinedButton("Сохранить данные на устройстве",
                                              on_click=lambda _: self.file_pickerAdd.save_file(allowed_extensions=["xlsx"]))
        self.basement = ft.Row(controls=[self.save_dataset], alignment=ft.MainAxisAlignment.CENTER)

        self.data_table_component = ft.Column(controls=[
            self.head,
            self.basement,
            self.title_f,
            self.data,
        ],
            alignment=ft.MainAxisAlignment.START,
            spacing=50,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            height=400,
            width=1200)

        self.plot_component = Plot_control(self.change_visible_plot)
        self.plot_component.visible = False

        return ft.Column(controls=[self.file_picker, self.file_pickerAdd, self.data_table_component, self.plot_component])

