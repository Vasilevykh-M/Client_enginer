from Models.Model import ModelEngineer
import torch
import torch.nn as nn


class Model_NN(torch.nn.Module):
    def __init__(self, layer):
        super(Model_NN, self).__init__()
        self.layer = layer


    def forward(self, X):
        return self.layer(X)


class ModelEngineerTorchNN(ModelEngineer):
    def __init__(self, type, model_architecture, split_epoch):
        super(ModelEngineerTorchNN, self).__init__(type, model_architecture, split_epoch)
        self.model = Model_NN(model_architecture)

    def fit(self, X_train, Y_train, X_test, Y_test, epoch):

        X_train = torch.FloatTensor(X_train)
        X_test = torch.FloatTensor(X_test)

        Y_train = torch.LongTensor(Y_train)
        Y_test = torch.LongTensor(Y_test)


        super(ModelEngineerTorchNN, self).fit(X_train, Y_train, X_test, Y_test, epoch)
        optimizer = torch.optim.AdamW(self.model.parameters(), lr=0.0001)
        loss = nn.CrossEntropyLoss()
        i = 0
        while epoch > 0:
            i += 1
            print(i)

            self.model.train()
            for j in range(self.split_epoch):
                Y_pred_train = self.model(X_train)
                l = loss(Y_pred_train, Y_train)
                l.backward()
                optimizer.step()
                optimizer.zero_grad()

            self.model.eval()
            with torch.no_grad():
                Y_pred_train = self.model(X_train)
                Y_pred_test = self.model(X_test)
                loss_train = loss(Y_pred_train, Y_train).item()
                loss_test = loss(Y_pred_train, Y_train).item()

            Y_pred_train = torch.max(Y_pred_train,1).indices
            Y_pred_test = torch.max(Y_pred_test, 1).indices

            self.calc_log(Y_pred_train, Y_pred_test, Y_train, Y_test, i, loss_train, loss_test)
            torch.save(self.model, "weights_model/torch/torch"+str(i*self.split_epoch))
            epoch -= self.split_epoch


    def predict(self, X):
        super(ModelEngineerTorchNN, self).predict(X)
        return self.model(X)