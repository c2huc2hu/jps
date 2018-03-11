# JPS

Python implementation of a jump point search. See [this link](https://harablog.wordpress.com/2011/09/07/jump-point-search/) for a description of the algorithm.

## Features

- Basic jump point search algorithm
- Tested + documented

Support for:
- Enable/ disable corner cutting
- Multiple end nodes
- Custom walkable and heuristic functions

Coming soon:
- Resumable search

## Documentation

1. Create an instance of a field, providing at least the map, start and end points. See `JPSField.__init__` for optional parameters.
By default, it assumes that walkable cells are filled with Infinity (`JPSField.WALKABLE`) and obstacles are filled with -1 (`JPSField.OBSTACLE`).

    search = jps.JPSField(map, start_point, end_point)

2. Make API calls that will return a path to the goal with the lowest cost.

    search.get_jump_point_path(set_of_goal_nodes)
    search.get_full_path(set_of_goal_nodes)
    search.get_path_length(set_of_goal_nodes)

## Contributing

Pull requests are welcome! Please run the tests: `python -m unittest discover`

