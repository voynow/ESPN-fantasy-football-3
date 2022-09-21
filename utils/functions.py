from utils import configs

def stats_to_json(stats, columns):
    """
    Helper function to convert 2D list into JSON with columns names
    """
    stats_json = {col: [] for col in columns}
    for row in stats:
        for col, item in zip(stats_json, row):
            stats_json[col].append(item)


    fns = [
        lambda x: None if x == "-" else x,
        lambda x: x.replace(",", "") if x else None,
        lambda x: x.replace("%", "") if x else None,
        lambda x: float(x) if x else None
    ]
    for col in stats_json:
        if col in configs.float_cols:
            for fn in fns:
                stats_json[col] = list(map(fn, stats_json[col]))

    return stats_json
    

def header_fn(data):
    """
    Extract misc player information not included in season/gamlog stats
    """
    header = {}
    raw_header = data['header']

    header['pos'], header['team'] = raw_header[2].split(", ")
    header['pos'] = header['pos'].lower()
    header['team'] = header['team'].lower()

    for item in raw_header[3:]:
        if ":" in item:
            split_item = item.split(": ")
            key = split_item[0]
            if key == "College":
                header[key.lower()] = split_item[1]
            if key == "Draft":
                header[key.lower()] = split_item[1].replace(" ", "_").replace("(", "").replace(")", "")
            if key in ["Ht", "DOB", "Age"]:
                item = item.replace(": ", ":").replace("  ", " ").split(" ")
                for subitem in item:
                    if ":" in subitem:
                        key, val = subitem.split(":")
                        header[key.lower()] = val

    data['header'] = header
    return data

def gamelog_stats_fn(data, table_name):
    """
    Extract data pertaining to players game level stats
    """
    gamelog_raw = data[table_name]
    pos = data['header']['pos']

    # collect data from relevant rows
    gamelog_stats = [row.replace('at ', '@').split(" ") for row in gamelog_raw[4:]]
    if "=" in gamelog_stats[-1]:
        gamelog_stats.pop()

    # collect columns
    prefix = configs.gamelog_stats['prefix_cols']
    suffix = configs.gamelog_stats['suffix_cols']
    columns = prefix + configs.col_names[pos] + suffix

    data[table_name] = stats_to_json(gamelog_stats, columns)
    return data


def gamelog_stats_2022_fn(data): 
    """
    Extract data pertaining to players 2019 game level stats
    """
    return gamelog_stats_fn(data, '2022_gamelog_stats')
