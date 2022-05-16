import os
from os.path import dirname
from pathlib import Path

if __name__ == "__main__":

    my_dir = dirname(__file__)
    print("你输入的内容是: ", my_dir)

    airflow_home_dir = os.environ.get("AIRFLOW_HOME", Path.home() / "airflow")

    print("你输入的内容是: ", airflow_home_dir)

    airflow_sources = str(Path(__file__).parents[2])
    print("你输入的内容是: ", airflow_sources)