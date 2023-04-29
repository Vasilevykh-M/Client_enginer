import pandas as pd

import RemouteSmartRieltor_pb2_grpc
import RemouteSmartRieltor_pb2

from DataSet.DataSet import DataSet
from DataSet.DataSet import FeatureNum

def create_genereator_to_post(df):
    for i, data in df.iterrows():
        yield RemouteSmartRieltor_pb2.Data(
            Booking = RemouteSmartRieltor_pb2.Booking(
                BookingDate = str(data["ДатаБрони"]),
                BookingTime = str(data["ВремяБрони"]),
                BookingSource = data["ИсточникБрони"],
                BookingTemporary = data["ВременнаяБронь"],
                City = data["Город"],
                TypeRoom = data["ВидПомещения"],
                TypeObject = data["Тип"],
                Area = int(data["ПродаваемаяПлощадь"]),
                Floor = int(data["Этаж"]),
                Cost = int(data["СтоимостьНаДатуБрони"]),
                TypeCost = data["ТипСтоимости"],
                PaymentOption = data["ВариантОплаты"],
                PaymentOptionAdditional = data["ВариантОплатыДоп"],
                Discount = int(data["СкидкаНаКвартиру"]),
                ActualCost = int(data["ФактическаяСтоимостьПомещения"]),
                DealAN = data["СделкаАН"],
                InvestmentProduct = data["ИнвестиционныйПродукт"],
                Privilege = data["Привилегия"],
                LeadStatus = data["Статус лида (из CRM)"],
            ),
            StateBooking = RemouteSmartRieltor_pb2.StateBooking(StateBooking = data["СледующийСтатус"])
        )

def genereation_data_from_server(data):
    dict_data = {
                    "ДатаБрони": [], "ВремяБрони": [], "ИсточникБрони": [],
                    "ВременнаяБронь": [], "Город": [], "ВидПомещения": [],
                    "Тип": [], "ПродаваемаяПлощадь": [], "Этаж": [],
                    "СтоимостьНаДатуБрони": [], "ТипСтоимости": [], "ВариантОплаты": [],
                    "ВариантОплатыДоп": [], "СкидкаНаКвартиру": [], "ФактическаяСтоимостьПомещения": [],
                    "СделкаАН": [], "ИнвестиционныйПродукт": [], "Привилегия": [],
                    "Статус лида (из CRM)": [], "СледующийСтатус": [], "КлючеваяСтавка": []
    }
    for i in data:
        dict_data["ДатаБрони"].append(int(i.Data.Booking.BookingDate[5:7]))
        dict_data["ВремяБрони"].append(int(i.Data.Booking.BookingTime[:2]))
        dict_data["ИсточникБрони"].append(i.Data.Booking.BookingSource)
        dict_data["ВременнаяБронь"].append(i.Data.Booking.BookingTemporary)
        dict_data["Город"].append(i.Data.Booking.City)
        dict_data["ВидПомещения"].append(i.Data.Booking.TypeRoom)
        dict_data["Тип"].append(i.Data.Booking.TypeObject)
        dict_data["ПродаваемаяПлощадь"].append(i.Data.Booking.Area)
        dict_data["Этаж"].append(i.Data.Booking.Floor)
        dict_data["СтоимостьНаДатуБрони"].append(i.Data.Booking.Cost)
        dict_data["ТипСтоимости"].append(i.Data.Booking.TypeCost)
        dict_data["ВариантОплаты"].append(i.Data.Booking.PaymentOption)
        dict_data["ВариантОплатыДоп"].append(i.Data.Booking.PaymentOptionAdditional)
        dict_data["СкидкаНаКвартиру"].append(i.Data.Booking.Discount)
        dict_data["ФактическаяСтоимостьПомещения"].append(i.Data.Booking.ActualCost)
        dict_data["СделкаАН"].append(i.Data.Booking.DealAN)
        dict_data["ИнвестиционныйПродукт"].append(i.Data.Booking.InvestmentProduct)
        dict_data["Привилегия"].append(i.Data.Booking.Privilege)
        dict_data["Статус лида (из CRM)"].append(i.Data.Booking.LeadStatus)
        dict_data["СледующийСтатус"].append(i.Data.StateBooking.StateBooking)
        dict_data["КлючеваяСтавка"].append(i.KeyRate)

    data_frame = pd.DataFrame.from_dict(dict_data)

    data_set = DataSet(data_frame, {})
    data_set.pre_data()

    return data_set

def genereation_data_from_file(data):
    data=data[["ДатаБрони", "ВремяБрони", "ИсточникБрони", "ВременнаяБронь", "Город", "ВидПомещения",
               "Тип", "ПродаваемаяПлощадь", "Этаж", "СтоимостьНаДатуБрони", "ТипСтоимости", "ВариантОплаты",
               "ВариантОплатыДоп", "СкидкаНаКвартиру", "ФактическаяСтоимостьПомещения", "СделкаАН",
               "ИнвестиционныйПродукт", "Привилегия", "Статус лида (из CRM)", "СледующийСтатус"]]
    data['ДатаБрони'] = data['ДатаБрони'].dt.strftime('%m').astype('int')
    data['ВремяБрони'] = data['ВремяБрони'].map(lambda x: x.hour)
    data_set = DataSet(data, {})
    data_set.pre_data()
    return data_set