import math


class City:
    def __init__(self, name, lat, long):
        self.name = name
        self.lat = lat
        self.long = long

    def __repr__(self):
        return self.name + ', ' + str(self.lat) + ', ' + str(self.long)



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

def distance_on_unit_sphere(lat1, long1, lat2, long2):

    # Convert latitude and longitude to
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0

    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians

    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians

    # Compute spherical distance from spherical coordinates.

    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta', phi')
    # cosine( arc length ) =
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length

    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth
    # in your favorite set of units to get length.
    arc *= 6371
    return arc

def split_by_median(sorted_points):
    half = len(sorted_points)//2
    first_half = []
    second_half = []
    middle = (sorted_points[half-1]['long'] +sorted_points[half]['long'])//2
    for i, point in enumerate(sorted_points):
        if i < half:
            first_half.append(point)
        elif i >= half:
            second_half.append(point)
    return first_half, second_half


def find_middle_line_by_long(sorted_points):
    half = len(sorted_points)//2
    return (sorted_points[half-1].long + sorted_points[half]) // 2


def check_neighboring_points(lat, long, sorted_by_longitude, min_so_far):
    return


def find_closest_pair(sorted_by_y):
    # base cases
    if len(sorted_by_y) == 2:
        return sorted_by_y[0], sorted_by_y[1], find_distance(sorted_by_y[0].lat, sorted_by_y[0].long, sorted_by_y[1].lat, sorted_by_y[1].long)

    if len(sorted_by_y) == 3:
        a = find_distance(sorted_by_y[0].lat, sorted_by_y[0].long, sorted_by_y[1].lat, sorted_by_y[1].long)
        b = find_distance(sorted_by_y[1].lat, sorted_by_y[1].long, sorted_by_y[2].lat, sorted_by_y[2].long)
        c = find_distance(sorted_by_y[2].lat, sorted_by_y[2].long, sorted_by_y[0].lat, sorted_by_y[0].long)
        shortest_dist = min(a,b,c)
        if shortest_dist == a:
            return sorted_by_y[0], sorted_by_y[1], a
        elif shortest_dist == b:
            return sorted_by_y[1], sorted_by_y[2], b
        else:
            return sorted_by_y[2], sorted_by_y[0], c

    # split using median



    # conquer
    # if len(first_half) > 1:
    #     shortest_south_city1, shortest_south_city2, shortest_south_dist = find_closest_pair(first_half)
    # else:
    #     shortest_south_dist = 25000
    #
    # if len(second_half) > 1:
    #     shortest_north_city1, shortest_north_city2, shortest_north_dist = find_closest_pair(second_half)
    # else:
    #     shortest_north_dist = 25000
    #
    # shortest_so_far = min(shortest_south_dist, shortest_north_dist)
    #
    # if shortest_so_far == shortest_south_dist:
    #     shortest_pairs = shortest_south_city1, shortest_south_city2
    # else:
    #     shortest_pairs = shortest_north_city1, shortest_north_city2
    #
    # # merge
    # possible_north_range = middle + shortest_so_far
    # possible_south_range = middle - shortest_so_far
    #
    # points_in_south_range = []
    # points_in_north_range = []
    # for point in sorted_by_y:
    #     if possible_south_range <= point.long <= middle:
    #         points_in_south_range.append(point)
    #
    #     elif middle <= point.long <= possible_north_range:
    #         points_in_north_range.append(point)
    #
    # for point_in_south in points_in_south_range:
    #     for point_in_north in points_in_north_range:
    #         distance = find_distance(point_in_south.lat, point_in_south.long, point_in_north.lat, point_in_north.long)
    #         if distance < shortest_so_far:
    #             shortest_so_far = distance
    #             shortest_pairs = point_in_south.city, point_in_north.city
    #
    # return shortest_pairs

#n = int(input())
file = open('2015A3_sample_input.in', 'r')

#outputfile = open('myoutput.txt','w')
n = file.readline()

n = int(n)
points = []

for _ in range(n):
    #city, latitude, longitude = input().split()
    city, latitude, longitude = file.readline().split()
    points.append(City(city, float(latitude), float(longitude)))

sorted_by_latitude = sorted(points, key=lambda point: point.lat)
sorted_by_longitude = sorted(points, key=lambda point: point.long)

print(sorted_by_longitude)


print(find_distance(52.523405, 13.4114, 51.050991, 13.733634))
file.close()
#print(find_closest_pair(sorted_by_longitude))
# print(split_by_median([1,2]))
