# from sklearn import datasets
#
# from DataSet import DataSet
# from Models.ModelEngineerCatBoost import ModelEngineerCatBoost
# from Models.ModelEngineerTorchNN import ModelEngineerTorchNN
# from sklearn.model_selection import train_test_split
# import seaborn as sns
# from matplotlib import pyplot as plt
# import pandas as pd
# import torch.nn as nn
#
# import grpc
# import RemouteSmartRieltor_pb2_grpc
# import RemouteSmartRieltor_pb2
#
# def modelDictTorch():
#     dict_ = {}
#     dict_["1"] = RemouteSmartRieltor_pb2.Layer(input = 14, output = 1000, dropout = False)
#     dict_["2"] = RemouteSmartRieltor_pb2.Layer(input = 1000, output = 2, dropout = False)
#     with open("weights_model/torch/Torch20.pth", 'rb') as f:
#         return RemouteSmartRieltor_pb2.TorchModel(layers = dict_, weights = f.read())
#
# def modelDictCatBoost():
#     with open("weights_model/cat_boost/CatBoost20.cbm", 'rb') as f:
#         return RemouteSmartRieltor_pb2.CatBoostModel(weights = f.read())
#
# def get_data():
#     return
#
# def post_stat(features):
#     request = {}
#     for i in features:
#         request[i] = RemouteSmartRieltor_pb2.StatFeature(std = features[i].std, mean = features[i].mean)
#     return RemouteSmartRieltor_pb2.Stat(Stat = request)
#
# def create_data():
#     data = pd.read_excel('FILE.xlsx')
#     data_set = DataSet.DataSet(data, {})
#     data_set.pre_data()
#     return data_set
#
# def train_get_data(data_set):
#     X = data_set.data[data_set.data.columns.difference(['СледующийСтатус'])]
#     Y = data_set.data['СледующийСтатус']
#     X = X.to_numpy()
#     Y = Y.to_numpy()
#     return train_test_split(X, Y, test_size=0.30)
#
# if __name__ == '__main__':
#     # data_set = create_data()
#     # X_train, X_test, y_train, y_test = train_get_data(data_set)
#     # #model = ModelEngineerCatBoost("CatBoost", 1, 2)
#     # #model.fit(X_train, y_train, X_test, y_test, 20)
#     #
#     # model = ModelEngineerTorchNN("TorchNN", nn.Sequential(nn.Linear(14, 1000), nn.ReLU(), nn.Linear(1000, 2)), 50)
#     # model.fit(X_train, y_train, X_test, y_test, 1000)
#     #
#     # list_name = []
#     # list_acc_train = []
#     # list_acc_test = []
#     # list_f1_train = []
#     # list_f1_test = []
#     # list_loss_train = []
#     # list_loss_test = []
#     # list_cm = []
#     # list_label = []
#     #
#     # for i in model.list_models:
#     #     list_name.append(model.list_models[i].iter * 50)
#     #     list_acc_train.append(model.list_models[i].metric.acc_train)
#     #     list_acc_test.append(model.list_models[i].metric.acc_test)
#     #     list_f1_train.append(model.list_models[i].metric.f1_train)
#     #     list_f1_test.append(model.list_models[i].metric.f1_test)
#     #     list_loss_train.append(model.list_models[i].metric.loss_train)
#     #     list_loss_test.append(model.list_models[i].metric.loss_test)
#     #     list_cm.append(model.list_models[i].metric.cm)
#     #
#     # for i in range(len(list_acc_train)):
#     #     list_label.append("train")
#     #
#     # for i in range(len(list_acc_train)):
#     #     list_label.append("test")
#     #
#     # loss_list = list_loss_train + list_loss_test
#     # acc_list = list_acc_train + list_acc_test
#     # f1_list = list_f1_train + list_f1_test
#     # list_name = list_name + list_name
#     #
#     # loss = pd.DataFrame(list(zip(loss_list, list_label, list_name)), columns=["loss", "label", "epoch"])
#     # acc = pd.DataFrame(list(zip(acc_list, list_label, list_name)), columns=["accuracy", "label", "epoch"])
#     # f1 = pd.DataFrame(list(zip(f1_list, list_label, list_name)), columns=["f1", "label", "epoch"])
#     # # sns.relplot(data=loss, kind="line", x = "epoch", y="loss", hue="label", marker='o')
#     # #
#     # # plt.show()
#
#
#
#     with grpc.insecure_channel('localhost:15000') as channel:
#         stub = RemouteSmartRieltor_pb2_grpc.EngineerServiceStub(channel)
#         # data2 = stub.postStat(post_stat(data_set.feature))
#         # data = stub.postTorchModel(modelDictTorch())
#         #data = stub.postCatBoostModel(modelDictCatBoost())
#         data = stub.getData(RemouteSmartRieltor_pb2.Response(code = 1))
#         for i in data:
#             print(i.KeyRate)
#         print("Greeter client received: " + str(data.code))
#

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