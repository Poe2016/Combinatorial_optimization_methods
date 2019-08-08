# -*-coding: UTF-8 -*-
# use simulated annealing method to solve TSP
from random import sample, uniform, choice
import math
import sys

# test date file's path
DATA_PATH = 'testdata.txt'
# initial temperature
T = 100
# the minimum temperature
T_MIN = 50
# annealing factor
FACTOR = 0.9


class Point:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)


def load_data(path):
    f_open = open(path)
    lines = f_open.readlines()
    f_open.close()
    point_list = []
    for line in lines[6:len(lines)-1]:
        line_list = line.strip().split()
        point_list.append(Point(line_list[1], line_list[2]))
    return point_list


# return the distance matrix of every two cities
def dist_matrix(point_list):
    num = len(point_list)
    dist = [[0]*num for i in range(num)]
    for i in range(num):
        for j in range(num):
            dist[i][j] = round(math.sqrt(math.pow(point_list[i].x-point_list[j].x, 2) + math.pow(point_list[i].y-point_list[j].y, 2)), 2) if i != j else 0
    return dist


def simulated_annealing(t, t_min, factor, point_list, dist):
    num = len(point_list)
    total_cost = 0
    # the initial sequence of cities
    init_seq = [i for i in range(num)]
    selected_seq = []
    selected_city = 0
    while len(selected_seq) < num:
        if len(selected_seq) == 0:
            selected_city = choice(init_seq)
            init_seq.remove(selected_city)
            selected_seq.append(selected_city)
            continue
        if len(selected_seq) == num:
            break
        left_num = len(init_seq)
        sample_num = left_num // 10 if left_num >= 10 else left_num % 10
        # select cities by random sampling
        sample_list = sample(init_seq, sample_num)
        curr_city = selected_seq[-1]
        cost = sys.maxsize
        sample_city = 0
        t_sample = t
        for city in sample_list:
            t_sample *= factor
            if dist[curr_city][city] < cost:
                cost = dist[curr_city][city]
                sample_city = city
            else:
                r = uniform(0, 1)
                if dist[curr_city][city] > cost and t_sample > t_min and math.exp(dist[curr_city][city] - cost)/t_sample > r:
                    sample_city = city
                    cost = dist[curr_city][city]
                    break
        init_seq.remove(sample_city)
        selected_seq.append(sample_city)
        total_cost += cost
    print '模拟退火得最小开销：', total_cost
    print '选择路径为：', selected_seq





if __name__ == '__main__':
    point_list = load_data(DATA_PATH)
    dist = dist_matrix(point_list)
    simulated_annealing(T, T_MIN, FACTOR, point_list, dist)