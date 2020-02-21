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
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
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


def dft_walker():
    # if player's current room is not in the dictionary add it, with an empty dict as it's value
    visited = {}
    if player.current_room.id not in visited:
        # then get available exits for room
        # set each item in direction to a ? in visited for current room id
        tempVar = {}
        for direction in player.current_room.get_exits():
            tempVar[direction] = "?"
        visited[player.current_room.id] = tempVar

    # else, or after that...
    # pick a random unexplored direction from the player's current room
    exits = player.current_room.get_exits()
    random.shuffle(exits)
    dir = exits[-1]
    # if the room is unexplored...
    if visited[player.current_room.id][dir] == "?":
        # remember the prev room id
        prev_room_id = player.current_room.id
        # travel to the new room and log the direction in traversal path
        player.travel(dir)
        traversal_path.append(dir)
        # update the entry in visited ditionary
        visited[prev_room_id][dir] = player.current_room.id
    print(visited)

    # loop until you reach a room with no unexplored paths


dft_walker()


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
