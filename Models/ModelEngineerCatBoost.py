from Models.Model import ModelEngineer
from catboost import CatBoostClassifier

class ModelEngineerCatBoost(ModelEngineer):
    def __init__(self, type, split_epoch, depth):
        self.model = CatBoostClassifier(depth = depth, iterations = split_epoch, random_seed=42)
        super(ModelEngineerCatBoost, self).__init__(type, self.model, split_epoch)
        self.depth = depth

    def fit(self, X_train, Y_train, X_text, Y_test, epoch):
        super(ModelEngineerCatBoost, self).fit(X_train, Y_train, X_text, Y_test, epoch)
        i=0
        while epoch > 0:
            i += 1
            self.model = CatBoostClassifier(depth=self.depth, iterations=self.split_epoch*i, random_seed=42)
            self.model.fit(X_train, Y_train, eval_set=(X_text, Y_test))
            Y_pred_train = self.predict(X_train)
            Y_pred_test = self.predict(X_text)
            self.model.save_model("weights_model/cat_boost/cat_boost"+str(i*self.split_epoch))
            self.calc_log(Y_pred_train, Y_pred_test, Y_train, Y_test, i)
            epoch -= self.split_epoch

    def predict(self, X):
        super(ModelEngineerCatBoost, self).predict(X)
        Y = self.model.predict(data=X)
        return Y

