import math
from collections import deque

class City:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def __repr__(self):
        return '{' + self.name + ', ' + str(self.x) + ', ' + str(self.y) + '} '


# remember that for me the x is the long and y is the lat
def distance(self, other):
    theta = self.x - other.x
    dist = math.sin(math.radians(self.y)) * math.sin(math.radians(other.y)) + math.cos(math.radians(self.y)) * math.cos(math.radians(other.y)) * math.cos(math.radians(theta))
    if dist.real > 1:
        dist = 0
    elif dist.real < -1:
        dist = math.pi
    else:
        dist = math.acos(dist)
    dist = math.degrees(dist)
    dist = dist * 60 * 1.1515 * 1.609344
    return dist

def split_by_median(sorted_by_x, sorted_by_y):
    half = len(sorted_by_x)//2

    left_by_x = sorted_by_x[:half]
    right_by_x = sorted_by_x[half:]

    x_of_halfway = left_by_x[-1].x

    # shoudl this be <= ???
    # these are the points on the left and right sorted by y
    left_by_y = list(filter(lambda point: point.x <= x_of_halfway, sorted_by_y))
    right_by_y = list(filter(lambda point: point.x > x_of_halfway, sorted_by_y))
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


def strip_closest(points, shortest_distance):
    lenPoints = len(points)
    found_shorter = False
    # for each point in the strip
    for i in range(lenPoints - 1):
        #look at the next 7 points
        for j in range(i+1, min(i + 8, lenPoints)):
            candidate_dist = distance(points[i], points[j])
            if candidate_dist < shortest_distance:
                found_shorter = True
                mindist = candidate_dist
                pairs = points[i], points[j]
    if found_shorter:
        return mindist, pairs
    else:
        return shortest_distance, None


def closest_pair(sorted_by_x, sorted_by_y):
    if len(sorted_by_x) <= 3:
        return brute_force_closest_pair(sorted_by_x)

    left_by_x, right_by_x, x_of_midpoint, left_by_y, right_by_y = split_by_median(sorted_by_x, sorted_by_y)

    leftCity1, leftCity2, leftDistance = closest_pair(left_by_x, left_by_y)
    rightCity1, rightCity2, rightDistance = closest_pair(right_by_x, right_by_y)

    if leftDistance < rightDistance:
        shortest_distance = leftDistance
        shortest_pair = leftCity1, leftCity2
    else:
        shortest_distance = rightDistance
        shortest_pair = rightCity1, rightCity2

    # points are in the strip if the abs of x - midpoint x is less than delta, it is sorted by y
    # it might be better to use a deque here but for now it is using a list
    strip_by_y = list(filter(lambda point: abs(point.x - x_of_midpoint) < shortest_distance, sorted_by_y))
    #print(len(strip_by_y))
    if len(strip_by_y) > 1:
        shortest_dist_in_strip, pairs = strip_closest(strip_by_y, shortest_distance)
        if pairs:
            shortest_distance = shortest_dist_in_strip
            shortest_pair = pairs

    return shortest_pair[0], shortest_pair[1], shortest_distance


file = open('mytest.txt', 'r')
n = file.readline()
n = int(n)
scenario = 1
while n != 0:
    points = []
    for _ in range(n):
            city, latitude, longitude = file.readline().split()
            # passing longitude as the x and lat as the y!!
            points.append(City(city, float(longitude), float(latitude)))
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