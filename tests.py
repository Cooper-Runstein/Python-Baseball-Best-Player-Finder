import unittest

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

if __name__ == '__main__':
    unittest.main()
