class Person:
    def __init__(self, preference):
        self.preference = preference
        self.queue = preference
        self.takenTo = False

def gale_shapley():
    n = int(input())
    instance = 0
    output = ''
    while n != 0:
        instance += 1
        blue_node_preferences = {}
        pink_node_preferences = {}
        bachelor = [x+1 for x in range(n)]
        blue_nodes = [x+1 for x in range(n)]

        for i in range(n):
            preference = input().split()
            preference_list = list(map(int, preference))
            blue_node_preferences[i+1] = Person(preference_list)

        for i in range(n):
            preference = input().split()
            pink_node_preferences[i+1] = Person(list(map(int, preference)))

        taken_nodes = set()
        taken_pink_nodes = 0

        while taken_pink_nodes < n:
            for blue_node in bachelor:
                unproposed = blue_node_preferences[blue_node].queue[0]
                if unproposed not in taken_nodes:
                    pink_node_preferences[unproposed].takenTo = blue_node
                    blue_node_preferences[blue_node].takenTo = unproposed
                    taken_nodes.add(unproposed)
                    bachelor.remove(blue_node)
                    taken_pink_nodes += 1

                elif unproposed in taken_nodes:
                    nodeTakenTo = pink_node_preferences[unproposed].takenTo
                    if pink_node_preferences[unproposed].preference.index(blue_node) < pink_node_preferences[unproposed].preference.index(nodeTakenTo):
                        pink_node_preferences[unproposed].takenTo = blue_node
                        blue_node_preferences[blue_node].takenTo = unproposed
                        bachelor.append(nodeTakenTo)

                blue_node_preferences[blue_node].queue.remove(unproposed)
                blue_node_preferences[blue_node].queue.append(unproposed)
        output = output + 'Instance ' + str(instance) + ':\n'
        for blue_node in blue_nodes:
            output = output + str(blue_node_preferences[blue_node].takenTo) + '\n'
        n = int(input())
    print(output[:-1])

gale_shapley()
