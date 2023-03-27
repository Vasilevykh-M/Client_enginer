#list_feature =
# [
# 'ДатаБрони', 'ПродаваемаяПлощадь',
# 'Этаж', 'СтоимостьНаДатуБрони',
# 'ФактическаяСтоимостьПомещения',	'ЦенаЗаКвМетр',
# 'ВремяБрони', 'СкидкаНаКвартиру', 'КлючеваяСтавка'
# ]

class Feature:
    def __init__(self, name, count):
        self.name = name
        self.count = count


class FeatureCat(Feature):
    def __init__(self, name, count, values, assignment):
        super(FeatureCat, self).__init__(name, count)
        self.values = values
        self.assignment = assignment


class FeatureNum(Feature):
    def __init__(self, name, count, std, mean):
        super(FeatureNum, self).__init__(name, count)
        self.std = std
        self.mean = mean


class DataSet:
    def __init__(self, data, feature):
        self.data = data
        self.feature = feature

    def clean_missing_values(self):
        self.data = self.data.fillna(
            value={
                'Этаж':0,
                'СкидкаНаКвартиру': 0,
                'СледующийСтатус': 'В резерве',
                'ВариантОплатыДоп': 'нет'
            }
        )

    def calc_stat(self, list_feature):
        for i in list_feature:
            self.feature[i].std = self.data[i].std()
            self.feature[i].std = self.data[i].mean()

    def normalization(self, list_feature):
        for i in list_feature:
            self.data[i] = (self.data[i] - self.feature[i].mean) / self.feature[i].std

    def cat_features(self, list_feature):
        for i in list_feature:
            self.data[i] = self.data[i].astype('category')
            self.data[i] = self.data[i].cat.codes
            self.data.drop(columns=[i], axis=1, inplace=True)

    def hash_codes(self, list_feature):
        for i in list_feature:
            self.data[i] = self.data[i].map(lambda x: hash(x)%100)
