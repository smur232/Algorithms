import math

co = math.cos
si = math.sin
aco = math.acos
ra = math.radians
pi = math.pi
deg = math.degrees


class City:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def __repr__(self):
        return '{' + self.name + ', ' + str(self.x) + ', ' + str(self.y) + '} '


def distance(city1, city2):
    theta = city1.y - city2.y
    city1xra = ra(city1.x)
    city2xra = ra(city2.x)
    dist = si(city1xra) * si(city2xra) + co(city1xra) * co(city2xra) * co(ra(theta))
    if dist.real > 1:
       dist = 0
    elif dist.real < -1:
       dist = pi
    else:
       dist = aco(dist)
    return deg(dist) * 60 * 1.1515 * 1.609344


def split_by_median(sorted_by_x, sorted_by_y):
    half = len(sorted_by_x)//2

    left_by_x = sorted_by_x[:half+1]
    right_by_x = sorted_by_x[half:]

    x_of_halfway = right_by_x[0].x

    left_by_y = filter(lambda x: x.y < x_of_halfway, sorted_by_y)
    right_by_y = filter(lambda x: x.y >= x_of_halfway, sorted_by_y)
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
    left_strip = [p for p in left_by_y if (abs(p.x - x_of_midpoint) < shortest_distance)]
    right_strip = [p for p in right_by_y if (abs(p.x - x_of_midpoint) < shortest_distance)]

    #THIS IS SEEING IF COMPARING EVERY POINT IN ENTIRE STRIP IS CHECKING IT CORRECT
    len_left = len(left_strip)
    len_right = len(right_strip)
    if len_left > 1 or len_right > 1:
        for i in range(len_left-1):
            for j in range(i+1, min(i+7, len_right)):
                    if left_strip[i] != right_strip[j]:
                        new_dist = distance(left_strip[i], right_strip[j])
                        if new_dist < shortest_distance:
                            shortest_distance = new_dist
                            shortest_pair = left_strip[i], right_strip[j]

    return shortest_pair[0], shortest_pair[1], shortest_distance


def main():
    n = input()
    n = int(n)
    scenario = 1
    while n != 0:
        points = []
        for _ in range(n):

            city, latitude, longitude = input().rsplit(' ', 2)
            points.append(City(city, float(latitude), float(longitude)))
        sorted_by_x = sorted(points, key=lambda point: point.x)
        sorted_by_y = sorted(points, key=lambda point: point.y)

        city1, city2, dist = closest_pair(sorted_by_x, sorted_by_y)
        if city1.name > city2.name:
            city1, city2 = city2, city1

        print('Scenario ' + str(scenario) + ':')
        print('Closest pair: ' + city1.name + ' ' + city2.name)
        print('Distance: ' + str(round(dist,1)))
        n = input()
        n = int(n)
        scenario += 1

main()
