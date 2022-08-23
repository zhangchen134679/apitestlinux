import yaml


def read_yaml(file):
    with open(file, mode="r", encoding="utf-8") as f:
        conf = yaml.load(f, Loader=yaml.SafeLoader)
        return conf






