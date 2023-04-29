from Models.Model import ModelEngineer
from Models.Model import Metadata
from catboost import CatBoostClassifier

class ModelEngineerCatBoost(ModelEngineer):
    def __init__(self, type, split_epoch, depth):
        self.model = CatBoostClassifier(depth = depth, iterations = split_epoch, random_seed=42, allow_const_label=True)
        super(ModelEngineerCatBoost, self).__init__(type, self.model, split_epoch)
        self.depth = depth

    def fit(self, X_train, Y_train, X_text, Y_test, epoch):
        super(ModelEngineerCatBoost, self).fit(X_train, Y_train, X_text, Y_test, epoch)
        i=0
        while epoch > 0:
            i += 1
            self.model = CatBoostClassifier(depth=self.depth, iterations=self.split_epoch*i, random_seed=42, allow_const_label=True)
            self.model.fit(X_train, Y_train, eval_set=(X_text, Y_test))
            Y_pred_train = self.predict(X_train)
            Y_pred_test = self.predict(X_text)
            metric = self.calc_metrics(Y_pred_train, Y_pred_test, Y_train, Y_test)
            metadata = Metadata(i, "CatBoost", metric, self.model)
            self.list_models["CatBoost" + str(i)] = metadata
            self.model.save_model("weights_model/cat_boost/CatBoost" + str(i) + ".cbm")
            epoch -= self.split_epoch

    def predict(self, X):
        super(ModelEngineerCatBoost, self).predict(X)
        Y = self.model.predict(data=X)
        return Y

