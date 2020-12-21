import functools
import operator
import re
from collections import defaultdict
from itertools import chain

import numpy as np
from cachetools import cached
from cachetools.keys import hashkey

from advent import AdventProblem

class TileNode:
    def __init__(self, tile):
        self.tile = tile
        self.left = None
        self.right = None
        self.top = None
        self.bottom = None

    def __repr__(self):
        return '{} = (left = {}, right = {}, top = {}, bottom = {})'.format(
            self.tile.name,
            self.left.tile.name if self.left is not None else None,
            self.right.tile.name if self.right is not None else None,
            self.top.tile.name if self.top is not None else None,
            self.bottom.tile.name if self.bottom is not None else None
        )

class Tile:
    def __init__(self, id, array, rot=0, flip=0):
        self.id = id
        self.original = array
        self.rot = rot
        self.flip = flip
        self.transformed = self.transform(self.original, self.rot, self.flip)

    @property
    def name(self):
        return self.id, self.rot, self.flip

    def __repr__(self):
        return str(self.name)

    @staticmethod
    def transform(arr, rot, flip):
        transformed = arr
        if flip:
            transformed = np.flip(transformed, axis=1)
        transformed = np.rot90(transformed, k=rot)
        return transformed

    @property
    def left(self):
        return self.transformed[:, 0]

    @property
    def right(self):
        return self.transformed[:, -1]

    @property
    def top(self):
        return self.transformed[0, :]

    @property
    def bottom(self):
        return self.transformed[-1, :]

    @property
    def borders(self):
        return (self.left, self.right, self.top, self.bottom)

    def generate_transforms(self):
        transforms = []
        for rot in range(4):
            for flip in range(2):
                transforms.append(Tile(self.id, self.original, rot, flip))
        return transforms


def preprocess(lines):
    MAPPER = {
        '#': 1,
        '.': 0
    }
    arrays = []
    curr_array = []
    curr_tile = None
    for line in lines:
        if len(line) == 0:
            arrays.append(Tile(curr_tile, np.array(curr_array)))
            curr_array = []
            curr_tile = None
        elif (match := re.fullmatch('Tile (\d+):', line)):
            curr_tile = int(match.group(1))
        else:
            curr_array.append([MAPPER[ch] for ch in line])
    arrays.append(Tile(curr_tile, np.array(curr_array)))
    return arrays


def make_dbs(tiles):
    all_transforms = {}
    left_borders = defaultdict(list)
    right_borders = defaultdict(list)
    top_borders = defaultdict(list)
    bottom_borders = defaultdict(list)
    for tile in tiles:
        for transform in tile.generate_transforms():
            all_transforms[transform.name] = transform
            left_borders[repr(transform.left)].append(transform.name)
            right_borders[repr(transform.right)].append(transform.name)
            top_borders[repr(transform.top)].append(transform.name)
            bottom_borders[repr(transform.bottom)].append(transform.name)

    borders = defaultdict(list)
    for border, transforms in chain(left_borders.items(), right_borders.items(), top_borders.items(), bottom_borders.items()):
        borders[border].extend(transforms)

    return all_transforms, left_borders, right_borders, top_borders, bottom_borders, borders

def identify_corner_tiles(tiles, borders):
    corners = []
    for tile in tiles:
        match_found = 0
        for border in tile.borders:
            if repr(border) in borders and any(t[0] != tile.id for t in borders[repr(border)]):
                match_found += 1
        if match_found == 2:
            corners.append(tile)
    return corners

