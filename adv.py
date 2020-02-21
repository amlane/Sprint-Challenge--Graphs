from room import Room
from player import Player
from world import World
from utils import Stack, Queue  # These may come in handy
import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
# traversal_path = ['s', 'w', 'e', 'n', 'n', 's']
traversal_path = []


def flip_dir(dir):
    if dir == "n":
        return "s"
    if dir == "s":
        return "n"
    if dir == "w":
        return "e"
    if dir == "e":
        return "w"
    else:
        return "error"


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


def dft_walker():
    visited = {}
    count = 0

    # put the first room in the dictionary
    visited[player.current_room.id] = {}
    # while count < 100:
    #     count += 1
    while len(visited) < len(room_graph):
        # Sets any directions not yet explored to "?" in visited
        for direction in player.current_room.get_exits():
            if direction not in visited[player.current_room.id]:
                # if it doesn't, add it with a value of "?"
                visited[player.current_room.id][direction] = "?"
                # if it does, don't do anything - done

        # if there are not unexplored rooms, do this...
        if "?" not in visited[player.current_room.id].values():
            # pick a random room until you find an unexplored room
            exits = player.current_room.get_exits()
            random.shuffle(exits)
            dir = exits[-1]
            prev_room_id = player.current_room.id
            # travel to the new room
            player.travel(dir)
            # log the direction in traversal path
            traversal_path.append(dir)

        else:
            # if there are unexplored rooms...
            # picks an unexplored room and travels to it, updates the traversal path and updates visited
            exits = player.current_room.get_exits()
            random.shuffle(exits)
            dir = exits[-1]
            # if the room is unexplored...
            if visited[player.current_room.id][dir] == "?":
                # remember the prev room id
                prev_room_id = player.current_room.id
                # travel to the new room
                player.travel(dir)
                # log the direction in traversal path
                traversal_path.append(dir)
                # update the entry in visited ditionary
                visited[prev_room_id][dir] = player.current_room.id
                visited[player.current_room.id] = {}
                visited[player.current_room.id][flip_dir(dir)] = prev_room_id
        # print(visited)


dft_walker()

print(traversal_path)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")