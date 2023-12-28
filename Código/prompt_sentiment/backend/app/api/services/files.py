import magic, json
import pandas as pd
import numpy as np
import uuid
from flask import current_app

def store_file(file):
    storage_folder = current_app.config.get("STORAGE_FOLDER")
    file_name = file.filename
    file_id = str(uuid.uuid4())
    file_path = storage_folder + file_id + ".bin" 
    file.save(file_path)
    file_info = get_file_info(file_path)
    file_info["file_name"] = file_name
    file_info["file_id"] = file_id
    return file_info

def get_file(file_id):
    storage_folder = current_app.config.get("STORAGE_FOLDER")
    file_path = storage_folder + file_id + ".bin"
    with open(file_path) as file:
        return file.read()

def get_file_info(file_path):
    result = {}
    file_type = magic.from_file(file_path, mime=True)
    file_format = "unknown"
    separator = ""
    header = []
    row_count = 0
    if file_type=="application/json":
        file_format = "json"
        with open(file_path) as file:
            jsfile = json.load(file)
            for key in jsfile[0].keys():
                header.append(key)
            row_count = len(jsfile)
    elif file_type== "text/plain":
        with open(file_path) as file:
            first_line = file.readline().strip()
            if first_line.__contains__('\t'):
                file_format = "tsv"
                separator = '\t'
                header = first_line.split(separator)
            elif first_line.__contains__(','):
                file_format = "csv"
                separator = ','
                header = first_line.split(separator)
            elif first_line.__contains__(';'):
                file_format = "csv"
                separator = ';'
                header = first_line.split(separator)
            row_count = len(file.readlines())
    result["file_format"] = file_format
    result["separator"] = separator
    result["header"] = header
    result["row_count"] = row_count
    return result
