import csv
import pickle


class dataload:
    def load(self):
        path_food = 'Food\\food.csv'
        file = open(path_food, 'r', encoding='euc-kr')
        reader = csv.reader(file)
        dic = {}
        for data in reader:
            # eu20180507b
            dic["eu" + data[0] + "a"] = data[1]
            dic["eu" + data[0] + "b"] = data[2]
            dic["eu" + data[0] + "c"] = data[3]

            """
            dic[data[0] + "breakfast_en"] = data[1]
            dic[data[0] + "lunch_en"] = data[2]
            dic[data[0] + "dinner_en"] = data[3]
            """
        print(dic)
        file.close()

        f = open("dic.dat", "wb")
        pickle.dump(dic, f)
        f.close()


        return dic
