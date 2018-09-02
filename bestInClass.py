import requests
import base64
import sys
from getTeamAbrevs import return_abreviations
from API_KEY import API_KEY

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
    team_abrevs.append('KC')
    for cat in categories:
        if cat.upper() in team_abrevs:
            cat = api_format_teams(cat)
            teams.append(cat)
        else:
            positions.append(cat)
    return {'teams': teams, 'positions': positions}

def api_format_teams(team_abrev):
    if team_abrev.upper() == 'KCR':
        return 'KC'
    elif team_abrev.upper() == 'SFG':
        return 'SF'
    elif team_abrev.upper() == 'TBR':
        return 'TB'
    return team_abrev.upper()

def prepare_categories():
    categories = str(get_inputs())
    categories = listify(categories)
    categories = seperate_categories(categories)
    return categories

def process_stats(stats):
    stats = listify(stats)
    stats = list(stat.upper() for stat in stats)
    return stats

def get_stats():
    stats = input("Enter list of stats to search: ")
    return stats

def request(teams_string, positions_string):
    response = requests.get(
            url='https://api.mysportsfeeds.com/v1.2/pull/mlb/2018-regular/cumulative_player_stats.json?team={}&position={}'
                .format(teams_string, positions_string),
            headers={
                "Authorization": "Basic " + base64.b64encode((API_KEY()).encode('utf-8')).decode('ascii')
            }
        )
    return response

def run_requests(stats, categories):
    """
    Takes an array of stats to search for and a categories dictionary
    Categories object contains list teams and array positions
    Returns a list of player objects
    Each player object has a 'name' tuple and stats dictionary of relevant stats
    """

    print("Running requests...")
    teams_string = ','.join(categories['teams'])
    positions_string = ','.join(categories['positions'])
    try:
        response = request(teams_string, positions_string)
    except requests.exceptions.RequestException as e:
        print("REQUEST ERROR: ",  e)
        sys.exit(1)
    if response.status_code == 200:
        response = response.json()
        print('Processing results...')
    else:
        print("Sorry, the API appears to not be working right now. Try again later.")
        sys.exit(1)
    results = []
    try:
        for player in response['cumulativeplayerstats']['playerstatsentry']:
            new_player  = {}
            new_player['name'] = (player["player"]['FirstName'], player["player"]['LastName'])
            stat_dict = {}
            for statname, statatrs in player['stats'].items():
                if statatrs['@abbreviation'] in stats:
                    stat_dict[statname]=  statatrs['#text']
            new_player['stats'] = stat_dict
            results.append(new_player)
    except KeyError:
        return False

    return results

def get_leaders(players):
    try:
        list(players)
    except TypeError:
        return False

    if len(players) == 0:
        return False
    elif len(players) == 1:
        leader_dict = {}
        for statkey, statvalue in players[0]['stats'].items():
            leader_dict[statkey] = players[0]['name'], players[0]['stats'][statkey]
        return leader_dict

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

    if len(categories['teams']) == 0:
        teams_string = 'any teams'

    if len(categories['positions']) == 0:
        positions_string = 'any position'
        
    confirm_categories = input(
        'Search Parameters: Players that play positions: {} for {}. Is this correct? Y/n.'
        .format(positions_string, teams_string))


    if confirm_categories.lower() == str('No') or confirm_categories.lower() == str('n'):
        main()
    else:
        stats = process_stats(get_stats())
        requested_players = run_requests(stats, categories)
        if requested_players:
            for statkey, statvalue in get_leaders(requested_players).items():
                print('{} leader: {}: {}'.format(statkey, ' '.join(statvalue[0]), statvalue[1]))
        else:
            print("Sorry, no players fit your search parameters")




if __name__ == "__main__":
    main()
