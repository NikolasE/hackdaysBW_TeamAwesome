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

    def __init__(self, map_image_path: Path, product_locations: List[Tuple[int]]) -> None:
        self.map = np.clip(255 - skimage.io.imread(map_image_path), 1, 255)
        self.product_locations = {i: v for i, v in enumerate(product_locations)}
        self.num_products = len(self.product_locations.keys())
        self.inter_product_distances, self.inter_product_paths = self._calculate_inter_product_routes()

    def _calculate_inter_product_routes(self):
        inter_product_distances = []
        inter_product_paths = {}
        map_bounds = np.shape(self.map)

        def raise_if_out_of_bounds(loc):
            if loc[0] >= map_bounds[0] or loc[1] >= map_bounds[1] or loc[0] < 0 or loc[1] < 0:
                raise ValueError(f'location {loc} is out of bounds {map_bounds}')

        for product_start in self.product_locations.items():
            start_id = product_start[0]
            start_loc = product_start[1]
            raise_if_out_of_bounds(start_loc)

            for product_end in self.product_locations.items():
                end_id = product_end[0]
                end_loc = product_end[1]
                raise_if_out_of_bounds(end_loc)

                # if we have the dist from 13 to 42 already, don't calculate 42 to 13
                if end_id in inter_product_paths.keys():
                    continue
                if start_id == end_id:
                    continue

                if start_id not in inter_product_paths.keys():
                    inter_product_paths[start_id] = {}

                path, cost = skimage.graph.route_through_array(
                    self.map, start=start_loc, end=end_loc, fully_connected=True)

                assert cost > 0, "Products must not have the same locations"

                inter_product_distances.append((start_id, end_id, cost))
                inter_product_paths[start_id][end_id] = path

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
        # if start_id=0, then [0 3 2 1]
        route = self._roll_route(start_id, route)
        path = self._route_to_path(route)
        return path
