import flet as ft
import grpc
import pandas as pd

import RemouteSmartRieltor_pb2_grpc

import generator_data
import validation_data


def post_data_to_server(data):
    return generator_data.create_genereator_to_post(data)

class SendFile(ft.UserControl):

    def __init__(self, bar_status):
        super(SendFile, self).__init__()
        self.bar_status = bar_status

    def build(self):
        self.file_picker = ft.FilePicker(on_result=self.get_file_picker)
        self.file_name = ft.Text("Файл: ", width=300, height=60, text_align=ft.TextAlign.CENTER)
        self.get_file = ft.ElevatedButton("Выбрать файл и отправить", on_click=self.get_file_click, width=250, height=40)
        return ft.Column(controls=[
            self.file_picker,
            self.file_name,
            self.get_file,
        ],
            alignment = ft.MainAxisAlignment.CENTER,
            spacing = 50,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            height=400,
            width=1200)

    def get_file_picker(self, e: ft.FilePickerResultEvent):
        if e.files != None:
            self.file_name.value = "Файл: " + e.files[0].name

            data = pd.read_excel(e.files[0].path)
            if validation_data.validation_(data):
                data = validation_data.cleanMissingValues(data)
                try:
                    with grpc.insecure_channel('localhost:15000') as channel:
                        stub = RemouteSmartRieltor_pb2_grpc.ClientServiceStub(channel)
                        data = stub.postData(post_data_to_server(data))
                        self.bar_status(data.code)
                except:
                    self.bar_status(-1)
            else:
                self.bar_status(-2)
        self.update()

    def get_file_click(self, e):
        self.file_picker.pick_files(allow_multiple=False, allowed_extensions=["xls", "xlsx"])

