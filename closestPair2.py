import math
from collections import deque
import cProfile


class City:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def __repr__(self):
        return '{' + self.name + ', ' + str(self.x) + ', ' + str(self.y) + '} '


# remember that for me the x is the long and y is the lat
# def distance(city1, city2):
#     if (city1.name == 'Hvypvvovaguvhefwqh' and city2.name == 'Qcsdgdautpmoldhbm') or (city2.name == 'Hvypvvovaguvhefwqh' and city1.name == 'Qcsdgdautpmoldhbm'):
#        print("YOOOOO44!!!!")
#     theta = city1.x - city2.x
#     dist = math.sin(math.radians(city1.y)) * math.sin(math.radians(city2.y)) + math.cos(math.radians(city1.y)) * math.cos(math.radians(city2.y)) * math.cos(math.radians(theta))
#     if dist.real > 1:
#        dist = 0
#     elif dist.real < -1:
#        dist = math.pi
#     else:
#        dist = math.acos(dist)
#     return math.degrees(dist) * 60 * 1.1515 * 1.609344

def distance(city1, city2):
    theta = city1.y - city2.y
    dist = math.sin(math.radians(city1.x)) * math.sin(math.radians(city2.x)) + math.cos(math.radians(city1.x)) * math.cos(math.radians(city2.x)) * math.cos(math.radians(theta))
    if dist.real > 1:
       dist = 0
    elif dist.real < -1:
       dist = math.pi
    else:
       dist = math.acos(dist)
    return math.degrees(dist) * 60 * 1.1515 * 1.609344


def split_by_median(sorted_by_x):
    half = len(sorted_by_x)//2

    left_by_x = sorted_by_x[:half+1]
    right_by_x = sorted_by_x[half:]

    x_of_halfway = right_by_x[0].x

    left_by_y = sorted(left_by_x, key=lambda point: point.y)
    right_by_y = sorted(right_by_x, key=lambda point: point.y)
    return left_by_x, right_by_x, x_of_halfway, left_by_y, right_by_y


def brute_force_closest_pair(points):
    if len(points) == 2:
        return points[0], points[1], distance(points[0], points[1])

    elif len(points) == 3:
        a = distance(points[0], points[1])
        b = distance(points[1], points[2])
        c = distance(points[2], points[0])
        shortest_dist = min(a,b,c)
        if shortest_dist == a:
            return points[0], points[1], a
        elif shortest_dist == b:
            return points[1], points[2], b
        else:
            return points[2], points[0], c


def strip_closest(points_left, points_right):
    left_len = len(points_left)
    right_len = len(points_right)
    min_dist = 30000
    pairs = None
    # for each point in the strip
    for i in range(left_len - 1):
        #look at the next 7 points
        for j in range(i, min(i + 7, right_len)):
            candidate_dist = distance(points_left[i], points_right[j])
            if candidate_dist < min_dist:
                min_dist = candidate_dist
                pairs = points_left[i], points_right[j]

        for m in range(max(i-7, 0), min(right_len, i)):
            candidate_dist = distance(points_left[i], points_right[m])
            if candidate_dist < min_dist:
                min_dist = candidate_dist
                pairs = points_left[i], points_right[m]
    return min_dist, pairs


def closest_pair(sorted_by_x, sorted_by_y):
    if len(sorted_by_x) <= 3:
        return brute_force_closest_pair(sorted_by_x)

    left_by_x, right_by_x, x_of_midpoint, left_by_y, right_by_y = split_by_median(sorted_by_x)

    leftCity1, leftCity2, leftDistance = closest_pair(left_by_x, left_by_y)
    rightCity1, rightCity2, rightDistance = closest_pair(right_by_x, right_by_y)

    if leftDistance < rightDistance:
        shortest_distance = leftDistance
        shortest_pair = leftCity1, leftCity2
    else:
        shortest_distance = rightDistance
        shortest_pair = rightCity1, rightCity2
    the_strip = entire_strip = [p for p in sorted_by_y if (abs(p.x - x_of_midpoint) <= shortest_distance)]
    entire_strip = [p for p in left_by_y if (abs(p.x - x_of_midpoint) <= shortest_distance)]
    entire_stripr = [p for p in right_by_y if (abs(p.x - x_of_midpoint) <= shortest_distance)]

    # TRYING THE BRUTE FORCE WE KNOW THAT LEFT AND RIGHT ARE OK
    # for x in left_by_x:
    #     for y in right_by_x:
    #         if x != y:
    #             new_dist = distance(x, y)
    #             if new_dist < shortest_distance:
    #                 shortest_distance = new_dist
    #                 shortest_pair = x, y
    # for x in the_strip:
    #     for y in the_strip:
    #         if x != y:
    #             new_dist = distance(x, y)
    #             if new_dist < shortest_distance:
    #                 shortest_distance = new_dist
    #                 shortest_pair = x, y

    #THIS IS SEEING IF COMPARING EVERY POINT IN ENTIRE STRIP IS CHECKING IT CORRECT
    len_strip = len(entire_strip)
    len_stripr = len(entire_stripr)
    if len_strip > 1 or len_stripr > 1:
        for i in range(len_strip-1):
            for j in range(i+1, min(i+7, len_stripr)):
                    if entire_strip[i] != entire_stripr[j]:
                        new_dist = distance(entire_strip[i], entire_stripr[j])
                        if new_dist < shortest_distance:
                            shortest_distance = new_dist
                            shortest_pair = entire_strip[i], entire_stripr[j]
    # for x in left_strip:
    #     for y in right_strip:
    #         if x != y:
    #             new_dist = distance(x, y)
    #             if new_dist < shortest_distance:
    #                 shortest_distance = new_dist
    #                 shortest_pair = x, y

    # if len(strip_by_y_left) > 1 or len(strip_by_y_right) > 1:
    #     shortest_dist_in_strip, pairs = strip_closest(strip_by_y_left, strip_by_y_right)
    #     if shortest_dist_in_strip < shortest_distance :
    #         shortest_distance = shortest_dist_in_strip
    #         shortest_pair = pairs

    return shortest_pair[0], shortest_pair[1], shortest_distance


def main():
    file = open('test_case_9.txt', 'r')
    n = file.readline()
    n = int(n)
    scenario = 1
    while n != 0:
        points = []
        for _ in range(n):

            city, latitude, longitude  = file.readline().rsplit(' ', 2)
            # passing longitude as the x and lat as the y!!
            #points.append(City(city, float(longitude), float(latitude)))
            points.append(City(city, float(latitude), float(longitude)))
        sorted_by_x = sorted(points, key=lambda point: point.x)
        sorted_by_y = sorted(points, key=lambda point: point.y)


        city1, city2, dist = closest_pair(sorted_by_x, sorted_by_y)
        if city1.name > city2.name:
            city1, city2 = city2, city1

        print('Scenario ' + str(scenario) + ':')
        print('Closest pair: ' + city1.name + ' ' + city2.name)
        print('Distance: ' + str(round(dist,1)))
        n = file.readline()
        n = int(n)
        scenario += 1

    file.close()

cProfile.run('main()')

