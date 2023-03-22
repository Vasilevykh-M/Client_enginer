from Models.Model import ModelEngineer
from Models.Model import Log_train
import torch
import torch.nn as nn
from sklearn import metrics


class Model_NN(torch.nn.Module):
    def __init__(self, layer):
        super(Model_NN, self).__init__()
        self.layer = layer


    def forward(self, X):
        return self.layer(X)


class ModelEngineerTorchNN(ModelEngineer):
    def __init__(self, type, model_architecture):
        super(ModelEngineerTorchNN, self).__init__(type, model_architecture)
        self.model = Model_NN(model_architecture)

    def fit(self, X_train, Y_train, X_test, Y_test, epoch, split_epoch):

        X_train = torch.FloatTensor(X_train)
        X_test = torch.FloatTensor(X_test)

        Y_train = torch.LongTensor(Y_train)
        Y_test = torch.LongTensor(Y_test)


        super(ModelEngineerTorchNN, self).fit(X_train, Y_train, X_test, Y_test, epoch, split_epoch)
        optimizer = torch.optim.AdamW(self.model.parameters(), lr=0.0001)
        loss = nn.CrossEntropyLoss()
        i = 0
        while epoch > 0:
            i += 1

            for i in range(split_epoch):
                Y_pred_train = self.model(X_train)
                l = loss(Y_pred_train, Y_train)
                l.backward()
                optimizer.step()
                optimizer.zero_grad()

            with torch.no_grad():
                Y_pred_train = self.model(X_train)
                Y_pred_test = self.model(X_test)

            Y_pred_train = torch.max(Y_pred_train,1).indices
            Y_pred_test = torch.max(Y_pred_test, 1).indices

            acc_train = metrics.accuracy_score(Y_train, Y_pred_train)
            acc_test = metrics.accuracy_score(Y_test, Y_pred_test)
            f1_train = metrics.f1_score(Y_train, Y_pred_train, average='micro')
            f1_test = metrics.f1_score(Y_test, Y_pred_test, average='micro')
            loss_train = metrics.mean_squared_log_error(Y_train, Y_pred_train)
            loss_test = metrics.mean_squared_log_error(Y_train, Y_pred_train)
            cm = metrics.confusion_matrix(Y_test, Y_pred_test)
            torch.save(self.model, "weights_model/torch"+str(i*split_epoch))
            self.list_models[str(i * split_epoch)] = (
                "cat_boost" + str(i * split_epoch) + ".cbm",
                Log_train(acc_train, acc_test, f1_train, f1_test, loss_train, loss_test, cm)
            )
            epoch -= split_epoch


    def predict(self, X):
        super(ModelEngineerTorchNN, self).predict(X)
        return self.model(X)