"""
KNN Algorithm

Outline

1. Generate 10 2-dim. pts in random
2. Plot the 10 pts
3. Calculate distance between any two pts
# 4. Sort
# 5. Plot the relationship

"""

import numpy as np

# 1. Generate 10 2-dim. pts in random
np.random.seed(123)
pts_coord = np.random.rand(10, 2)

# 2. Plot the 10 pts
import matplotlib.pyplot as plt
import seaborn
seaborn.set()

x_coord = pts_coord[:, 0]
y_coord = pts_coord[:, 1]
plt.scatter(x_coord, y_coord, s = 100)

# 3. Calculate distance between any two pts
# pts_coord[:, np.newaxis].shape
# pts_coord[np.newaxis, :].shape

diff = pts_coord[:, np.newaxis] - pts_coord[np.newaxis, :]
# diff.shape

diff_square = diff ** 2 

dist_square = diff_square.sum(axis = 2) # 3rd coordinate
# dist_square.shape

dist_square.diagonal()


# 4. Sort
sort_dist_square = np.sort(dist_square, axis = 1) # sort for each row
order_dist_square = np.argsort(dist_square, axis = 1) # sort for each row

K = 2
partit_nearest_K = np.argpartition(dist_square, K + 1, axis = 1)


# 5. Plot the relationship
plt.scatter(x_coord, y_coord, s = 100)

for each_pt in range(len(partit_nearest_K)):
    for one_of_all_pts in partit_nearest_K[each_pt, : K+1]:
        plt.plot(*zip(pts_coord[each_pt], pts_coord[one_of_all_pts]),
                 color = "g")
plt.savefig("02_1 KNN Relationship Plot.png")



