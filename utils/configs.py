from utils import functions


function_map = {
    'header': functions.header_fn,
    'season_stats': functions.season_stats_fn,
    '2021_gamelog_stats': functions.gamelog_stats_2021_fn,
    '2020_gamelog_stats': functions.gamelog_stats_2020_fn,
    '2019_gamelog_stats': functions.gamelog_stats_2019_fn,
}

fftoday = "https://fftoday.com"
link = f"{fftoday}/stats/playerstats.php?Season=2021&GameWeek=&PosID="
link_suffix = "&LeagueID=17"

links_loc="data/player_links.json"
raw_loc = 'data/raw.json'
structured_loc = 'data/structured.json'

table_names = [
    'header',
    'Season Stats',
    '2021 Gamelog Stats', 
    '2020 Gamelog Stats', 
    '2019 Gamelog Stats', 
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

    'running': [
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

    'wide': [
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

    'tight': [
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