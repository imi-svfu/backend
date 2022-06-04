import datetime

def get(pair_num):
    result = dict()
    pairtime_begin = {
        1: datetime.time(8, 0),
        2: datetime.time(9, 50),
        3: datetime.time(11, 40),
        4: datetime.time(14, 00),
        5: datetime.time(15, 50),
        6: datetime.time(17, 40)
    }
    pairtime_end = {
        1: datetime.time(9, 35),
        2: datetime.time(11, 25),
        3: datetime.time(13, 15),
        4: datetime.time(15, 35),
        5: datetime.time(17, 25),
        6: datetime.time(19, 15)
    }

    result['begin'] = pairtime_begin[pair_num]
    result['end'] = pairtime_end[pair_num]

    return result
