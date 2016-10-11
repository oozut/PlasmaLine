from unittest import TestCase


class TestLevels(TestCase):
    def test___init__(self):
        from Level import Levels
        from Level import Level
        l = Levels('../data/CI.level')
        lev = Level('2s2.2p2','3P','2','0.005381')
        lev.configuration_strip_down()
        self.assertTrue(l.levels_obj[2].configuration_high_detail == lev.configuration_high_detail)

