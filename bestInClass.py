import requests as r

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

def listify_categories(categories):
    categories = categories.replace(' ', ',')
    categories = categories.replace(',,', ',')
    categories = categories.split(',')
    categories = list(filter(lambda cat: 0 < len(cat) < 4, categories))

    return categories

def seperate_categories(categories):
    teams = []
    positions = []

    for cat in categories:
        if len(cat) == 1:
            positions.append(cat)
        elif



def main():
    categories = str(get_inputs())
    categories = listify_categories(categories)
    print(categories)




if __name__ == "__main__":
    main()
