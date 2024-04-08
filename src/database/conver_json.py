import datetime
import json


def conver_to_json(dictionary):

    wd_json_data = json.dumps(dictionary, indent=4, sort_keys=True, default=str)

    return wd_json_data




if __name__ == "__main__":

    tall = [1, 2, 3]
    time = [datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now()]

    dict_test = dict(zip(tall, time))

    wd_json_data = conver_to_json(dict_test)

    print(wd_json_data)

    