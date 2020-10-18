import re
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
import tqdm
import pickle
import os
import hashlib
from six import string_types

CACHE_PATH = 'cache.pickle'

class Pathplanner:

    def __init__(self, map_image_path: Path, locations: Dict[str, Tuple[int, int]]) -> None:
        """Initialize TSP Pathplanner.

        Args:
            map_image_path: file path to a 8bit (!) grayscale (!) image file that holds the map,
                where "whiter" is more passable
            locations: dict of ean-string to (y,x) tuples that are the locations on the route. first one is start, last one is end.
                everything in between can be reshuffled by the tsp algorithm.
        """

        self.map = np.clip(255 - skimage.io.imread(map_image_path), 1, 255)
        self.product_locations = locations
        self.locations_hash = self._get_hash_of_locations(locations)

        self.inter_product_distances = list()
        self.inter_product_paths = dict()

        if not self._load_distance_and_paths():
            self.inter_product_distances, self.inter_product_paths = self._calculate_inter_product_routes()
            self._store_distance_and_paths()

    def _get_hash_of_locations(self, locations):
        m = hashlib.sha1()
        m.update(str(locations).encode('utf-8'))
        return m.hexdigest()

    def _load_distance_and_paths(self):
        if not os.path.exists(CACHE_PATH):
            print("No cache file for distances!")
            return False
        print("Loading distances and paths from file!")
        with open(CACHE_PATH, 'rb') as f:
            try:
                data = pickle.load(f)
            except EOFError:
                print("Empty pickle cache")
                return False
            if self.locations_hash not in data.keys():
                print("No cache for this locations hash found")
                return False
            self.inter_product_distances = data[self.locations_hash]['product_distances']
            self.inter_product_paths = data[self.locations_hash]['product_paths']

        return True

    def _store_distance_and_paths(self):
        print("Storing")
        try:
            with open(CACHE_PATH, 'rb') as f:
                data = pickle.load(f)
        except (FileNotFoundError, EOFError):
            data = {}
        data[self.locations_hash] = {
            "product_distances": self.inter_product_distances,
            "product_paths": self.inter_product_paths,
        }
        with open(CACHE_PATH, 'wb') as f:
            pickle.dump(data, f)

    def _calculate_inter_product_routes(self):
        inter_product_distances = []
        inter_product_paths = {}
        map_bounds = np.shape(self.map)

        def raise_if_out_of_bounds(loc):
            if loc[0] >= map_bounds[0] or loc[1] >= map_bounds[1] or loc[0] < 0 or loc[1] < 0:
                raise ValueError(f'location {loc} is out of bounds {map_bounds}')

        inter_product_paths = dict()
        inter_product_distances = []

        # tqdm creates a progress bar to show the process of the path computation
        num_prods = len(self.product_locations)
        num_iters = (num_prods*num_prods)/2 - num_prods
        t = tqdm.tqdm(total=num_iters)
        ean_start_index = 0
        for ean_start, loc_start in list(self.product_locations.items())[:-1]:
            inter_product_paths[ean_start] = dict()
            raise_if_out_of_bounds(loc_start)
            for ean_end, loc_end in list(self.product_locations.items())[ean_start_index+1:]:
                raise_if_out_of_bounds(loc_end)
                path, cost = None, None
                path, cost = skimage.graph.route_through_array(
                    self.map, start=loc_start, end=loc_end, fully_connected=True)
                assert cost > 0, "Products must not have the same locations"
                inter_product_paths[ean_start][ean_end] = path
                inter_product_distances.append((ean_start, ean_end, cost))
                t.update(1)
            ean_start_index += 1
        t.close()
        return inter_product_distances, inter_product_paths

    def _calculate_user_product_routes(self, user_loc):

        paths = self.inter_product_paths.copy()
        dists = self.inter_product_distances.copy()
        paths['_user'] = dict()

        # compute distance and path to all products
        for ean_target, loc_target in self.product_locations.items():
            path, cost = skimage.graph.route_through_array(
                self.map, start=user_loc, end=loc_target, fully_connected=True)
            paths['_user'][ean_target] = path
            dists.append(('_user', ean_target, cost))

        return dists, paths

    def _get_max_index_value_in_dists(self, dists):
        return np.max([max(dist_point[0], dist_point[1]) for dist_point in dists])

    def _get_indices_in_dist(self, dists):
        indices = set([d[0] for d in dists])
        indices.update(set([d[1] for d in dists]))
        return list(indices)

    def _insert_dummy_node(self, dists, user_id, end_id):
        assert end_id in self._get_indices_in_dist(dists), "end id not in dists list"

        """Insert a dummy node between the user node and the last node."""
        self.dummy_id = self._get_max_index_value_in_dists(dists) + 1
        dists.append((user_id, self.dummy_id, 1))
        dists.append((self.dummy_id, end_id, 1))
        return dists

    def _do_tsp(self, dist_list):
        """Do the actual travelling salesperson."""
        dist_list.sort(key=lambda x: x[0])
        length = int(self._get_max_index_value_in_dists(dist_list) + 1)
        try:
            fitness_dists = mlrose.TravellingSales(distances=dist_list)
            problem_fit = mlrose.TSPOpt(
                length=length, fitness_fn=fitness_dists, maximize=False)
            best_state, best_fitness = mlrose.genetic_alg(
                problem_fit, mutation_prob=0.2, max_attempts=50)
        except Exception:
            print(f"tsp failed. dist_list: {dist_list}")
            raise
        return best_state

    def _roll_route(self, start_id: int, end_id: int, route: List[int]) -> List[int]:
        """Roll the route such that the start_id is at the start of the route."""
        route = np.roll(route, -list(route).index(start_id))
        if route[1] == end_id:  # [0 3 5 4 8 2 1 6 7] where 3 is end_id
            route = np.flip(np.roll(route, -1))
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

    def _filter_dists(self, selected_artikel_eans, dist_list):

        selected_artikel_eans_and_user = selected_artikel_eans + ["_user"]

        def is_in_spid(src, target):
            in_selected_products = src in selected_artikel_eans_and_user and target in selected_artikel_eans_and_user
            return in_selected_products

        ean_to_tsp_id = {}
        filtered_dists_with_tsp_id = []
        for src, target, dist in dist_list:
            if is_in_spid(src, target):
                new_src_idx = list(selected_artikel_eans_and_user).index(src)
                new_target_idx = list(selected_artikel_eans_and_user).index(target)
                ean_to_tsp_id[src] = new_src_idx
                ean_to_tsp_id[target] = new_target_idx

                filtered_dists_with_tsp_id.append((new_src_idx, new_target_idx, dist))

        return filtered_dists_with_tsp_id, ean_to_tsp_id

    def _remove_dummy(self, route_with_dummy):
        route_no_dummy = list(route_with_dummy)
        route_no_dummy.remove(self.dummy_id)
        return route_no_dummy

    def _convert_route_from_tsp_id_to_ean(self, ean_to_tsp_id: dict, rolled_route: List[int]):
        def invert_lookup(d: dict, v):
            ndx = list(d.values()).index(v)
            return list(d.keys())[ndx]
        ean_route = [invert_lookup(ean_to_tsp_id, tsp_id) for tsp_id in rolled_route]
        return ean_route


    def get_path(self, user_location, selected_artikel_eans, end_ean):
        if end_ean not in selected_artikel_eans:
            selected_artikel_eans.append(end_ean)

        dist_list_ean_all_with_user, paths = self._calculate_user_product_routes(user_location)
        dist_list_tspids_selected_with_user, ean_to_tsp_id = self._filter_dists(selected_artikel_eans, dist_list_ean_all_with_user)
        end_tsp_id = ean_to_tsp_id[end_ean]
        user_tsp_id = ean_to_tsp_id['_user']
        dist_list_tspids_selected_with_user_and_dummy = self._insert_dummy_node(dist_list_tspids_selected_with_user, user_tsp_id, end_tsp_id)
        print(f"calculated dist_list = {dist_list_tspids_selected_with_user_and_dummy}")
        route_with_dummy = self._do_tsp(dist_list_tspids_selected_with_user_and_dummy)
        print(f"calculated route = {route_with_dummy}")
        route_no_dummy = self._remove_dummy(route_with_dummy)
        print(f"route with product location indices = {route_no_dummy}")
        rolled_route = self._roll_route(start_id=user_tsp_id, end_id=end_tsp_id, route=route_no_dummy)
        print(f"rolled_route = {rolled_route}")
        rolled_route_with_eans = self._convert_route_from_tsp_id_to_ean(ean_to_tsp_id, rolled_route)
        path = self._route_to_path(rolled_route_with_eans, paths)
        return path, rolled_route_with_eans


if __name__ == "__main__":
    pl = {
        "_kasse": (899, 399),
        "0003376": (730, 110),
        "0116393": (200, 110),
    }
    pp = Pathplanner('map.png', pl)
    p, r = pp.get_path((10, 10), ["0003376", "0116393"], "_kasse")
    pass