@cached(cache={}, key=lambda curr_tile, tiles_left, tile_node, *extras: hashkey(curr_tile))
def solve_jigsaw(curr_tile, tiles_left, tile_node, *extras):
    transforms, left_borders, right_borders, top_borders, bottom_borders = extras
    iterator = [
        ('left', 'right', right_borders),
        ('right', 'left', left_borders),
        ('top', 'bottom', bottom_borders),
        ('bottom', 'top', top_borders)
    ]
    has_options = [False, False, False, False]
    for i, (direction, foil_dir, borders) in enumerate(iterator):
        if getattr(tile_node, direction) is not None:
            has_options[i] = True
            continue
        options = borders[repr(getattr(curr_tile, direction))]
        for opt in options:
            if opt[0] in tiles_left:
                has_options[i] = True
                new_node = TileNode(transforms[opt])
                setattr(new_node, foil_dir, tile_node)
                setattr(tile_node, direction, new_node)
                if not solve_jigsaw(transforms[opt], tiles_left - {opt[0]}, new_node, *extras):
                    setattr(tile_node, direction, None)
    return np.sum(has_options) >= 1

def order_tile_nodes(tile_node, visited, ordered_map, r, c):
    if tile_node is None or tile_node.tile.id in visited:
        return
    ordered_map[(r, c)] = tile_node
    visited.add(tile_node.tile.id)
    for direction, dr, dc in [('left', 0, -1), ('right', 0, 1), ('top', -1, 0), ('bottom', 1, 0)]:
        order_tile_nodes(getattr(tile_node, direction), visited, ordered_map, r + dr, c + dc)

def resolve_tile_map(tile_node):
    ordered_map = {}
    order_tile_nodes(tile_node, set(), ordered_map, 0, 0)
    min_r = min(ordered_map.keys(), key=lambda k: k[0])[0]
    max_r = max(ordered_map.keys(), key=lambda k: k[0])[0]
    min_c = min(ordered_map.keys(), key=lambda k: k[1])[1]
    max_c = max(ordered_map.keys(), key=lambda k: k[1])[1]
    ordered_arr = []
    for i in range(min_r, max_r + 1):
        ordered_arr.append([])
        for j in range(min_c, max_c + 1):
            ordered_arr[-1].append(ordered_map[(i, j)])

    resolved = []
    for ordered_row in ordered_arr:
        resolved.append(np.hstack([node.tile.transformed[1:-1, 1:-1] for node in ordered_row]))
    return np.vstack(resolved)

def find_sea_monsters(resolved):
    WINDOW = np.array([
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
        [1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,1],
        [0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0],
    ])
    USED_HASHTAGS = np.copy(resolved)
    monsters = 0
    for r in range(resolved.shape[0] - WINDOW.shape[0] + 1):
        for c in range(resolved.shape[1] - WINDOW.shape[1] + 1):
            section = resolved[r:r+WINDOW.shape[0], c:c+WINDOW.shape[1]]
            if ((section * WINDOW) == WINDOW).sum() == WINDOW.size:
                monsters += 1
                USED_HASHTAGS[r:r+WINDOW.shape[0], c:c+WINDOW.shape[1]] -= WINDOW
    return (monsters > 0), np.count_nonzero(USED_HASHTAGS == 1)

def part_1(tiles):
    _, _, _, _, _, borders = make_dbs(tiles)
    corners = identify_corner_tiles(tiles, borders)
    return functools.reduce(operator.mul, [t.id for t in corners], 1)

def part_2(tiles):
    *extras, _ = make_dbs(tiles)
    root_node = TileNode(tiles[0])
    solve_jigsaw(tiles[0], set(t.id for t in tiles) - {tiles[0].id}, root_node, *extras)
    resolved = resolve_tile_map(root_node)
    for rot in range(4):
        for flip in range(2):
            transformed = resolved
            if flip:
                transformed = np.flip(transformed, axis=1)
            transformed = np.rot90(transformed, k=rot)
            valid, num_unused = find_sea_monsters(transformed)
            if valid:
                return num_unused


if __name__ == '__main__':
    part1 = AdventProblem(20, 1, preprocess, 'file')
    part1.add_solution(part_1)
    part1.run()

    part2 = AdventProblem(20, 2, preprocess, 'file')
    part2.add_solution(part_2)
    part2.run()
