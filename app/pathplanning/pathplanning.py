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

    def __init__(self, map_image_path: Path, locations: List[Tuple[int]]) -> None:
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

        product_locations = self.product_locations + [(0, 0)]  # add dummy location
        dummy_location_index = len(product_locations) - 1

        inter_product_paths = dict()
        inter_product_distances = []
        for i_start, loc_start in enumerate(product_locations[:-1]):
            inter_product_paths[i_start] = dict()
            raise_if_out_of_bounds(loc_start)
            for i_end, loc_end in enumerate(product_locations[i_start+1:]):
                i_end += i_start + 1  # index is relative to where i_start is
                raise_if_out_of_bounds(loc_end)
                path, cost = None, None
                if i_end == dummy_location_index:
                    if i_start == 0:
                        path, cost = ([], 1e-9)
                    else:
                        path, cost = ([], np.inf)
                else:
                    path, cost = skimage.graph.route_through_array(
                        self.map, start=loc_start, end=loc_end, fully_connected=True)
                assert cost > 0, "Products must not have the same locations"
                inter_product_paths[i_start][i_end] = path
                inter_product_distances.append((i_start, i_end, cost))

        return inter_product_distances, inter_product_paths

    def _do_tsp(self, dist_list):
        """Do the actual travelling salesperson."""
        fitness_dists = mlrose.TravellingSales(distances=dist_list)
        problem_fit = mlrose.TSPOpt(
            length=self.num_products, fitness_fn=fitness_dists, maximize=False)
        best_state, best_fitness = mlrose.genetic_alg(
            problem_fit, mutation_prob=0.2, max_attempts=100, random_state=2)
        return best_state

    def _roll_route(self, start_id: int, route: List[int]) -> List[int]:
        """Roll the route such that the start_id is at the start of the route."""
        return np.roll(route, -list(route).index(start_id))

    def _route_to_path(self, route: List[int]) -> List[Tuple[int]]:
        """Piece together the paths between the route destinations."""
        path = []
        start = route[0]
        for target in route[1:]:
            end = target
            try:
                path_part = self.inter_product_paths[start][end]
            except KeyError:  # we only saved one way, so let's try the same path in reverse
                path_part = reversed(self.inter_product_paths[end][start])
            path.extend(path_part)
            start = end
        return path

    def _targets_to_dist_list(self, targets):
        return self.inter_product_distances
        # TODO: for now we can only use ALL of the products given in the initializer.
        # Otherwise we'll get Exception: All nodes must appear at least once in distances.
        # because ids will be missing, but mlrose wants them monotonically.
        # def products_are_both_included(id1, id2) -> bool:
        #     return id1 in target_product_ids and id2 in target_product_ids
        # dist_list = [ipd for ipd in self.inter_product_distances if products_are_both_included(
        #     ipd[0], ipd[1])]
        # print(dist_list)

    def get_path(self, start_id: int = 0, target_product_ids: Set[int] = None):
        if len(self.product_locations) == 0:
            return []
        dist_list = self._targets_to_dist_list(target_product_ids)
        print(f"dist_list: {dist_list}")
        route = self._do_tsp(dist_list)  # e.g. [2 1 0 3]
        print(f"route: {route}")
        # if start_id=0, then [0 3 2 1]
        route = self._roll_route(start_id, route)
        path = self._route_to_path(route)
        return path, route
