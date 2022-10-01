from utils import functions


fftoday = "https://fftoday.com"
link = f"{fftoday}/stats/playerstats.php?Season=2022&GameWeek=&PosID="
link_suffix = "&LeagueID=17"


historical_data_url = 'https://raw.githubusercontent.com/voynow/ESPN-fantasy-football-2/main/data/structured.json'
links_loc = 'data/player_links.json'
raw_loc = 'data/raw.json'
structured_loc = 'data/structured.json'
master_loc = 'data/master.json'
schedule_2022_loc = 'data/2022_schedule.csv'

weeks_played = 3
num_weeks = 18


function_map = {
    'header': functions.header_fn,
    '2022_gamelog_stats': functions.gamelog_stats_2022_fn,
}


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


team_abbreviation_map = {
    'buffalo bills': "BUF",
    'tampa bay buccaneers': "TB",
    'los angeles chargers': "LAC",
    'kansas city chiefs': "KC",
    'los angeles rams': "LAR",
    'green bay packers': "GB",
    'cincinnati bengals': "CIN",
    'dallas cowboys': "DAL",
    'philadelphia eagles': "PHI",
    'arizona cardinals': "ARI",
    'minnesota vikings': "MIN",
    'tennessee titans': "TEN",
    'las vegas raiders': "LV",
    'washington commanders': "WAS",
    'baltimore ravens': "BAL",
    'denver broncos': "DEN",
    'san francisco 49ers': "SF",
    'new england patriots': "NE",
    'indianapolis colts': "IND",
    'jacksonville jaguars': "JAC",
    'miami dolphins': "MIA",
    'detroit lions': "DET",
    'carolina panthers': "CAR",
    'new york giants': "NYG",
    'houston texans': "HOU",
    'new york jets': "NYJ",
    'chicago bears': "CHI",
    'new orleans saints': "NO",
    'cleveland browns': "CLE",
    'seattle seahawks': "SEA",
    'pittsburgh steelers': "PIT",
    'atlanta falcons': "ATL",
}


opp_strength_cols = [
    "opp", 
    "fpts/g", 
    "std", 
    "var", 
    "min", 
    "max",
    "num_weeks"
]


main_slate_times = [
    "1:00 PM",
    "4:05 PM",
    "4:25 PM",
]