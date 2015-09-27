def triangle_chain():
    # file = open('multiTest.txt', 'r')
    # n = int(file.readline())
    n = int(input())
    triangles = []

    for i in range(n):
        side1, side2, side3, grayscale = input().split()
        triangles.append(((int(side1), int(side2), int(side3)), float(grayscale)))
        triangles.append(((int(side2), int(side3), int(side1)), float(grayscale)))
        triangles.append(((int(side3), int(side1), int(side2)), float(grayscale)))

    sorted_triangles = sorted(triangles, key=lambda triangle: triangle[1])

    # for triangle in sorted_triangles:
    #     possible_sides.append(triangle[0])
    possible_sides = [triang[0] for triang in sorted_triangles]
    max_triangles = [1] * n * 3

    for i in range(2,n * 3):
        i_possible_sides = possible_sides[i]
        igrayscale = sorted_triangles[i][1]
        i_max_triangle = max_triangles[i]

        for j in range(i+1, n * 3):
            jgrayscale = sorted_triangles[j][1]

            if igrayscale < jgrayscale:
                j_original_sides = sorted_triangles[j][0]
                sides_copy = list(j_original_sides)

                side_to_try = j_original_sides[0]

                if side_to_try in i_possible_sides and i_max_triangle + 1 > max_triangles[j]:
                    max_triangles[j] = i_max_triangle + 1
                    sides_copy.remove(side_to_try)
                    possible_sides[j] = sides_copy

    print(max(max_triangles))



triangle_chain()

