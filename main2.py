import os
import json
import random

import numpy as np
import time
from copy import deepcopy
from API_Script import API
import math

ACTIONS = ["D", "L", "U", "R"]
ACTIONS_ANALOG = {"D":"S", "L":"W", "U":"N", "R":"E"}
TEAM_ID = 1364
WORLD_ID = 2
EPSILON = True

def get_eps(episode):
    # return math.e ** (-episode/2)
    return 0
    # return 0.5



def move(q, state, episode):
    if state not in q:
        q[state] = [0, 0, 0, 0]

    available_actions = []
    unavailable_actions = []

    for action in ACTIONS:
        if state[0] == 0 and action == 'L':
            unavailable_actions.append('L')
            continue

        if state[0] == 39 and action == 'R':
            unavailable_actions.append('R')
            continue

        if state[1] == 0 and action == 'D':
            unavailable_actions.append('D')
            continue

        if state[1] == 39 and action == 'U':
            unavailable_actions.append('U')
            continue

        available_actions.append(action)

    for action in unavailable_actions:
        q[state][ACTIONS.index(action)] = -np.inf



    if np.random.uniform(0, 1) > get_eps(episode):
        max_q = np.argmax(q[state])
        action = ACTIONS[max_q]
    else:
        if 0 in q[state]:
            while True:
                ind = random.randint(0, 3)
                ac = ACTIONS[ind]
                if ac in available_actions and q[state][ind] == 0:
                    action = ac
                    break
            print(ind, action)
        else:
            action = random.choice(available_actions)




    x = API().make_move(TEAM_ID, ACTIONS_ANALOG[action], WORLD_ID)

    if x["newState"] == None:
        q[state] = [x["reward"]] * 4
        return action, action, x["reward"], state, True

    if x["code"] != "OK":
        print(x["message"])

    new_state = (int(x["newState"]["x"]), int(x["newState"]["y"]))
    move_made = (state[0]-new_state[0], state[1]-new_state[1])

    if move_made[0] == 1 and move_made[1] == 0:
        move_made = "L"
    elif move_made[0] == -1 and move_made[1] == 0:
        move_made = "R"
    elif move_made[0] == 0 and move_made[1] == 1:
        move_made = "D"
    elif move_made[0] == 0 and move_made[1] == -1:
        move_made = "U"


    return action, move_made, x["reward"], (int(x["newState"]["x"]), int(x["newState"]["y"])), False


def get_other_states(state, q):
    x = []

    x.append((state[0] - 1,state[1]))
    x.append((state[0] + 1, state[1]))
    x.append((state[0], state[1] + 1))
    x.append((state[0], state[1] - 1))

    x_new = []
    for i in x:
        if -1 not in i and 39 not in i:
            x_new.append(i)

    for i in x_new:
        if i not in q:
            q[i] = [0, 0, 0, 0]


    return x_new


def get_action(prev_state, new_state):
    move_made = (prev_state[0] - new_state[0], prev_state[1] - new_state[1])

    if move_made[0] == 1 and move_made[1] == 0:
        move_made = "L"
    elif move_made[0] == -1 and move_made[1] == 0:
        move_made = "R"
    elif move_made[0] == 0 and move_made[1] == 1:
        move_made = "D"
    elif move_made[0] == 0 and move_made[1] == -1:
        move_made = "U"

    return move_made





def main():
    # Check if JSON file exists and load Q_values from file if it does
    if os.path.exists(f"World{WORLD_ID}.json"):
        with open(f"World{WORLD_ID}.json", "r") as f:
            zzz = json.load(f)
            Q_values = dict()
            for i in zzz:
                k = tuple(int(j) for j in i.split(','))
                v = zzz[i]
                Q_values[k] = v

    else:
        Q_values = dict()

    for ep in range(20):
        API().reset(TEAM_ID)
        time.sleep(5)

        resp = API().enter_world(WORLD_ID, TEAM_ID)
        ss = resp["state"].split(':')
        ss = (int(ss[0]), int(ss[1]))
        time.sleep(5)

        START_STATE = deepcopy(ss)
        GAMMA = 0.98
        ALPHA = 0.1

        run_rewards = []
        state = deepcopy(START_STATE)
        for i in range(2000):
            action_chosen, action_made, reward, next_state, terminal = move(Q_values, state, ep)
            print("\nQ_Values -> ", Q_values[state], "\naction Chosen: -> ", action_chosen, "\naction Taken: -> ", action_made, "\nreward: -> ", reward, "\nPrev State: -> ", state,
                  "\nnew state: -> ", next_state, "\nscore -> ", API().get_score(TEAM_ID)['score'], "\nStates Explored -> ", len(Q_values))

            if terminal:
                break

            if next_state == state:
                time.sleep(1)
                continue

            if next_state not in Q_values:
                Q_values[next_state] = [0, 0, 0, 0]

            Q_values[state][ACTIONS.index(action_made)] += ALPHA * (
                        reward + GAMMA * np.max(Q_values[next_state]) - Q_values[state][ACTIONS.index(action_made)])

            state = deepcopy(next_state)

            run_rewards.append(reward)
            print("cum_rewards -> ", sum(run_rewards), "\n")
            print('--------------------------------------------------------------------------------------------------------')

            time.sleep(0.1)
           
        with open(f"World{WORLD_ID}.json", "w") as f:
            zzz = dict()
            for i in Q_values:
                print(','.join([str(j) for j in i]), Q_values[i])
                zzz[','.join([str(j) for j in i])] = Q_values[i]
            json.dump(zzz, f)

main()
