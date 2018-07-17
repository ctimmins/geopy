import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import scipy.spatial

import os, sys, argparse, math, timeit

def build_tree(csv_path):
    coords = pd.read_csv(csv_path, sep=',')
    tree = scipy.spatial.cKDTree(coords.values, leafsize=12, compact_nodes=True, balanced_tree=True, copy_data=True)

    return tree


def find_neighbors_within_radius(tree, query_points, radius=np.inf, k=1):
    dd, ii = tree.query(query_points, k=k, distance_upper_bound=radius)
    ii = filter(lambda x: x != len(tree.data), ii)  # filter out values where index is out of range

    return ii


def find_radius_for_percentile_coverage(tree, query_points, percentile=80):
    dd, ii = tree.query(query_points, k=1)

    return np.percentile(dd, percentile, interpolation='linear')


def find_max_radius_for_kth_neighbor(tree, query_points, k=1000):
    dd, ii = tree.query(query_points, k=[k])

    return dd.max()

def graph(cars, chargers, r=1):
    fig, axes = plt.subplots(nrows=1, sharex=True, sharey=True)
    cmap = plt.get_cmap('hot_r')
    colors = cmap(np.linspace(0, 1, len(chargers.data)))

    ii = cars.query_ball_point(chargers.data, r)
    len_map = map(lambda x: len(x), ii)
    colors = cmap(np.linspace(0, 1, max(len_map)+1))

    for c, i in zip(chargers.data, ii):
        color = colors[len(i)]
        plt.scatter(c[0], c[1], c=color, marker='x')

    axes.set_title('Cars Proximity to Superchargers')
    axes.set_xlabel('X')
    axes.set_ylabel('Y')
    plt.show()


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        arg_parser = argparse.ArgumentParser(description="find nearest points")
        arg_parser.add_argument('--centroids', default='centroids.csv', help='centroids csv file')
        arg_parser.add_argument('--coords', default='coordinates.csv', help='coordinates csv file')
        arg_parser.add_argument('--heatmap', nargs=1, metavar='<radius>', help='show proximity heatmap')

        ns = arg_parser.parse_args(sys.argv[1:])
        if (ns.heatmap is not None):
            cars = build_tree(ns.coords)
            chargers = build_tree(ns.centroids)
            try:
                radius = int(ns.heatmap[0])
            except ValueError:
                print "Invalid radius. Defaulting to 5m"
                radius = 5
            graph(cars, chargers, radius)
        else:
            # answers = run(ns.centroids, ns.coords, ns.out)
            cars = build_tree(ns.coords)
            chargers = build_tree(ns.centroids)
            print "num cars within 5 meters: %s" % len(find_neighbors_within_radius(chargers, cars.data, 5))
            print "num cars within 10 meters: %s" % len(find_neighbors_within_radius(chargers, cars.data, 10))
            print "min radius to cover 80%% of cars: %s m" % find_radius_for_percentile_coverage(chargers, cars.data, 80)
            print "max radius s.t. no more than 1000 cars per charger: %s m" % find_max_radius_for_kth_neighbor(cars, chargers.data, 1000)

    except argparse.ArgumentError as e:
        print e
        sys.exit(-1)
