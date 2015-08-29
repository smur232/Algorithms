import math


class City:
    def __init__(self, name, lat, long):
        self.name = name
        self.lat = lat
        self.long = long

    def __repr__(self):
        return '{' + self.name + ', ' + str(self.lat) + ', ' + str(self.long) + '} '


def distance(self, other):
    theta = self.long - other.long
    dist = math.sin(math.radians(self.lat)) * math.sin(math.radians(other.lat)) + math.cos(math.radians(self.lat)) * math.cos(math.radians(other.lat)) * math.cos(math.radians(theta))
    if dist.real > 1:
        dist = 0
    elif dist.real < -1:
        dist = math.pi
    else:
        dist = math.acos(dist)
    dist = math.degrees(dist)
    dist = dist * 60 * 1.1515 * 1.609344
    return dist


def split_by_median(sorted_by_long, sorted_by_lat):
    half = len(sorted_by_long)//2

    left_by_long = sorted_by_long[:half]
    right_by_long = sorted_by_long[half:]

    lat_of_halfway = sorted_by_long[half].lat

    left_by_lat = filter(lambda point: point.lat < lat_of_halfway, sorted_by_lat)
    right_by_lat = filter(lambda point: point.lat >= lat_of_halfway, sorted_by_lat)
    return left_by_long, right_by_long, left_by_lat, right_by_lat, half


def find_closest_pair(sorted_by_y, sorted_by_x):

    #returns city1, city2, distance
    # base cases
    if len(sorted_by_y) == 2:
        return sorted_by_y[0], sorted_by_y[1], distance(sorted_by_y[0], sorted_by_y[1])

    if len(sorted_by_y) == 3:
        a = distance(sorted_by_y[0], sorted_by_y[1])
        b = distance(sorted_by_y[1], sorted_by_y[2])
        c = distance(sorted_by_y[2], sorted_by_y[0])
        shortest_dist = min(a,b,c)
        if shortest_dist == a:
            return sorted_by_y[0], sorted_by_y[1], a
        elif shortest_dist == b:
            return sorted_by_y[1], sorted_by_y[2], b
        else:
            return sorted_by_y[2], sorted_by_y[0], c

    # split using median
    elif len(sorted_by_y) > 3:
        first_half, second_half, half, first_half_lat, second_half_lat = split_by_median(sorted_by_y, sorted_by_x)

        #finds the shortest distance from top and bottom
        first_half_city1, first_half_city2, distance1 = find_closest_pair(first_half, first_half_lat)
        second_half_city1, second_half_city2, distance2 = find_closest_pair(second_half, second_half_lat)

        shortest_dist = min(distance1, distance2)

        if shortest_dist == distance1:
            shortest_pair = first_half_city1, first_half_city2
        elif shortest_dist == distance2:
            shortest_pair = second_half_city1, second_half_city2

        halfway = sorted_by_y[half].long
        # find range where the crossing overs could be
        bottom, top = halfway - shortest_dist, halfway + shortest_dist

        bottom_range = []
        top_range = []

        for i, point in enumerate(sorted_by_y):
            if (i < half) and (bottom <= point.long <= halfway):
                bottom_range.append(point)
            elif (i >= half) and (halfway <= point.long <= top):
                top_range.append(point)

        for bottom_point in bottom_range:
            for top_point in top_range:
                candidate_dist = distance(bottom_point, top_point)
                if candidate_dist < shortest_dist:
                    shortest_dist = candidate_dist
                    shortest_pair = bottom_point, top_point
        return shortest_pair[0], shortest_pair[1], shortest_dist


file = open('test_case_0.txt', 'r')

n = file.readline()
n = int(n)
scenario = 1
while n != 0:
    points = []
    for _ in range(n):
            city, latitude, longitude = file.readline().split()
            points.append(City(city, float(latitude), float(longitude)))
    sorted_by_latitude = sorted(points, key=lambda point: point.lat)
    sorted_by_longitude = sorted(points, key=lambda point: point.long)

    city1, city2, dist = find_closest_pair(sorted_by_longitude, sorted_by_latitude)
    if city1.name > city2.name:
        city1, city2 = city2, city1

    print('Scenario ' + str(scenario) + ':')
    print('Closest pair: ' + city1.name + ' ' + city2.name)
    print('Distance: ' + str(round(dist,1)))
    n = file.readline()
    n = int(n)
    scenario += 1


file.close()
