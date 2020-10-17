from typing import Dict, Tuple, Set, List
from pathlib import Path
# https://stackoverflow.com/a/62354885/5559867  # noqa E402
import six  # noqa E402
import sys  # noqa E402
sys.modules['sklearn.externals.six'] = six  # noqa E402
import mlrose  # noqa E402
import numpy as np
import skimage.io
import skimage.graph


class Pathplanner:

    def __init__(self, map_image_path: Path, locations: List[Tuple[int, int]]) -> None:
        """Initialize TSP Pathplanner.

        Args:
            map_image_path: file path to a 8bit (!) grayscale (!) image file that holds the map,
                where "whiter" is more passable
            locations: list of (x,y) tuples that are the locations on the route. first one is start, last one is end.
                everything in ebtween can be reshuffled by the tsp algorithm.
        """
        self.map = np.clip(255 - skimage.io.imread(map_image_path), 1, 255)
        self.product_locations = locations
        self.num_products = len(self.product_locations)
        self.inter_product_distances, self.inter_product_paths = self._calculate_inter_product_routes()

    def _calculate_inter_product_routes(self):
        inter_product_distances = []
        inter_product_paths = {}
        map_bounds = np.shape(self.map)

        def raise_if_out_of_bounds(loc):
            if loc[0] >= map_bounds[0] or loc[1] >= map_bounds[1] or loc[0] < 0 or loc[1] < 0:
                raise ValueError(f'location {loc} is out of bounds {map_bounds}')

        product_locations = self.product_locations  # + [(0, 0)]  # add dummy location
        # self.dummy_location_index = len(product_locations) - 1

        inter_product_paths = dict()
        inter_product_distances = []
        for i_start, loc_start in enumerate(product_locations[:-1]):
            i_start += 1
            inter_product_paths[i_start] = dict()
            raise_if_out_of_bounds(loc_start)
            for i_end, loc_end in enumerate(product_locations[i_start:]):
                i_end += i_start + 1  # index is relative to where i_start is
                print((i_start, i_end))
                raise_if_out_of_bounds(loc_end)
                path, cost = None, None
                # if i_end == self.dummy_location_index:
                #     if i_start == 0:
                #         path, cost = ([], 1e-9)
                #     else:
                #         path, cost = ([], np.inf)
                # else:
                #     path, cost = skimage.graph.route_through_array(
                #         self.map, start=loc_start, end=loc_end, fully_connected=True)
                path, cost = skimage.graph.route_through_array(
                    self.map, start=loc_start, end=loc_end, fully_connected=True)
                assert cost > 0, "Products must not have the same locations"
                inter_product_paths[i_start][i_end] = path
                inter_product_distances.append((i_start, i_end, cost))

        return inter_product_distances, inter_product_paths

    def _calculate_user_product_routes(self, user_loc):
        user_id = 0
        paths = self.inter_product_paths.copy()
        dists = self.inter_product_distances.copy()
        paths[user_id] = dict()
        for prod_id, loc_prod in enumerate(self.product_locations):
            prod_id += 1
            path, cost = skimage.graph.route_through_array(
                self.map, start=user_loc, end=loc_prod, fully_connected=True)
            paths[user_id][prod_id] = path
            dists.append((user_id, prod_id, cost))

        return dists, paths

    def _insert_dummy_node(self, dists, paths, end_id):
        """Insert a dummy node between the user node and the last node."""
        user_id = 0
        dummy_id = self.num_products + 1
        dists.append((user_id, dummy_id, 1))
        dists.append((dummy_id, end_id, 1))
        return dists, paths

    def _do_tsp(self, dist_list):
        """Do the actual travelling salesperson."""
        dist_list.sort(key=lambda x: x[0])
        fitness_dists = mlrose.TravellingSales(distances=dist_list)
        problem_fit = mlrose.TSPOpt(
            length=self.num_products+2, fitness_fn=fitness_dists, maximize=False)
        best_state, best_fitness = mlrose.genetic_alg(
            problem_fit, mutation_prob=0.2, max_attempts=50)
        return best_state

    def _roll_route(self, start_id: int, end_id: int, route: List[int]) -> List[int]:
        """Roll the route such that the start_id is at the start of the route."""
        route = np.roll(route, -list(route).index(start_id))
        if route[1] == end_id:  # [0 3 5 4 8 2 1 6 7] where 3 is end_id
            route = np.flip(np.roll(route, -1))
        dummy_id = self.num_products + 1  # dummy id must be removed from route
        route = list(route)
        route.remove(dummy_id)
        return route

    def _route_to_path(self, route: List[int], paths) -> List[Tuple[int]]:
        """Piece together the paths between the route destinations."""
        path = []
        start = route[0]
        for target in route[1:]:
            end = target
            try:
                path_part = paths[start][end]
            except KeyError:  # we only saved one way, so let's try the same path in reverse
                path_part = reversed(paths[end][start])
            path.extend(path_part)
            start = end
        return path

    def get_path(self, user_loc, end_at_id):
        assert end_at_id <= self.num_products, "end id must be within 0..{self.num_products}"
        if self.num_products == 0:
            return [], []
        dist_list, paths = self._calculate_user_product_routes(user_loc)
        dist_list, paths = self._insert_dummy_node(dist_list, paths, end_at_id)
        print(f"dist_list: {dist_list}")
        route = self._do_tsp(dist_list)  # e.g. [2 1 0 3]
        print(f"route: {route}")
        # if start_id=0, then [0 3 2 1]
        rolled_route = self._roll_route(start_id=0, end_id=end_at_id, route=route)
        path = self._route_to_path(rolled_route, paths)
        return path, rolled_route


if __name__ == "__main__":
    pp = Pathplanner('/home/laurenz/Documents/Github/HackdaysBW_TeamAwesome/app/pathplanning/map.png', [(850, 60), (100, 212), (150, 212), (190, 212),
                                                                                                        (300, 437), (700, 212), (650, 112), (700, 112), (999, 400)])
    p = pp.get_path((10, 10), 5)
    pass
