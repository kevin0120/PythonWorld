# https://examples.dask.org/bag.html
import json
from datetime import date, timedelta


def name(i):
    return str(date(2015, 1, 1) + i * timedelta(days=1))


if __name__ == "__main__":
    import dask.bag as db

    b = db.from_sequence([1, 2, 3, 4, 5, 6], npartitions=3)

    print(b.compute())
    print(list(b))

    b.map(json.dumps).to_textfiles("./data/*.json", name_function=name)
