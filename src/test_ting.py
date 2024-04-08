import datetime 

def time_format_now():
    query = datetime.datetime.now().replace(microsecond=0,second=0,minute=0)
    # print(query)
    query = str(query).replace(' ','T')+'+00:00'
    return query


if __name__ == "__main__":
    test = time_format_now()
    print(test)
