def triangle_chain():
    n = int(input())

    triangles = []
    possible_sides = []

    for i in range(n):
        side1, side2, side3, grayscale = input().split()
        triangles.append(([int(side1), int(side2), int(side3)], float(grayscale)))
        triangles.append(([int(side2), int(side3), int(side1)], float(grayscale)))
        triangles.append(([int(side3), int(side1), int(side2)], float(grayscale)))

    sorted_triangles = sorted(triangles, key=lambda triangle: triangle[1])

    for triangle in sorted_triangles:
        possible_sides.append(triangle[0])

    to_the_right_of = [x for x in range(n*3)]
    max_triangles = [1] * n * 3

    for i in range(n * 3):
        # print('!!!!' + str(i))
        i_possible_sides = possible_sides[i]
        igrayscale = sorted_triangles[i][1]

        for j in range(i+1, n * 3):
            jgrayscale = sorted_triangles[j][1]

            if igrayscale < jgrayscale:
                #print('===' + str(j))
                j_original_sides = sorted_triangles[j][0]
                sides_copy = list(j_original_sides)

                side_to_try = j_original_sides[0]
                feasible = False
                # print('i possible sides ', i_possible_sides)
                # print('j original sides ', side_to_try)
                if side_to_try in i_possible_sides:
                    feasible = True
                # print(feasible)

                if feasible and max_triangles[i] + 1 > max_triangles[j]:
                    max_triangles[j] = max_triangles[i]+ 1
                    to_the_right_of[j] = i
                    sides_copy.remove(side_to_try)
                    possible_sides[j] = sides_copy

    print(max(max_triangles))

triangle_chain()

