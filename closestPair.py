import math

class City:
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long

def find_distance(lat1, long1, lat2, long2):
    theta = long1 - long2
    dist = math.sin(degrees_to_radians(lat1) * math.sin(degrees_to_radians(lat2)) + math.cos(degrees_to_radians(lat1)) * math.cos(degrees_to_radians(lat2)) * math.cos(theta))
    dist = math.acos(dist)
    dist = radians_to_degrees(dist)
    dist = dist * 60 * 1.1515
    dist *= 1.609344
    return dist


def degrees_to_radians(deg):
    return deg * math.pi/180.0


def radians_to_degrees(rad):
    return rad * 180.0/math.pi


def split_by_median(sorted_points):
    half = len(sorted_points)//2
    first_half = []
    second_half = []
    print(sorted_points)
    print(half)
    middle = (sorted_points[half-1]['long'] +sorted_points[half]['long'])//2
    for i, point in enumerate(sorted_points):
        if i < half:
            first_half.append(point)
        elif i >= half:
            second_half.append(point)
    return first_half, second_half, middle


def check_neighboring_points(lat, long, sorted_by_longitude, min_so_far):
    return


def find_closest_pair(sorted_by_y):
    # base case
    if len(sorted_by_y) == 2:
        return sorted_by_y[0][city],sorted_by_y[1][city],find_distance(sorted_by_y[0]['lat'], sorted_by_y[0]['long'], sorted_by_y[1]['lat'], sorted_by_y[1]['long'])

    # split using median
    first_half, second_half, middle = split_by_median(sorted_by_y)


    # conquer
    if len(first_half) > 1:
        shortest_south_city1, shortest_south_city2, shortest_south_dist = find_closest_pair(first_half)
    else:
        shortest_south_dist = 25000

    if len(second_half) > 1:
        shortest_north_city1, shortest_north_city2, shortest_north_dist = find_closest_pair(second_half)
    else:
        shortest_north_dist = 25000

    shortest_so_far = min(shortest_south_dist, shortest_north_dist)

    if shortest_so_far == shortest_south_dist:
        shortest_pairs = shortest_south_city1, shortest_south_city2
    else:
        shortest_pairs = shortest_north_city1, shortest_north_city2

    # merge
    possible_north_range = middle + shortest_so_far
    possible_south_range = middle - shortest_so_far

    points_in_south_range = []
    points_in_north_range = []
    for point in sorted_by_y:
        if possible_south_range <= point.long <= middle:
            points_in_south_range.append(point)

        elif middle <= point.long <= possible_north_range:
            points_in_north_range.append(point)

    for point_in_south in points_in_south_range:
        for point_in_north in points_in_north_range:
            distance = find_distance(point_in_south.lat, point_in_south.long, point_in_north.lat, point_in_north.long)
            if distance < shortest_so_far:
                shortest_so_far = distance
                shortest_pairs = point_in_south.city, point_in_north.city

    return shortest_pairs

n = int(input())
points = []
for _ in range(n):
    city, latitude, longitude = input().split()
    points.append({'city': city, 'lat': float(latitude), 'long': float(longitude)})

sorted_by_latitude = sorted(points, key=lambda point: point['lat'])
sorted_by_longitude = sorted(points, key=lambda point: point['long'])

#print(sorted_by_longitude)

print(find_closest_pair(sorted_by_longitude))
# print(split_by_median([1,2]))
