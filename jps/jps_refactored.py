from jps.FastPriorityQueue import FastPriorityQueue
import math
from itertools import repeat

def signum(x):
    if x == 0:
        return 0
    elif x > 0:
        return 1
    else:
        return -1

class JPSField:
    UNINITIALIZED, OBSTACLE = -2, -1 # enum
    WALKABLE = float('inf')  # needs to always be >= cost

    def __init__(self, raw_field, start_x, start_y,
                 corner_cut=False, diagonal_cost=1.414,
                 walkable_fcn=None, heuristic_fcn=None,
                 resumable=False):

        '''
        Create a field to be processed by jump point search

        raw_field        - 2d array representing the cost to get to that node.
        start_x, start_y - the x, y coordinates of the starting position (ints)
        corner_cut       - bool
        diagonal_cost    - cost to move diagonally. Must be between 1 and 2 inclusive.
        walkable_fcn     - f(x, y, cell) -> bool. Defaults to raw_field[x][y] == JPSField.WALKABLE
        heuristic_fcn    - f(x, y, start_x, start_y, cell) -> float. Defaults to the minimum calculated from diagonal_cost and the absolute distances.
        resumable        - whether another search can be calculated using the result of the current search. adds runtime and memory.
        '''
        self.raw_field = raw_field
        self.processed_field = [[JPSField.UNINITIALIZED for x in row] for row in raw_field]        # a copy of field for caching
        self.parents = [[(None, None) for x in row] for row in raw_field]      # references to the jump point parent of each cell
        self.pq = FastPriorityQueue()   # priority queue storing jump points that have yet to be explored
        self.resume_pq = FastPriorityQueue()  # priority queue storing jump points that

        self.goal = None, None
        self.goal_cost = float('inf')

        self.corner_cut = corner_cut
        self.diagonal_cost = diagonal_cost
        self.walkable_fcn = walkable_fcn or JPSField._default_walkable_fcn
        self.goal_set = set()
        self.heuristic_fcn = heuristic_fcn or self._default_heuristic_fcn
        self.resumable = resumable

        if self._visit_cell(start_x, start_y) == JPSField.OBSTACLE:
            raise ValueError('Starting cell is not walkable')
        self._enqueue_search(start_x, start_y)
        self.processed_field[start_x][start_y] = 0

    def _jps(self):
        """
        Main JPS loop. Stops when it finds a goal
        """
        while (not self.pq.empty()):
            px, py = self.pq.pop_task()

            cardinals = ((1,0), (-1,0), (0,1), (0,-1))
            diagonals = ((1,1), (1,-1), (-1,1), (-1,-1))

            # TODO: optimization: only need to explore certain directions if the previous direction is known
            for c in cardinals:
                self._explore_cardinal(px, py, *c)

            for d in diagonals:
                self._explore_diagonal(px, py, *d)

            if self.processed_field[px][py] >= self.goal_cost:
                return

        if self.goal_cost == float('inf'):
            raise ValueError('No path is found')

    def get_jump_point_path(self, goal_set):
        """ Returns a list of jump points from the start to the goal including both endpoints, where each point will be in a line """

        # Verify that a goal is reachable. It may be useful to get a list of all points reachable from the start,
        # in which case this code should be changed.
        self.goal_set = {g for g in goal_set if self._visit_cell(*g) != JPSField.OBSTACLE}
        if not self.goal_set:
            raise ValueError('No possible goals!')

        # Check if the goal has already been reached. Otherwise try to reach it
        min_x, min_y = min(goal_set, key=lambda g: self._visit_cell(*g))
        if self.processed_field[min_x][min_y] != JPSField.WALKABLE:
            self.goal = min_x, min_y
            self.goal_cost = self.processed_field[min_x][min_y]
        else:
            self._jps()

        # Reconstruct the path
        cur_x, cur_y = self.goal
        path = []
        while cur_x != None and cur_y != None:
            path.append((cur_x, cur_y))
            cur_x, cur_y = self.parents[cur_x][cur_y]
        return path[::-1]

    def get_full_path(self, goal_set):
        """
        Returns a list of points from the start to the goal including both endpoints, where each point will be one step apart.
        """
        path = self.get_jump_point_path(goal_set)
        result = []
        for i in range(len(path) - 1):
            cur_x, cur_y = path[i]
            dir_x = signum(path[i + 1][0] - cur_x)
            dir_y = signum(path[i + 1][1] - cur_y)

            if dir_x == 0:
                xs = repeat(cur_x)
            else:
                xs = range(cur_x, path[i+1][0], dir_x)
            if dir_y == 0:
                ys = repeat(cur_y)
            else:
                ys = range(cur_y, path[i+1][1], dir_y)

            result.extend(zip(xs, ys))

        # add the final step to the path
        result.append(path[-1])
        return result

    def get_path_length(self, goal_set):
        self.get_jump_point_path(goal_set)
        return self.goal_cost

    def _explore_cardinal(self, start_x, start_y, dir_x, dir_y):
        cur_x, cur_y = start_x, start_y # indices of current cell
        cur_cost = self.processed_field[start_x][start_y]

        while True:
            cur_x += dir_x
            cur_y += dir_y
            cur_cost += 1

            if cur_cost > self.goal_cost and not self.resumable:
                return None

            next_cell_type = self._visit_cell(cur_x, cur_y)

            # Check for obstacles and jump points
            if next_cell_type == JPSField.OBSTACLE:
                return None

            # If the next cell has already been explored with lower cost, end this path
            if cur_cost >= self.processed_field[cur_x][cur_y]:
                return None

            # Otherwise explore it
            self.processed_field[cur_x][cur_y] = cur_cost
            self.parents[cur_x][cur_y] = start_x, start_y

           # Check for jump points
            is_jump_point = False
            if not self.corner_cut:
                is_jump_point = is_jump_point or dir_x == 0 and (self._visit_cell(cur_x + 1, cur_y - dir_y) == JPSField.OBSTACLE
                                                        or self._visit_cell(cur_x - 1, cur_y - dir_y) == JPSField.OBSTACLE)
                is_jump_point = is_jump_point or dir_y == 0 and (self._visit_cell(cur_x - dir_x, cur_y + 1) == JPSField.OBSTACLE
                                                        or self._visit_cell(cur_x - dir_x, cur_y - 1) == JPSField.OBSTACLE)
            else:           # TODO: The next cell must also be empty!
                is_jump_point = is_jump_point or dir_x == 0 and (self._visit_cell(cur_x + 1, cur_y) == JPSField.OBSTACLE
                                                        or self._visit_cell(cur_x - 1, cur_y) == JPSField.OBSTACLE)
                is_jump_point = is_jump_point or dir_y == 0 and (self._visit_cell(cur_x, cur_y + 1) == JPSField.OBSTACLE
                                                        or self._visit_cell(cur_x, cur_y - 1) == JPSField.OBSTACLE)
            if is_jump_point:
                self._enqueue_search(cur_x, cur_y)

            # if we've reached a goal, save it. TODO: cache state when enabling resuming search
            if (cur_x, cur_y) in self.goal_set:
                if cur_cost < self.goal_cost:
                    self.goal = (cur_x, cur_y)
                    self.goal_cost = cur_cost
                if not self.resumable:
                    return

    def _explore_diagonal(self, start_x, start_y, dir_x, dir_y):
        """
        Explores field along the diagonal direction for JPS, starting at point (start_x, start_y)

        Parameters
        start_x, start_y - the coordinates to start exploring from.
        direction_x, direction_y - an element from: {(1, 1), (-1, 1), (-1, -1), (1, -1)} corresponding to the x and y directions respectively.

        Return
        A 2-tuple containing the coordinates of the jump point or goal if it found one
        None if no jumppoint or goal was found.
        """

        cur_x, cur_y = start_x, start_y # indices of current cell
        cur_cost = self.processed_field[start_x][start_y]

        while True:
            cur_x += dir_x
            cur_y += dir_y
            cur_cost += self.diagonal_cost

            # If the cost of reaching this cell is > the cost of this cell, we can stop processing.
            # To resume the search, we will need to cache this result.
            if cur_cost > self.goal_cost and not self.resumable:
                return None

            # Handle the current cell
            next_cell_type = self._visit_cell(cur_x, cur_y)

            # If we reach an obstacle, end this path
            if next_cell_type == JPSField.OBSTACLE:
                return None

            # Cannot move from 1 to 2 if corner cutting is disabled
            # . # 2
            # . 1 .
            if (not self.corner_cut and (self._visit_cell(cur_x - dir_x, cur_y) == JPSField.OBSTACLE or
                                          self._visit_cell(cur_x, cur_y - dir_y) == JPSField.OBSTACLE)):
                return None
            # Cannot move from 1 to 2.
            # . # 2
            # . 1 #
            if (self._visit_cell(cur_x - dir_x, cur_y) == JPSField.OBSTACLE and
                self._visit_cell(cur_x, cur_y - dir_y) == JPSField.OBSTACLE):
                return None

            # If the next cell has already been explored with lower cost, end this path
            if cur_cost >= self.processed_field[cur_x][cur_y]:
                return None

            # Otherwise explore it
            self.processed_field[cur_x][cur_y] = cur_cost
            self.parents[cur_x][cur_y] = start_x, start_y

            # if we've reached a goal, save it.
            if (cur_x, cur_y) in self.goal_set:
                if cur_cost < self.goal_cost:
                    self.goal = (cur_x, cur_y)
                    self.goal_cost = cur_cost
                if not self.resumable:
                    return

            # Check if this is a jump point. To reach x from 1, we must go through 2.
            # . . 2 .
            # . 1 # x
            if self.corner_cut and (self._visit_cell(cur_x - dir_x, cur_y) == JPSField.OBSTACLE or
                                     self._visit_cell(cur_x, cur_y - dir_y) == JPSField.OBSTACLE):
                self._enqueue_search(cur_x, cur_y)

            # Extend horizontal and vertical searches to check for jumpp points
            self._explore_cardinal(cur_x, cur_y, dir_x, 0)
            self._explore_cardinal(cur_x, cur_y, 0, dir_y)

    def _enqueue_search(self, x, y):
        """
        Add a jump point to the priority queue to be searched later. The priority is the minimum possible number of steps to the destination.
        Also check whether the search is finished.

        Parameters
        pq - a priority queue for the jump point search
        x, y - 2-tuple with the coordinates of a point to add.

        Return
        None
        """
        self.pq.add_task((x, y), self.processed_field[x][y] + self.heuristic_fcn(x, y, self.raw_field[x][y]))

    def _visit_cell(self, x, y):
        '''
        Visits a spot on the field and categorizes it, caching the result.
        Returns the type of this cell
        '''
        if self.processed_field[x][y] == JPSField.UNINITIALIZED:
            if self.walkable_fcn(x, y, self.raw_field[x][y]):
                self.processed_field[x][y] = JPSField.WALKABLE
            else:
                self.processed_field[x][y] = JPSField.OBSTACLE

        return self.processed_field[x][y]

    @staticmethod
    def _default_walkable_fcn(x, y, cell):
        return cell == JPSField.WALKABLE
    def _default_heuristic_fcn(self, x, y, cell):
        """ Function to estimate how far it is from x, y to a goal. """
        goal_costs = [0]
        for gx, gy in self.goal_set:
            dx = abs(gx - x)
            dy = abs(gy - y)
            goal_costs.append(min(dx, dy) * self.diagonal_cost + max(dx, dy) - min(dx, dy))
        return min(goal_costs)


if __name__ == "__main__":
    _map = [
        [-1, -1, -1, -1],
        [-1,  0,  0, -1],
        [-1, -1, -1, -1],
    ]
    field = JPSField(_map, 1, 1)
    path = field.get_jump_point_path(((1, 2),))
    print("path", path)