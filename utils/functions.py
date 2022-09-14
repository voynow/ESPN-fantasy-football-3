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
    header_raw = data['header'][2:]

    # get position and team, if no team exists team = ""
    position_team = header_raw.pop(0).split(", ")
    position_team.append("")
    (pos, team) = position_team[:2]

    # format string for key value structure
    draft_class_replace_tuples = (" ", "_"), (":_",": "), ("(", ""), (")", "")
    for t in draft_class_replace_tuples:
        header_raw[0] = header_raw[0].replace(*t)
    header_raw.append(header_raw.pop().replace("  ", " "))

    # add pos and team in key value structure
    header_raw.append(f'pos: {pos.lower()}')
    header_raw.append(f'team: {team.lower()}')

    # seperate keys from values
    header_key_values = [item.replace(": ", " ").split(" ") for item in header_raw]

    # populate dict with keys and values
    header_dict_collection = {}
    for row in header_key_values:
        for i, item in enumerate(row):
            if i % 2:
                header_dict_collection[key] = item.lower()
            else:
                key = item.lower()

    data['header'] = header_dict_collection
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
