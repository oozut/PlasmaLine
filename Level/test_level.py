from unittest import TestCase


class TestLevel(TestCase):
    def test___init__(self):
        from Level import Level
        l = Level('2s2.2p2','3P','1','7.480392')
        self.assertTrue(l.configuration =='2s2.2p2' and l.J=='1' and l.level == 7.480392 and l.term == '3P')

    def test_configuration_strip_down(self):
        from Level import Level
        l = Level('2s2.2p2','3P','1','7.480392')  # create of the object
        l.configuration_strip_down()  # test the function
        self.assertTrue(l.configuration =='2s2.2p2' and l.J=='1' and l.level == 7.480392 and l.term == '3P' and l.configuration_high_detail == [['2s','2'],['2p','2']])
