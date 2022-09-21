from utils import functions


function_map = {
    'header': functions.header_fn,
    '2022_gamelog_stats': functions.gamelog_stats_2022_fn,
}


fftoday = "https://fftoday.com"
link = f"{fftoday}/stats/playerstats.php?Season=2022&GameWeek=&PosID="
link_suffix = "&LeagueID=17"

historical_data_url = 'https://raw.githubusercontent.com/voynow/ESPN-fantasy-football-2/main/data/structured.json'

links_loc = 'data/player_links.json'
raw_loc = 'data/raw.json'
structured_loc = 'data/structured.json'
master_loc = 'data/master.json'

table_names = [
    'header',
    '2022 Gamelog Stats', 
]

season_stats = {
    'prefix_cols': [        
        'season', 
        'team', 
        'games_played',
    ],

    'suffix_cols': [ 
        'fpts',
        'fpts/g',
    ],
}


gamelog_stats = {
    'prefix_cols': [        
        'week', 
        'opp', 
        'result',
        'score',
    ],

    'suffix_cols': [ 
        'fpts',
    ],
}


col_names = {
    'quarterback': [
        'cmp', 
        'passing_att', 
        'cmp%', 
        'passing_Yard', 
        'passing_td', 
        'int',
        'rushing_att', 
        'rushing_yard', 
        'rushing_avg', 
        'rushing_td',
    ],

    'running back': [
        'rushing_att',
        'rushing_yard',
        'rushing_avg',
        'rushing_td',
        'receiving_target',
        'receiving_rec',
        'receiving_yard',
        'receiving_avg',
        'receiving_td',
    ],

    'wide receiver': [
        'receiving_target',
        'receiving_rec',
        'receiving_yard',
        'receiving_avg',
        'receiving_td',
        'rushing_att',
        'rushing_yard',
        'rushing_avg',
        'rushing_td',
    ],

    'tight end': [
        'receiving_target',
        'receiving_rec',
        'receiving_yard',
        'receiving_avg',
        'receiving_td',
    ],

    'kicker': [
        'fgm', 
        'fga', 
        'fg%', 
        'epm', 
        'epa'
    ]
}

float_cols = [
    'games_played',
    'fpts',
    'fpts/g',
    'week'
    'cmp', 
    'passing_att', 
    'cmp%', 
    'passing_Yard', 
    'passing_td', 
    'int',
    'rushing_att', 
    'rushing_yard', 
    'rushing_avg', 
    'rushing_td',
    'receiving_target',
    'receiving_rec',
    'receiving_yard',
    'receiving_avg',
    'receiving_td',
    'fgm', 
    'fga', 
    'fg%', 
    'epm', 
    'epa'
]