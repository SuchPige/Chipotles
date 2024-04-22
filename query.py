import pandas as pd
import geopandas as gpd
from scipy.spatial import KDTree
from geopy.distance import geodesic
from geopy.point import Point
from shapely.geometry import Polygon, Point

from index import build_index_rtree
from index import build_index_quadtree
from index import build_index_kdtree
from db import get_df
from measurement import measure_start, measure_end, measure_output, print_title


# inform of using AI
# chat GPT 3.5 is used mainly for selecting library and methods while coding
# code generated from AI has been debugged and modified

# retrieve data
df = get_df()

# build index
# rtree
start = measure_start()

# execution part
idx_rtree = build_index_rtree(df)

end = measure_end()
print_title("Index building", "building r-tree index", "r-tree")
measure_output(start, end)
print("\n")

# quadtree
start = measure_start()

# execution part
idx_quadtree = build_index_quadtree(df)

end = measure_end()
print_title("Index building", "building quadtree index", "quadtree")
measure_output(start, end)
print("\n")

# kd-tree
start = measure_start()

# execution part
idx_kdtree = build_index_kdtree(df)

end = measure_end()
print_title("Index building", "building kd-tree index", "kd-tree")
measure_output(start, end)
print("\n")


# Task 1
# get all points of a rectangle area (-83, 37, -80, 40)
lon_min, lat_min, lon_max, lat_max = -83, 37, -80, 40

# rtree
start = measure_start()

# execution part
result = idx_rtree.intersection((lon_min, lat_min, lon_max, lat_max))

end = measure_end()
print_title("1", "get all points of a rectangle area (-82, 38, -80, 40)", "r-tree")
measure_output(start, end)

task1a = [df.iloc[result]]
print("Query result:")
for tuple in task1a:
    print(tuple)
print("\n")

# quadtree
start = measure_start()

# execution part
result = idx_quadtree.intersect((lon_min, lat_min, lon_max, lat_max))

end = measure_end()
print_title("1", "get all points of a rectangle area (-82, 38, -80, 40)", "quadtree")
measure_output(start, end)

task1b = [df.iloc[result]]
print("Query result:")
for tuple in task1b:
    print(tuple)
print("\n")


# linear scan
start = measure_start()

# execution part
task1c = df[(df['longitude'] >= lon_min) & 
            (df['longitude'] <= lon_max) &
            (df['latitude'] >= lat_min) & 
            (df['latitude'] <= lat_max)]

end = measure_end()
print_title("1", "get all points of a rectangle area (-82, 38, -80, 40)", "linear scan")
measure_output(start, end)

print("Query result:")
print(task1c)
print("\n")


# Task 2
# get 15 nearest points by the coordinate (-70, 40)
lon, lat = -70, 40

# kdtree
start = measure_start()

# execution part
points = idx_kdtree.query((lon, lat), k=15)[1]

end = measure_end()
print_title("2", "get 15 nearest points by the coordinate (-70, 40)", "kd-tree")
measure_output(start, end)

task2a = df.iloc[points]
print("Query result:")
print(task2a)
print("\n")

# rtree
start = measure_start()

# execution part
points = idx_rtree.nearest((lon, lat), 15)

end = measure_end()
print_title("2", "get 15 nearest points by the coordinate (-70, 40)", "r-tree")
measure_output(start, end)

task2b = df.iloc[list(points)]
print("Query result:")
print(task2b)
print("\n")


# Task 3
# get all points with the range 12 km from the coordinate(-118, 34)
lon, lat = -118, 34
distance_range = 12

# kdtree
result = []
start = measure_start()

# execution part
points = idx_kdtree.query_ball_point((lon, lat), distance_range)
for point in points:
    row = df.iloc[point]
    distance = geodesic((lat, lon), (row['latitude'], row['longitude'])).km
    if distance <= distance_range:
        result.append(row)
        
end = measure_end()
print_title("3", "get all points with the range 12 km from the coordinate(-118, 34)", "kd-tree filter followed by linear scan")
measure_output(start, end)

task3b = pd.DataFrame(result)
print("Query result:")
print(task3b)
print("\n")

# linear scan
result = []
start = measure_start()

# execution part
for id, row in df.iterrows():
    latitude, longitude = row['latitude'], row['longitude']
    distance = geodesic((lat, lon), (latitude, longitude)).km
    if distance <= distance_range:
        result.append(row)

end = measure_end()
print_title("3", "get all points with the range 12 km from the coordinate(-118, 34)", "linear scan")
measure_output(start, end)

task3a = pd.DataFrame(result)
print("Query result:")
print(task3a)
print("\n")


# Task 4
# get all points with the 5-gon (-85 39, -79 38, -81 35, -83 35, -82 38, -85 39)
lons = [-85, -79, -81, -83, -82, -85]
lats = [39, 38, 35, 35, 38, 39]
polygon = Polygon(zip(lons, lats))

# kd-tree
points= []
start = measure_start()

# execution part
for id, point in enumerate(idx_kdtree.data):
    if polygon.contains(Point(point[0], point[1])):
        points.append(id)

end = measure_end()
print_title("4", "range search within polygon area (-85 39, -79 38, -81 35, -83 35, -82 38, -85 39)", "kd-tree")
measure_output(start, end)

task4a = df.iloc[points]
print("Query result:")
print(task4a)
print("\n")

# linear scan
result = []
start = measure_start()

# execution part
for id, row in df.iterrows():
    point = Point(row['longitude'], row['latitude'])
    if polygon.contains(point):
        result.append(row)

end = measure_end()
print_title("4", "range search within polygon area (-85 39, -79 38, -81 35, -83 35, -82 38, -85 39)", "linear scan")
measure_output(start, end)

task4b = pd.DataFrame(result)
print("Query result:")
print(task4b)
print("\n")
