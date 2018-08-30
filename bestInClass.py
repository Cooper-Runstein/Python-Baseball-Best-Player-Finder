import requests as r
from getTeamAbrevs import return_abreviations

base_url = 'https://api.mysportsfeeds.com/v2.0/pull/mlb/2018/player_stats_totals.json'

# r.get()

def get_inputs():
    category = input('Choose a class, or set of classes of Baseball Player, or type 0 for options/help: ')
    if category.strip() == '0':
         print('You may input teams, using the standard 2 or 3 letter abrreviation (SEA, NYY, etc.) \n'
         'You may enter a position by abbreviation (3B, P, CF, LHP, etc.) \n'
         'You may seperate different categories with commas, spaces, or both. \n'
         'see https://en.wikipedia.org/wiki/Wikipedia:WikiProject_Baseball/Team_abbreviations for teams.')
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
    print(stats, categories)
    print("Running requests")


def main():
    categories = prepare_categories()
    teams_string = ', '.join(categories['teams'])
    positions_string = ', '.join(categories['positions'])
    print(teams_string)
    confirm_categories = input(
        'Search Parameters: Teams: {} Positions: {}. Is this correct? Y/n.'
        .format(teams_string, positions_string))
    if confirm_categories.lower() == str('No') or confirm_categories.lower() == str('n'):
        main()
    else:
        stats = get_stats()
        run_requests(stats, categories)






if __name__ == "__main__":
    main()
