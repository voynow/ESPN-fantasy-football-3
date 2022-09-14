import json
from os import stat
from utils import configs


def split_on_newline(raw_data):
    """
    Utility function for data preparation
    split raw text on newline characters - semistructuring the text objects
    """
    for key in raw_data:
        raw_data[key] = raw_data[key].replace("\n\n\n", "\n\n")
        raw_data[key] = raw_data[key].split("\n\n")

    for key in raw_data:
        data_split = []
        for item in raw_data[key]:
            data_split.append(item.split("\n"))
        raw_data[key] = data_split

    return raw_data


def prep_raw_data(raw_loc):
    """
    Open raw json and collect data relevant for transformation
    """
    master_raw_data = json.load(open(raw_loc, 'rb'))
    raw_data = {k: v['data'] for k, v in master_raw_data.items()}
    raw_data = split_on_newline(raw_data)
    return master_raw_data, raw_data


def group(data):
    """
    Separate raw data into groups defined in configs.table_names
    header group accessed by index (0th and 2nd row of raw data)
    other groups accessed by string search
    """
    player_dict = {}
    player_dict[configs.table_names[0]] = data[0] + data[2]

    for row in data:
        for string in configs.table_names:
            if row[0] == string:
                string_key = string.replace(" ", "_").lower()
                player_dict[string_key] = row
    
    return player_dict


def transform():
    """
    Pipeline for facilitating data tranformation of raw text/json data into 
    a structured josn format, where table-like structures begin to emerge
    """
    function_map = configs.function_map
    raw_loc = configs.raw_loc

    master_raw_data, raw_data = prep_raw_data(raw_loc)
    
    # transformations
    for k, data in raw_data.items():
        grouped_data = group(data)
        for group_name in grouped_data:
            transformation = function_map[group_name]
            grouped_data = transformation(grouped_data)
            raw_data[k] = grouped_data

    # restructuring
    for k, data in raw_data.items():
        master_raw_data[k]['data'] = data

    # save data
    with open(configs.structured_loc, "w") as f:
        json.dump(master_raw_data, f, indent=4)
        