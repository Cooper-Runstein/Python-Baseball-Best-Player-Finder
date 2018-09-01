import unittest

from unittest.mock import patch

import bestInClass
import getTeamAbrevs

class LisitfyTests(unittest.TestCase):
    def test_normal_cases(self):
        assert bestInClass.listify('3B NYY Sea') == ['3B', 'NYY', 'Sea']
        assert bestInClass.listify('3B, NYY, Sea') == ['3B', 'NYY', 'Sea']
        assert bestInClass.listify(' 3B NYY  Sea') == ['3B', 'NYY', 'Sea']

    def test_abnormal_comas(self):
        assert bestInClass.listify('3b,,SEA,,,NYY') == ['3b', 'SEA', 'NYY']
        assert bestInClass.listify('3b, ,SEA,, ,NYY') == ['3b', 'SEA', 'NYY']
        assert bestInClass.listify(',3b,,SEA,,,NYY,') == ['3b', 'SEA', 'NYY']

class SeperateTests(unittest.TestCase):
    def test_seperate(self):
        assert bestInClass.seperate_categories(['3B', 'NYY']) == {
            'teams':['NYY'],
            'positions':['3B']
        }
    def test_upper_cases(self):
        assert bestInClass.seperate_categories(['3B', 'NYY', 'Sea', 'P']) == {
            'teams':['NYY', 'SEA'],
            'positions':['3B', 'P']
        }

class ApiFormatTests(unittest.TestCase):
    def test_KC(self):
        assert bestInClass.api_format_teams('KCR') == 'KC'

    def test_SF(self):
        assert bestInClass.api_format_teams('SFG') == 'SF'

class GetLeadersTests(unittest.TestCase):
    def setUp(self):
        self.players1Stat= [
            {
                'name': ('Miguel', 'Andujar'),
                'stats': {'Hits':'143'}
            },
            {
                'name': ('NotMiguel', 'NotAndujar'),
                'stats': {'Hits':'5'}
            },
        ]
        self.players2Stat= [
            {
                'name': ('Miguel', 'Andujar'),
                'stats': {
                    'Hits':'143',
                    'HomeRuns': '25'
                }
            },
            {
                'name': ('NotMiguel', 'NotAndujar'),
                'stats': {
                    'Hits': '5',
                    'HomeRuns': '3'
                }
            },
            {
                'name': ('AlsoNotMiguel', 'AlsoNotAndujar'),
                'stats': {
                    'Hits':'5',
                    'HomeRuns': '6'
                }
            }
        ]
        self.players1Player = [
            {
                'name': ('Miguel', 'Andujar'),
                'stats': {
                    'Hits':'143',
                    'HomeRuns': '25'
                }
            },
        ]


    def test_one_stat(self):
        assert bestInClass.get_leaders(self.players1Stat) == {'Hits': (('Miguel', 'Andujar'), '143')}

    def test_two_stat(self):
        assert bestInClass.get_leaders(self.players2Stat) == {
            'Hits': (('Miguel', 'Andujar'), '143'),
            'HomeRuns': (('Miguel', 'Andujar'), '25')
        }

    def test_one_person(self):
        assert bestInClass.get_leaders(self.players1Player) == {'Hits': (('Miguel', 'Andujar'), '143'), 'HomeRuns': (('Miguel', 'Andujar'), '25')}

    def test_no_players(self):
        self.assertFalse(bestInClass.get_leaders([]))

    def test_bad_input(self):
        self.assertFalse(bestInClass.get_leaders(False))

class TestPrepare(unittest.TestCase):
    @patch('bestInClass.get_inputs', return_value='')
    def test_no_input(self, input):
        assert bestInClass.prepare_categories() == {'teams': [], 'positions': []}

    @patch('bestInClass.get_inputs', return_value='NYY, SEA, 3B ')
    def test_with_input(self, input):
        assert bestInClass.prepare_categories() == {'teams': ['NYY', 'SEA'], 'positions': ['3B']}

class TestProcessStats(unittest.TestCase):
    def setUp(self):
        self.stats = 'HR'
    def test_one_stat(self):
        assert bestInClass.process_stats(self.stats) == ['HR']

if __name__ == '__main__':
    unittest.main()
