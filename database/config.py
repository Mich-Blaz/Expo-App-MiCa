import yaml
from pydantic import BaseModel,field_validator,model_validator
from typing import Optional
from pathlib import Path


class DataModelApp(BaseModel):
    columns_api : list
    url_api : str


def get_config(conf_file = "config.yml"):
    PATH_CONFIG = Path(__file__).parent / conf_file
    with open(PATH_CONFIG, "r") as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)
    return DataModelApp(**data)