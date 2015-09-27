
def triangle_chain():
    file = open('input.txt', 'r')
    n = int(file.readline())
    counter = 1
    while n != 0 and counter < 7:
        triangles = []
        possible_sides = []

        for i in range(n):
            side1, side2, side3, grayscale = file.readline().split()
            triangles.append(([int(side1), int(side2), int(side3)], float(grayscale)))
            triangles.append(([int(side2), int(side3), int(side1)], float(grayscale)))
            triangles.append(([int(side3), int(side1), int(side2)], float(grayscale)))

        sorted_triangles = sorted(triangles, key=lambda triangle: triangle[1])

        for triangle in sorted_triangles:
            possible_sides.append(triangle[0])

        to_the_right_of = [x for x in range(n*3)]
        max_triangles = [1] * n * 3
        print(possible_sides)
        print(sorted_triangles)

        for i in range(n):
            #print('!!!!' + str(i))
            i_possible_sides = possible_sides[i]
            igrayscale = sorted_triangles[i][1]

            for j in range(i+1, n):
                #print('===' + str(j))
                j_original_sides = sorted_triangles[j][0]
                sides_copy = list(j_original_sides)

                side_to_try = j_original_sides[0]
                jgrayscale = sorted_triangles[j][1]

                #print('i possible sides ', i_possible_sides)
                #print('j original sides ', j_original_sides)
                if side_to_try in i_possible_sides:
                    feasible = True
                feasible = list(set(i_possible_sides) & set(j_original_sides))
                #print(feasible)
                #print(possible_sides)
                if feasible and igrayscale < jgrayscale:
                    #still have not really increased
                    if max_triangles[i] + 1 > max_triangles[j]:
                        max_triangles[j] += 1
                        to_the_right_of[j] = i
                        sides_copy.remove(feasible[0])
                        possible_sides[j] = sides_copy

        #print(max_triangles)
        print('Case', counter , ': ',  max(max_triangles))
        n = int(file.readline())
        counter += 1

triangle_chain()

