from sklearn import metrics

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
    def __init__(self, type, model_architecture, split_epoch):
        self.type = type
        self.model_architecture = model_architecture
        self.split_epoch = split_epoch
        self.list_models = {}

    def fit(self, X_train, Y_train, X_text, Y_test, epoch):
        return

    def predict(self, X):
        return

    def calc_log(self, Y_pred_train, Y_pred_test, Y_train, Y_test, i, loss_train = 0, loss_test = 0):
        acc_train = metrics.accuracy_score(Y_train, Y_pred_train)
        acc_test = metrics.accuracy_score(Y_test, Y_pred_test)
        f1_train = metrics.f1_score(Y_train, Y_pred_train, average='micro')
        f1_test = metrics.f1_score(Y_test, Y_pred_test, average='micro')
        if loss_train == 0 and loss_test == 0:
            loss_train = metrics.mean_squared_log_error(Y_train, Y_pred_train)
            loss_test = metrics.mean_squared_log_error(Y_train, Y_pred_train)
        cm = metrics.confusion_matrix(Y_test, Y_pred_test)
        self.list_models[str(i * self.split_epoch)] = (
            "cat_boost" + str(i * self.split_epoch) + ".cbm",
            Log_train(acc_train, acc_test, f1_train, f1_test, loss_train, loss_test, cm)
        )
