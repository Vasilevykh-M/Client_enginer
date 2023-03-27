from sklearn import datasets
from Models.ModelEngineerCatBoost import ModelEngineerCatBoost
from Models.ModelEngineerTorchNN import ModelEngineerTorchNN
from sklearn.model_selection import train_test_split
import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd
import torch.nn as nn


if __name__ == '__main__':
    dataset = datasets.load_iris()
    X = dataset.data
    y = dataset.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)

    #model = ModelEngineerCatBoost("CatBoost", 1, 2)
    #model.fit(X_train, y_train, X_test, y_test, 20)

    model = ModelEngineerTorchNN("TorchNN", nn.Sequential(nn.Linear(4, 1000), nn.ReLU(), nn.Linear(1000, 3)), 50)
    model.fit(X_train, y_train, X_test, y_test, 1000)

    list_name = []
    list_acc_train = []
    list_acc_test = []
    list_f1_train = []
    list_f1_test = []
    list_loss_train = []
    list_loss_test = []
    list_cm = []
    list_label = []

    for i in model.list_models:
        list_name.append(model.list_models[i].iter * 50)
        list_acc_train.append(model.list_models[i].metric.acc_train)
        list_acc_test.append(model.list_models[i].metric.acc_test)
        list_f1_train.append(model.list_models[i].metric.f1_train)
        list_f1_test.append(model.list_models[i].metric.f1_test)
        list_loss_train.append(model.list_models[i].metric.loss_train)
        list_loss_test.append(model.list_models[i].metric.loss_test)
        list_cm.append(model.list_models[i].metric.cm)

    for i in range(len(list_acc_train)):
        list_label.append("train")

    for i in range(len(list_acc_train)):
        list_label.append("test")

    loss_list = list_loss_train + list_loss_test
    acc_list = list_acc_train + list_acc_test
    f1_list = list_f1_train + list_f1_test
    list_name = list_name + list_name

    loss = pd.DataFrame(list(zip(loss_list, list_label, list_name)), columns=["loss", "label", "epoch"])
    acc = pd.DataFrame(list(zip(acc_list, list_label, list_name)), columns=["accuracy", "label", "epoch"])
    f1 = pd.DataFrame(list(zip(f1_list, list_label, list_name)), columns=["f1", "label", "epoch"])

    sns.relplot(data=loss, kind="line", x = "epoch", y="loss", hue="label", marker='o')

    plt.show()
