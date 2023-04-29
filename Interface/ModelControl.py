import grpc
import matplotlib
import pandas as pd
import torch
from flet_core.matplotlib_chart import MatplotlibChart
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
import flet as ft

import os

import RemouteSmartRieltor_pb2
import RemouteSmartRieltor_pb2_grpc
from Models.ModelEngineerCatBoost import ModelEngineerCatBoost
from Models.ModelEngineerTorchNN import ModelEngineerTorchNN

def post_stat(features):
    request = {}
    for i in features:
        request[i] = RemouteSmartRieltor_pb2.StatFeature(std = features[i].std, mean = features[i].mean)
    return RemouteSmartRieltor_pb2.Stat(Stat = request)

def train_get_data(data_set):
    X = data_set.data[data_set.data.columns.difference(['СледующийСтатус'])]
    Y = data_set.data['СледующийСтатус']
    X = X.to_numpy()
    Y = Y.to_numpy()
    return train_test_split(X, Y, test_size=0.30)


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

class Layer(ft.UserControl):
    def __init__(self, ci, co, do, name, edit_layer, delete_layer):
        super(Layer, self).__init__()
        self.name = name
        self.ci = ci
        self.co = co
        self.do = do
        self.edit_layer = edit_layer
        self.delete_layer = delete_layer

    def edit_layer_in_list(self, e):
        self.edit_layer(int(self.input.value), int(self.output.value), bool(self.dropout.value), self.name)

    def delete_layer__in_list(self, e):
        self.delete_layer(self.name)

    def build(self):
        self.input = ft.TextField(value=str(self.ci), width=200)
        self.output = ft.TextField(value=str(self.co), width=200)
        self.dropout = ft.Dropdown(
            options=[ft.dropdown.Option(True), ft.dropdown.Option(False)],
            value=self.do if self.do != None else None,
            width=200)
        self.edit = ft.IconButton(icon=ft.icons.EDIT, on_click = self.edit_layer_in_list)
        self.delete = ft.IconButton(icon=ft.icons.DELETE, on_click=self.delete_layer__in_list)
        return ft.Row(controls=[self.input, self.output, self.dropout, self.edit, self.delete], vertical_alignment=ft.CrossAxisAlignment.CENTER)

class Layer_add(ft.UserControl):

    def __init__(self, add_layer):
        super(Layer_add, self).__init__()
        self.add_layer = add_layer

    def add_layer_in_list(self, e):
        self.add_layer(int(self.input.value), int(self.output.value), bool(self.dropout.value))
        self.update()

    def build(self):
        self.input = ft.TextField(width=200)
        self.output = ft.TextField(width=200)
        self.dropout = ft.Dropdown(
            options=[ft.dropdown.Option(True), ft.dropdown.Option(False)],
            width=200)
        self.add = ft.IconButton(icon=ft.icons.ADD, on_click=self.add_layer_in_list)
        return ft.Row(controls=[self.input, self.output, self.dropout, self.add], vertical_alignment=ft.CrossAxisAlignment.CENTER)

class Tree(ft.UserControl):
    def build(self):
        self.max_depth = ft.TextField(label="Максимальная глубина дерева")
        return self.max_depth


