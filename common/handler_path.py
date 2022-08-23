import os
from datetime import datetime

ts = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_path():
    # return os.path.join(dir_path, "tests")
    return os.path.join(dir_path)


def data_path():
    return os.path.join(dir_path, "data")


def logs_path():
    return os.path.join(dir_path, "logs")


def reports_path():
    return os.path.join(dir_path, r"reports\reports-{}.html".format(ts))


def config_path():
    return os.path.join(dir_path, "config")


if __name__ == "__main__":
    print(dir_path)
    print(test_path())
    print(data_path())
    print(logs_path())
    print(reports_path())
    print(config_path())
