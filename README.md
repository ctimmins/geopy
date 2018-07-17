# Description
The following is my playground for scipy and visualization of nearest-neighbor points.  They could potentially represent the proximity of electric vehicles to superchargers

### Notes
* Please see `geopy/spatial.py` for the implementation
* I have included heatmap png's of the density of cars in proximity to superchargers at various radii


# Usage
**Setup**
```
virtualenv venv
source venv/bin/activate
pip install -r geopy/requirements.txt
```
**CLI Usage**
```
spatial.py [-h] [--centroids CENTROIDS] [--coords COORDS] [--heatmap <radius>]


optional arguments:
  -h, --help            show this help message and exit
  --centroids CENTROIDS
                        centroids csv file
  --coords COORDS       coordinates csv file
  --heatmap <radius>    show proximity heatmap
```

**Python Usage**
```
from geopy.spatial import *

cars = build_tree(path_to_cars_csv)
chargers = build_tree(path_to_chargers_csv)
```

`find_neighbors_within_radius(chargers, cars.data, radius)`

`find_radius_for_percentile_coverage(chargers, cars.data, percentage)`

`find_max_radius_for_kth_neighbor(cars, chargers.data, k)`


# Answers
#### 1. How many cars are within *5* meters of at least one of the superchargers?
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; A: 90,851

#### 2. How many cars are within *10* meters of at least one of the superchargers?
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; A: 315,614

#### 3. What is the minimum radius *R* such that 80% of the cars are within *R* meters of atleast one of the superchargers
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; A: 21.25m

#### 4. What is the maximum radius R such that no single supercharger has more than 1,000 cars within a radius of R meters?
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; A: 31.32m
   

### Complexities
_All answers assume 2-dimensional space e.g. cartesian coordinates_
#### Building the tree

Cars => O(n log n)

Superchargers => O(k log k)

#### Searching the tree
Cars => O(log n) average

Superchargers => O(log k) average