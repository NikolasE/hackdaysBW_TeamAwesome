import unittest

from pathplanning.pathplanning import Pathplanner, Path
class TestPathPlanning(unittest.TestCase):

    def test_caching(self):
        positions = [(850, 60), (100, 212), (150, 212), (190, 212)]
        pp = Pathplanner('app/pathplanning/map.png', positions)
        print(pp.inter_product_distances)
        # check 
        indices = pp._get_indices_in_dist(pp.inter_product_distances) 
        for i in range(len(positions)):
            self.assertTrue((i+1) in indices)
        self.assertTrue(len(indices) == len(positions))
        self.assertTrue(0 not in indices)

    # def test_roll(self):
    #     positions = [(850, 60), (100, 212), (150, 212), (190, 212)]
    #     pp = Pathplanner('app/pathplanning/map.png', positions)
    #     p2 = Pathplanner._roll_route([0,2,3,1], )    


    def test_full(self):
        positions = [(850, 60), (100, 212), (150, 212), (190, 212)]
        pp = Pathplanner('app/pathplanning/map.png', positions)
        p, r = pp.get_path((10, 10), [1,2,3], 2)
        print(p)

    def test_add_user_position(self):
        positions = [(850, 60), (100, 212), (150, 212), (190, 212)]
        pp = Pathplanner('app/pathplanning/map.png', positions)
        new_dist, new_path = pp._calculate_user_product_routes((0,0))

        indices = pp._get_indices_in_dist(new_dist)
        for i in range(len(positions)):
            self.assertTrue((i+1) in indices)
        self.assertTrue(len(indices) == len(positions) + 1)
        self.assertTrue(pp.user_position_id in indices)
        self.assertTrue(pp.user_position_id == 0)
        
        # insert dummy node:
        end_id = 3
        dist_dummy = pp._insert_dummy_node(new_dist, end_id)
        indices = pp._get_indices_in_dist(new_dist)
        for i in range(len(positions)):
            self.assertTrue((i+1) in indices)
        self.assertTrue(len(indices) == len(positions) + 2)
        self.assertTrue(pp.user_position_id in indices)
        self.assertTrue(end_id in indices)
        self.assertTrue(pp.user_position_id == 0)
        
    def test_roll_route(self):
        pass



if __name__ == '__main__':
    unittest.main()