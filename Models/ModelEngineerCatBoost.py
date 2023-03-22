from Models.Model import ModelEngineer
from Models.Model import Log_train
from catboost import CatBoostClassifier
from sklearn import metrics

class ModelEngineerCatBoost(ModelEngineer):
    def __init__(self, type, split_epoch, depth):
        self.model = CatBoostClassifier(depth = depth, iterations = split_epoch, random_seed=42)
        super(ModelEngineerCatBoost, self).__init__(type, self.model)
        self.depth = depth
        self.split_epoch = split_epoch

    def fit(self, X_train, Y_train, X_text, Y_test, epoch):
        super(ModelEngineerCatBoost, self).fit(X_train, Y_train, X_text, Y_test, epoch, self.split_epoch)
        i=0
        while epoch > 0:
            i += 1
            self.model = CatBoostClassifier(depth=self.depth, iterations=self.split_epoch*i, random_seed=42)
            self.model.fit(X_train, Y_train, eval_set=(X_text, Y_test))
            Y_pred_train = self.predict(X_train)
            Y_pred_test = self.predict(X_text)
            acc_train = metrics.accuracy_score(Y_train, Y_pred_train)
            acc_test = metrics.accuracy_score(Y_test, Y_pred_test)
            f1_train = metrics.f1_score(Y_train, Y_pred_train, average='micro')
            f1_test = metrics.f1_score(Y_test, Y_pred_test, average='micro')
            loss_train = metrics.mean_squared_log_error(Y_train, Y_pred_train)
            loss_test = metrics.mean_squared_log_error(Y_train, Y_pred_train)
            cm = metrics.confusion_matrix(Y_test, Y_pred_test)
            self.model.save_model("cat_boost/weights_model/cat_boost"+str(i*self.split_epoch))
            self.list_models[str(i*self.split_epoch)] = (
                "cat_boost"+str(i*self.split_epoch) + ".cbm",
                Log_train(acc_train, acc_test, f1_train, f1_test, loss_train, loss_test, cm)
            )
            epoch -= self.split_epoch

    def predict(self, X):
        super(ModelEngineerCatBoost, self).predict(X)
        Y = self.model.predict(data=X)
        return Y

