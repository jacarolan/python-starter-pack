# keep these three import statements
import game_API
import fileinput
import json

# your import statements here
import random
import copy
import math

first_line = True # DO NOT REMOVE

# global variables or other functions can go here
stances = ["Rock", "Paper", "Scissors"]

##########################################################################################

def get_value(node, pastgame, nodes_traversed):

    if nodes_traversed == 7:
        return 0

    game = copy.deepcopy(pastgame)

    adjacent_nodes = game.get_adjacent_nodes()

    me = game.get_self()
    opponent = game.get_opponent()

    if pastgame.has_monster(node):
        monster = game.get_monster(node)

        delta_time = monster.respawn_counter-monster.respawn_rate

        fight_time = 0

        if delta_time < 7-me.speed:
            fight_time = math.ceil(monster.get_health / me.get_damage)

        value = monster_value(node) / (delta_time + fight_time)

        for node in adjacent_nodes:
            value += get_value(node, game, nodes_traversed + 1)

        return value
    else:
        value = 0

        for node in adjacent_nodes:
            value += get_value(node, game, nodes_traversed + 1)

        return value

#This should return the relative value of travelling to specified node
def node_value(node, game):

    return random.random()
    #get_value(node, game, 0)

def best_stance_no_monster(me, opponent):
    return stances[random.randint(0,2)]

def best_stance_with_monster(me, opponent, monster):
    return best_stance_no_monster(me, opponent)

##########################################################################################

def monsterWillBeAlive(node, game):
    if not game.has_monster(node):
        return False
    return (not game.get_monster(node).dead) or (game.get_monster(node).respawn_counter == 1)

def get_winning_stance(stance):
    if stance == "Rock":
        return "Paper"
    elif stance == "Paper":
        return "Scissors"
    elif stance == "Scissors":
        return "Rock"

# main player script logic
# DO NOT CHANGE BELOW ----------------------------
for line in fileinput.input():
    if first_line:
        game = game_API.Game(json.loads(line))
        first_line = False
        continue
    game.update(json.loads(line))
# DO NOT CHANGE ABOVE ---------------------------

    # code in this block will be executed each turn of the game

    me = game.get_self()
    opponent = game.get_opponent()

    # Determines destination node
    if me.location == me.destination:
        maxVal = node_value(me.location, game)
        destination_node = me.location

        for node in game.get_adjacent_nodes(me.location):
            current_value = node_value(node, game)

            if current_value > maxVal:
                destination_node = node
                maxVal = current_value

    else:
        # Waiting for movement counter; should not change destination since that resets counter
        destination_node = me.destination

    # Determines node on next turn

    nextNode = 0
    if me.movement_counter == me.speed + 1:
        nextNode = destination_node
    else:
        nextNode = me.location

    # Determines best stance, only calls function when dealing with other player
    if monsterWillBeAlive(nextNode, game):
        if opponent.location == nextNode:
            chosen_stance = best_stance_with_monster(me, opponent, game.get_monster(nextNode))
        else:
            # if there's a monster at my location, choose the stance that damages that monster
            chosen_stance = get_winning_stance(game.get_monster(nextNode).stance)
    else:
        chosen_stance = best_stance_no_monster(me, opponent)

    # submit your decision for the turn (This function should be called exactly once per turn)
    game.submit_decision(destination_node, chosen_stance)