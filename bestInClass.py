import requests
import base64
import sys
from getTeamAbrevs import return_abreviations

def get_inputs():
    category = str(input('Choose a class, or set of classes of Baseball Player, or type 0 for options/help: '))
    if category.strip() == '0':
         print('You may input teams, using the standard 2 or 3 letter abrreviation (SEA, NYY, etc.) \n'
         'You may enter a position by abbreviation (3B, P, CF, LHP, etc.) \n'
         'You may seperate different categories with commas, spaces, or both. \n'
         'see https://www.baseball-reference.com/about/team_IDs.shtml for teams.')
         return get_inputs()
    else:
        return category

def listify(input_string):
    modified_string = input_string.replace(' ', ',')
    modified_string = modified_string.replace(',,', ',')
    listed_inputs = modified_string.split(',')
    filtered_list = list(filter(lambda input: 0 < len(input) < 4, listed_inputs))
    return filtered_list

def seperate_categories(categories):
    teams, positions = [], []
    print("Processing Inputs...")
    team_abrevs = return_abreviations()
    for cat in categories:
        if cat.upper() in team_abrevs:
            teams.append(cat.upper())
        else:
            positions.append(cat)
    return {'teams': teams, 'positions': positions}

def prepare_categories():
    categories = str(get_inputs())
    categories = listify(categories)
    categories = seperate_categories(categories)
    return categories

def get_stats():
    stats = input("Enter list of stats to search: ")
    stats = listify(stats)
    return stats

def run_requests(stats, categories):
    print("Running requests...")
    teams_string = ','.join(categories['teams'])
    positions_string = ','.join(categories['positions'])
    try:
        response = requests.get(
                url='https://api.mysportsfeeds.com/v1.2/pull/mlb/2018-regular/cumulative_player_stats.json?team={}&position={}'
                    .format(teams_string, positions_string),
                headers={
                    "Authorization": "Basic " + base64.b64encode(('').encode('utf-8')).decode('ascii')
                }
            )
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
    if response.status_code == 200:
        res = response.json()
        print('Processing results...')
    else:
        print("Sorry, the API appears to not be working right now. Try again later.")
        sys.exit(1)
    results = []
    for player in res['cumulativeplayerstats']['playerstatsentry']:
        new_player  = {}
        new_player['name'] = (player["player"]['FirstName'], player["player"]['LastName'])
        stat_dict = {}
        for statname, statatrs in player['stats'].items():
            if statatrs['@abbreviation'] in stats:
                stat_dict[statname]=  statatrs['#text']
        new_player['stats'] = stat_dict
        results.append(new_player)

    return results

def get_leaders(players):
    if len(players) == 0:
        print('there are no players that fit your search parameters')
    elif len(players) == 1:
        for statkey, statvalue in players[0]['stats'].items():
            print('Leader in {} -> {}: {}'.format(statkey, players[0]['name'], statvalue))
    else:
        initial_player = players[0]
        leader_dict = {}
        for statkey, statvalue in initial_player['stats'].items():
            leader = players[0]
            for player in players[1:]:
                try:
                    if float(player['stats'][statkey]) > float(leader['stats'][statkey]):
                        leader = player
                except KeyError:
                    pass
            leader_dict[statkey] = leader['name'], leader['stats'][statkey]
        return leader_dict


def main():
    categories = prepare_categories()
    teams_string = ', '.join(categories['teams'])
    positions_string = ', '.join(categories['positions'])
    confirm_categories = input(
        'Search Parameters: Teams: {} Positions: {}. Is this correct? Y/n.'
        .format(teams_string, positions_string))
    if confirm_categories.lower() == str('No') or confirm_categories.lower() == str('n'):
        main()
    else:
        stats = get_stats()
        requested_players = run_requests(stats, categories)
        for statkey, statvalue in get_leaders(requested_players).items():
            print('{} leader: {}: {}'.format(statkey, ' '.join(statvalue[0]), statvalue[1]))




if __name__ == "__main__":
    main()
