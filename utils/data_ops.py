import json
import pandas as pd

from utils import configs


def normalize(json_data):
    """
    Update data structure where data tables are brought to top level 
    """
    for player, obj in json_data.items():

        # bring header attributes to top level
        for key, value in json_data[player]['data']['header'].items():
            json_data[player][key] = value

        # remove header object
        del json_data[player]['data']['header']

        # bring dataset keys to top level
        for dataset, data in obj['data'].items():
            json_data[player][dataset] = data

        # remove data object
        del json_data[player]['data']

    return json_data


def load():
    """
    Load master dataset with tables names accessible by dictionary key
    """
    f_open = open(configs.master_loc, 'rb')
    normalized_data = normalize(json.load(f_open))
    joined_data = join_players(normalized_data)
    
    return joined_data


def join_players(json_data):
    """
    Join game statistics partitioned by position
    """
    dfs = {}
    for player, data in json_data.items():
        pos = data['pos']

        for key in data:
            year = key.split("_")[0]

            if year.isnumeric() and len(year) == 4:
                df = pd.DataFrame(data[key])
                df['player'] = player
                df['year'] = int(year)

                if pos in dfs:
                    dfs[pos].append(df)
                else:
                    dfs[pos] = [df]

    for key in dfs:
        dfs[key] = pd.concat(dfs[key])

    return dfs


def get_schedule(week_num):
    """
    Transforming schedule copied from https://www.fftoday.com/nfl/schedule.php
    """
    data_path = configs.schedule_2022_loc

    schedule = []
    for row in open(data_path, 'r').readlines():

        remove_strings = "\n", " â¹", " *"
        for string in remove_strings:
            row = row.replace(string, "")
        row = row.split(",")

        if 'Week' in row[0]:
            schedule.append([])
        else:
            schedule[-1].append(row)

    for i, week in enumerate(schedule):
        if i == week_num - 1:
            df = pd.DataFrame(week[1:]).iloc[:, :4]
            df.columns = week[0]
            for col in ["Away Team", "Home Team"]:
                df[col] = df[col].apply(lambda x: x.lower() if x else x)
                df[col] = df[col].apply(lambda x: configs.team_abbreviation_map[x] if x else x)
            return df


def get_opponent_strength(dfs, season=2022):
    """
    Group data by position & opponent and exctact statistics for points scored
    The resulting dataframe can identify strength of an opponen for all positions
    """    
    opp_strength_all_positions = {}
    opp_strength_cols = configs.opp_strength_cols

    for pos in dfs:
        df = dfs[pos]
        df_year = df[df['year'] == season]
        df_year['opp'] =  df_year['opp'].apply(lambda x: x.replace("@", ""))

        opp_strength = {col: [] for col in opp_strength_cols}

        for opp, group in df_year.groupby('opp'):

            fpts = group.groupby('week').sum()['fpts']

            opp_strength['opp'].append(opp)
            opp_strength['fpts/g'].append(fpts.mean().round(3))
            opp_strength['std'].append(fpts.std().round(3))
            opp_strength['var'].append(fpts.var().round(3))
            opp_strength['min'].append(fpts.min())
            opp_strength['max'].append(fpts.max())

        opp_strength_all_positions[pos] = pd.DataFrame(opp_strength).sort_values(by='fpts/g', ascending=False).reset_index()

    return opp_strength_all_positions


def get_main_slate_games(schedule):
    """
    Create map of games playing on Sunday afternoons only
    This info can be used for underdog fantasy main slate tournaments
    """
    main_slate_times = configs.main_slate_times
    main_slate_games = pd.concat([schedule[schedule['Time (ET)'] == string] for string in main_slate_times])

    game_map = {}
    for _, row in main_slate_games.iterrows():
        game_map[row['Away Team']] = row['Home Team']
        game_map[row['Home Team']] = row['Away Team']

    return game_map


def generate_main_slate_report(dfs, week_num):
    """
    Generate report for strength of schedule (Sunday afternoon games only)
    This info can be used for underdog fantasy main slate tournaments
    """
    opponent_strength = get_opponent_strength(dfs)
    schedule = get_schedule(week_num)
    game_map = get_main_slate_games(schedule)

    return_string = ""
    for key in opponent_strength:
        df = opponent_strength[key]

        return_string += f"\n\nPOSITION: {key}\tMean: {df['fpts/g'].mean():.1f}\t Std: {df['fpts/g'].std():.1f}\n"

        for i, row in df.iterrows():
            if row.opp in list(game_map.keys()):
                rank = 32 - i
                if rank <=8 or rank >= 24:
                    if rank <= 8:
                        return_string += "XXX "
                    if rank >= 24:
                        return_string += u'\u2713'*2 + " "
                else:
                    continue

                return_string += (f"Rank: {rank:2n}\t"
                f"Teams: {game_map[row.opp]} -> {row.opp:3s}\t"
                f"Average: {row['fpts/g']:.1f}\t\t"
                f"(Std: {row['std']:.1f}, Var: {row['var']:.1f}, Min: {row['min']:.1f}, Max: {row['max']:.1f})\n")

    return return_string