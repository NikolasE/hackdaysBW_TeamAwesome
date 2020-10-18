import unittest

from pathplanning.pathplanning import Pathplanner, Path
class TestPathPlanning(unittest.TestCase):

    def test_bla(self):
        pp = Pathplanner('app/pathplanning/map.png', [(850, 60), (100, 212), (150, 212), (190, 212)])
        print(pp.inter_product_distances)
        # p, r = pp.get_path((10, 10), [1,2,3], 2)
        # print(p, r)
        # print(p[0])

if __name__ == '__main__':
    unittest.main()