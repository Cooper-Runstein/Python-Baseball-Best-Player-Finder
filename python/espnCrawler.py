from bs4 import BeautifulSoup
from contextlib import closing
import requests

def get_page(url):
    """
    Gets content at HTML if possible.
    Else returns False
    """
    try:
        with closing(requests.get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except requests.exceptions.RequestException as e:
        print(e)
        return False

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def make_soup(url):
    """
    Run request and turn content to soup
    """
    raw_html = get_page(url)
    html = BeautifulSoup(raw_html, 'html.parser')
    return html

def get_from_soup(soup):
    leaders = []
    leader_container = soup.find(class_="mod-stat-leaders")
    players_info = leader_container.find_all(class_="player-info")

    for i, player in enumerate(players_info):
        text = player.find('a').get_text()
        leaders.append({"player": text})
    
    stats = leader_container.find_all('h4')

    for i, stat in enumerate(stats):
        text = stat.get_text()
        leaders[i]["stat"] = text

    for item in leaders:
        print({item["stat"]: item["player"]})

    # for i, tr in enumerate():
    #     print({i: tr})
    #     print("\n")
    #print()
    # """
    # parse html and get Team_abbreviations
    # """
    # abrevs = []
    # for i, tr in enumerate(soup.select('tr')):
    #     tr = str(tr)
    #     tr = tr.replace('<tr>', '')
    #     tr = tr.replace('</tr>', '')
    #     tr = tr.replace('</td>', '')
    #     tr = tr.split('<td>')
    #     tr = tr[1:]
    #     abrevs.append(tr)

    # abrevs = list(filter(lambda x: x[-1] == 'Present', abrevs))
    # abrevs = list(map(lambda x: x[1], abrevs))
    # return abrevs


def return_abreviations(team):
    url = f"http://www.espn.com/mlb/team/stats/pitching/_/name/{team}"
    soup = make_soup(url)
    return get_from_soup(soup)

if __name__ == "__main__":
    return_abreviations('bos')
