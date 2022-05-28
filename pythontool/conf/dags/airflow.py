import datetime

# from airflow.utils import dates

if __name__ == "__main__":
    cur = datetime.datetime.now()
    print(cur)
    # print(dates.days_ago(1))
    print(datetime.timedelta(minutes=60))
    print(datetime.datetime(2022, 5, 21))
