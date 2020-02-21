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
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)
# keep track
traversal_path = []
backtrack_path = []

# make a function that returns the flipped direction


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


# keep track of which rooms are visited
visited = {}
# put the first room in the dictionary with the list of exists
visited[player.current_room.id] = player.current_room.get_exits()
# while the length of the visited rooms is less than the number of rooms in the graph - the first room
while len(visited) < len(room_graph) - 1:
    # if the current room has never been visited
    if player.current_room.id not in visited:
        # set the list of exits to the room in both dictionaries
        visited[player.current_room.id] = player.current_room.get_exits()
        last_move = backtrack_path[-1]
        # mark the room you came from as explored
        visited[player.current_room.id].remove(last_move)
    # if there's a dead end...
    while len(visited[player.current_room.id]) < 1:
        # go back
        # remove the last direction from backtrack_path
        backtrack = backtrack_path.pop()
        player.travel(backtrack)
        traversal_path.append(backtrack)

    else:
        # if there are unexplored rooms...
        # pick the first exit
        exit = visited[player.current_room.id].pop(0)
        # append it to the traversal path
        traversal_path.append(exit)
        # store the reverse direction for going back
        backtrack_path.append(flip_dir(exit))
        # travel to the next room
        player.travel(exit)


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
# print(traversal_path)


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
