# DQN Extensions
> state-of-the-art SOTA
>> benchmark
>>> baseline
***
## types

1.**N-step DQN:** how to improve convergence speed and stability with a simple
unrolling of the Bellman equation, and why it's not an ultimate solution.

2.**Double DQN:** how to deal with DQN overestimation of the values of the
actions

3.**Noisy networks:** how to make exploration more efficient by adding noise
to the network weights

4.**Prioritized replay buffer:** why uniform sampling of our experience is not the
best way to train

5.**Dueling DQN:** how to improve convergence speed by making our network's
architecture represent more closely the problem that we are solving

6.**Categorical DQN:** how to go beyond the single expected value of the action
and work with full distributions

## Basic DQN

>*At the same time, the purpose of this book is not to teach you how to use the existing
libraries, but rather how to develop intuition about RL methods and, if necessary,
implement everything from scratch. From my perspective, this is a much more
valuable skill, as libraries come and go, but true understanding of the domain will
allow you to quickly make sense of other people's code and apply it consciously.*


### the unpack batch method
    def unpack_batch(batch: List[ptan.experience.ExperienceFirstLast]):
    states, actions, rewards, dones, last_states = [],[],[],[],[]
    for exp in batch:
        state = np.array(exp.state)
        states.append(state)
        actions.append(exp.action)
        rewards.append(exp.reward)
        dones.append(exp.last_state is None)
        if exp.last_state is None:
            lstate = state  # the result will be masked anyway
        else:
            lstate = np.array(exp.last_state)
        last_states.append(lstate)
    return np.array(states, copy=False), np.array(actions), \
           np.array(rewards, dtype=np.float32), \
           np.array(dones, dtype=np.uint8), \
           np.array(last_states, copy=False)


### calculate the loss 
    def calc_loss_dqn(batch, net, tgt_net, gamma, device="cpu"):
    states, actions, rewards, dones, next_states = \
        unpack_batch(batch)

    states_v = torch.tensor(states).to(device)
    next_states_v = torch.tensor(next_states).to(device)
    actions_v = torch.tensor(actions).to(device)
    rewards_v = torch.tensor(rewards).to(device)
    done_mask = torch.BoolTensor(dones).to(device)

    actions_v = actions_v.unsqueeze(-1)
    state_action_vals = net(states_v).gather(1, actions_v)
    state_action_vals = state_action_vals.squeeze(-1)
    with torch.no_grad():
        next_state_vals = tgt_net(next_states_v).max(1)[0]
        next_state_vals[done_mask] = 0.0

    bellman_vals = next_state_vals.detach() * gamma + rewards_v
    return nn.MSELoss()(state_action_vals, bellman_vals)

