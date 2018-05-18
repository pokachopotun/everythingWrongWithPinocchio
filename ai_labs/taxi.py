import gym
import numpy as np
import time

def get_train_data(policy):
    env = gym.make("Taxi-v2")
    perc = 0.5
    n_agents = 100
    states = list()
    actions = list()
    balance = list()
    for _ in range(n_agents):
        moves = 0
        state = env.reset()
        # env.render()
        st = list()
        ac = list()
        bal = 0
        while True:
            action = np.random.choice(range(6), p=policy[state])
            # actions = {"s" : 0, "w":1, "d":2, "a":3, "p":4, "o":5}
            # choice = int(actions[ input("wasd op:").strip() ])
            st.append(state)
            ac.append(action)
            state, reward, done, info = env.step(action)
            bal += reward
            moves += 1
            # env.render()
            # time.sleep(1)
            if done:
                actions.append(ac)
                states.append(st)
                balance.append(bal)
                break
            if not done and moves >= 10000:
                break

    balance, states, actions = (list(t) for t in zip(*sorted(zip( balance, states, actions))))
    return states, actions, balance

def train(policy):
    n_epoch = 100
    threshold = -250
    perc = 0.5
    for epoch_id in range(n_epoch):
        print("training epoch id", epoch_id)
        states, actions, balance = get_train_data(policy)
        cnt = len(states) # int(len(states) * perc)
        new_policy = np.zeros_like(policy)
        selected_cnt  = 0
        for i in range(cnt):
            if balance[i] <= threshold:
                continue
            selected_cnt += 1
            for s, a in zip(states[i], actions[i]):
                new_policy[s][a] += 1
        for i in range(len(new_policy)):
            tmp = sum(new_policy[i])
            if tmp != 0:
                new_policy[i] /= tmp
            else:
                new_policy[i] = policy[i]
        policy = new_policy
        # print("selected_cnt", selected_cnt)
        test_policy(policy)
    return policy

def test_policy(policy, times = 100):
    env = gym.make("Taxi-v2")
    n_agents = times
    avg = 0
    for agent_id in range(n_agents):
        state = env.reset()
        # env.render()
        bal = 0
        while True:
            action = np.random.choice(range(6), p=policy[state])
            state, reward, done, info = env.step(action)
            bal += reward
            # env.render()
            # time.sleep(1)
            if done:
                # print("Test agent", agent_id, "balance", bal)
                avg += bal/times
                break
    print("Test", times ,"run avg", avg)



if __name__ == "__main__":
    n_actions = 6
    n_states = 500
    policy = np.ones((n_states, n_actions)) / n_actions
    policy = train(policy)

