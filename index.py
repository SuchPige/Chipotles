import rtree
import pyqtree
from scipy.spatial import KDTree
import pandas


# r-tree index build
def build_index_rtree(df: pandas.DataFrame):
    # creat index
    idx = rtree.Index()

    # insert data
    for id, row in df.iterrows():
        idx.insert(id, (row['longitude'], row['latitude'], row['longitude'], row['latitude']))

    return idx


# quadtree index build
def build_index_quadtree(df: pandas.DataFrame):
    # create index
    idx = pyqtree.Index(bbox=(-130, 20, -60, 50))

    # insert data
    for id, row in df.iterrows():
        idx.insert(item=id, bbox=(row['longitude'], row['latitude'], row['longitude'], row['latitude']))

    return idx


# kd-tree index build
def build_index_kdtree(df: pandas.DataFrame):
    # extract id, latitude, and longitude columns from the DataFrame
    coordinates = df[['longitude', 'latitude']].values

    # create index
    idx = KDTree(coordinates, leafsize=3000)

    return idx
