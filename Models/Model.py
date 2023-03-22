class Log_train:
    def __init__(self, acc_train, acc_test, f1_train, f1_test, loss_train, loss_test, cm):
        self.acc_train = acc_train
        self.acc_test = acc_test
        self.f1_train = f1_train
        self.f1_test = f1_test
        self.loss_train = loss_train
        self.loss_test = loss_test
        self.cm = cm


class ModelEngineer:
    def __init__(self, type, model_architecture):
        self.type = type
        self.model_architecture = model_architecture
        self.list_models = {}

    def fit(self, X_train, Y_train, X_text, Y_test, epoch, split_epoch):
        return

    def predict(self, X):
        return