class Model(ft.UserControl):

    def __init__(self, accept, show_banner, data_set = None):
        super(Model, self).__init__()
        self.accept = accept
        self.data_set = data_set
        self.count_layer = 1
        self.model_dict = {
            "f": RemouteSmartRieltor_pb2.Layer(input = 14, output = 1000, dropout = False),
            "l": RemouteSmartRieltor_pb2.Layer(input = 1000, output = 2, dropout = False)
        }
        self.show_banner = show_banner
        self.Model = None
        self.list_name = []
        self.list_acc_train = []
        self.list_acc_test = []
        self.list_f1_train = []
        self.list_f1_test = []
        self.list_loss_train = []
        self.list_loss_test = []
        self.list_label = []


    def list_layers(self):
        l = []
        for i in self.model_dict:
            if i != "f" and i !="l":
                l.append(Layer(self.model_dict[i].input, self.model_dict[i].output, self.model_dict[i].dropout, i,
                               self.edit_layer, self.delete_layer))
        l.append(Layer_add(self.add_layer))
        return l

    def add_layer(self, io, ou, dr):
        self.model_dict[str(self.count_layer)] = RemouteSmartRieltor_pb2.Layer(input = io, output = ou, dropout = dr)
        self.data.content.controls = self.list_layers()
        self.count_layer += 1
        self.update()

    def edit_layer(self, io, ou, dr, name):
        self.model_dict[name] = RemouteSmartRieltor_pb2.Layer(input=io, output=ou, dropout=dr)
        self.data.content.controls = self.list_layers()
        self.update()

    def delete_layer(self, name):
        self.model_dict.pop(name)
        self.data.content.controls = self.list_layers()
        self.update()

    def f(self, e):
        self.accept(1)
        self.update()

    def focus_model(self, e):
        if self.type_model.value == "Нейронная сеть":
            self.title_f.visible = True
            self.data.visible = True
            self.tree.visible = False

        if self.type_model.value == "Градиентный бустинг":
            self.title_f.visible = False
            self.data.visible = False
            self.tree.visible = True
        self.update()

    def fit_model(self, e):
        if self.count_epoch.value == "":
            self.show_banner()
            return

        if self.type_model.value == "Нейронная сеть":
            start = None
            end = None
            for i in self.model_dict:
                if i != "f" and i != "l":
                    end = self.model_dict[i]
                    if start == None:
                        start = self.model_dict[i]
                        continue
                    if start.output != end.input:
                        self.show_banner()
                        return
                    start = end

        if self.type_model.value == "Градиентный бустинг":
            if self.tree.max_depth.value == "":
                self.show_banner()
                return

        X_train, X_test, y_train, y_test = train_get_data(self.data_set)

        if self.type_model.value == "Нейронная сеть":

            i = min(self.model_dict.keys())
            self.model_dict["f"].output = self.model_dict[i].input

            a = list(self.model_dict.keys())
            a.remove("f")
            a.remove("l")
            j = max(a)

            self.model_dict["l"].input = self.model_dict[j].output
            self.Model = ModelEngineerTorchNN("TorchNN", torch.nn.Sequential(), 50)

            self.Model.model.layer = torch.nn.Sequential(torch.nn.Linear(self.model_dict["f"].input, self.model_dict["f"].output))
            for i in self.model_dict:
                if i == "f" or i =="l":
                    continue
                self.Model.model.layer.append(torch.nn.Linear(self.model_dict[i].input, self.model_dict[i].output))
                if self.model_dict[i].dropout:
                    self.Model.model.layer.append(torch.nn.Dropout())
                self.Model.model.layer.append(torch.nn.ReLU())

            self.Model.model.layer.append(torch.nn.Linear(self.model_dict["l"].input, self.model_dict["l"].output))
            self.Model.model.layer.append(torch.nn.ReLU())

            for i in self.model_dict:
                print(i)

        if self.type_model.value == "Градиентный бустинг":
            self.Model= ModelEngineerCatBoost("CatBoost", 50, int(self.tree.max_depth.value))

        self.Model.fit(X_train, y_train, X_test, y_test, int(self.count_epoch.value))
        self.stat.disabled = False

        self.list_name = []
        self.list_acc_train = []
        self.list_acc_test = []
        self.list_f1_train = []
        self.list_f1_test = []
        self.list_loss_train = []
        self.list_loss_test = []
        self.list_label = []

        for i in self.Model.list_models:
            self.list_name.append(self.Model.list_models[i].iter * 50)
            self.list_acc_train.append(self.Model.list_models[i].metric.acc_train)
            self.list_acc_test.append(self.Model.list_models[i].metric.acc_test)
            self.list_f1_train.append(self.Model.list_models[i].metric.f1_train)
            self.list_f1_test.append(self.Model.list_models[i].metric.f1_test)
            self.list_loss_train.append(self.Model.list_models[i].metric.loss_train)
            self.list_loss_test.append(self.Model.list_models[i].metric.loss_test)

        for i in range(len(self.list_acc_train)):
            self.list_label.append("train")

        for i in range(len(self.list_acc_train)):
            self.list_label.append("test")

        if self.type_model.value == "Нейронная сеть":
            self.model.options = [ft.dropdown.Option(i) for i in os.listdir('weights_model/torch')]

        if self.type_model.value == "Градиентный бустинг":
            self.model.options = [ft.dropdown.Option(i) for i in os.listdir('weights_model/cat_boost')]

        self.update()

    def acc_plot(self, e):
        fig, axs = plt.subplots()
        axs.plot(self.list_name, self.list_acc_train, self.list_name, self.list_acc_test)
        axs.set_xlabel("Epoch")
        axs.set_ylabel("Accuracy")
        axs.set_title("Accuracy")
        axs.grid(True)

        self.plot_component.plot.figure = fig
        self.plot_component.plot.update()
        self.update()
        self.plot_component.visible = True
        self.data_table_component.visible = False
        self.update()

    def f1_plot(self, e):
        fig, axs = plt.subplots()
        axs.plot(self.list_name, self.list_f1_train, self.list_name, self.list_f1_test)
        axs.set_xlabel("Epoch")
        axs.set_ylabel("F1")
        axs.set_title("F1")
        axs.grid(True)

        self.plot_component.plot.figure = fig
        self.plot_component.plot.update()
        self.update()
        self.plot_component.visible = True
        self.data_table_component.visible = False
        self.update()


    def loss_plot(self, e):
        fig, axs = plt.subplots()
        axs.plot(self.list_name, self.list_loss_train, self.list_name, self.list_loss_test)
        axs.set_xlabel("Epoch")
        axs.set_ylabel("Loss")
        axs.set_title("Loss")
        axs.grid(True)

        self.plot_component.plot.figure = fig
        self.plot_component.plot.update()
        self.update()
        self.plot_component.visible = True
        self.data_table_component.visible = False
        self.update()

    def change_visible_plot(self):
        self.plot_component.visible = False
        self.data_table_component.visible = True
        self.update()

    def dict_torch(self):
        with open("weights_model/torch/" + self.model.value, 'rb') as f:
            return RemouteSmartRieltor_pb2.TorchModel(layers = self.model_dict, weights = f.read())

    def dict_catboost(self):
        with open("weights_model/cat_boost/" + self.model.value, 'rb') as f:
            return RemouteSmartRieltor_pb2.CatBoostModel(weights = f.read())

    def send_model_to_server(self, e):
        try:
            with grpc.insecure_channel('localhost:15000') as channel:
                stub = RemouteSmartRieltor_pb2_grpc.EngineerServiceStub(channel)
                data = stub.postStat(post_stat(self.data_set.feature))
        except:
            self.accept(-1)


        if self.type_model.value == "Нейронная сеть":

            self.model_dict["0"] = self.model_dict["f"]
            self.model_dict[str(self.count_layer + 1)] = self.model_dict["l"]
            self.model_dict.pop("f")
            self.model_dict.pop("l")

            self.model_dict = dict(sorted(self.model_dict.items()))

            try:
                with grpc.insecure_channel('localhost:15000') as channel:
                        stub = RemouteSmartRieltor_pb2_grpc.EngineerServiceStub(channel)
                        data = stub.postTorchModel(self.dict_torch())
                        self.accept(1)

                        self.model_dict = {
                            "f": RemouteSmartRieltor_pb2.Layer(input=14, output=1000, dropout=False),
                            "l": RemouteSmartRieltor_pb2.Layer(input=1000, output=2, dropout=False)
                        }
            except:
                self.accept(-1)

        if self.type_model.value == "Градиентный бустинг":
            try:
                with open("weights_model/cat_boost/" + self.model.value, 'rb') as f:
                    with grpc.insecure_channel('localhost:15000') as channel:
                        stub = RemouteSmartRieltor_pb2_grpc.EngineerServiceStub(channel)
                        data = stub.postCatBoostModel(self.dict_catboost())
                        self.accept(1)
            except:
                self.accept(-1)

    def build(self):
        self.type_model = ft.Dropdown(
            label="Выберите тип модели",
            options=[
                ft.dropdown.Option("Градиентный бустинг"),
                ft.dropdown.Option("Нейронная сеть")],
            on_change=self.focus_model
        )

        self.train = ft.ElevatedButton("Обучить", on_click=self.fit_model)
        self.count_epoch = ft.TextField(label="Кол-во эпох")

        self.loss_curve = ft.ElevatedButton("Построить график ошибки", on_click=self.loss_plot)
        self.acc_curve = ft.ElevatedButton("Построить график точности", on_click=self.acc_plot)
        self.f1_curve = ft.ElevatedButton("Построить график f1 меры", on_click=self.f1_plot)
        self.stat = ft.Column(controls=[self.loss_curve, self.acc_curve, self.f1_curve])
        self.stat.disabled = True

        self.model = ft.Dropdown(
            label="Выберите модель",
            options=[])

        self.send_model = ft.ElevatedButton("Отправить модель", on_click=self.send_model_to_server)

        self.info = ft.Column(controls=[
            self.type_model,
            ft.Row(controls=[self.train,  self.count_epoch]),
            self.stat,
            self.model,
            self.send_model])


        self.tree = Tree()
        self.tree.visible = False

        self.title_f = ft.Container(ft.Row(controls=[ft.Text("Входы", width=200, weight=ft.FontWeight.BOLD),
                                        ft.Text("Выходы", width=200, weight=ft.FontWeight.BOLD),
                                        ft.Text("Dropout", width=200, weight=ft.FontWeight.BOLD)],
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER),
                                    border=ft.border.only(bottom=ft.border.BorderSide(1, "black")))
        self.title_f.visible = False


        self.data = ft.Container(ft.Column(controls=[Layer_add(self.add_layer)], scroll=ft.ScrollMode.HIDDEN, height=400))
        self.data.visible = False

        self.plot_component = Plot_control(self.change_visible_plot)
        self.plot_component.visible = False

        self.data_table_component = ft.Row(controls=[
            self.info,
            ft.Column(controls=[self.title_f, self.data]),
            self.tree,
        ],
            alignment=ft.MainAxisAlignment.START,
            spacing=50,
            height=400,
            width=1200)

        return ft.Column(controls=[
            self.data_table_component,
            self.plot_component,
        ])