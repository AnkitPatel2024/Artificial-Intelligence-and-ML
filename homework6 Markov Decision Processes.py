# Include your imports here, if any are used.
import math
from collections import defaultdict


student_name = "Ankita Patel"


# 1. Value Iteration
class ValueIterationAgent:
    """Implement Value Iteration Agent using Bellman Equations."""

    def __init__(self, game, discount):
        """Store game object and discount value into the agent object,
        initialize values if needed.
        """
        self.game = game
        self.discount = discount
        self.values = defaultdict(int)
        game_states = self.game.states
        for state in game_states:
            self.values[state] = 0

    def get_value(self, state):
        """Return value V*(s) correspond to state.
        State values should be stored directly for quick retrieval.
        """
        self.value = self.values[state]
        return self.value

    def get_q_value(self, state, action):
        """Return Q*(s,a) correspond to state and action.
        Q-state values should be computed using Bellman equation:
        Q*(s,a) = Σ_s' T(s,a,s') [R(s,a,s') + γ V*(s')]
        """
        q_val = 0
        prob_dict = self.game.get_transitions(state, action)
        transition_states = self.game.get_transitions(state, action)
        for s in transition_states:
            state_value = self.get_value(s)
            utility_r = self.game.get_reward(state, action, s)
            discounted_value = self.discount * state_value
            s_prob = 0
            for k, v in prob_dict.items():
                if k == s:
                    s_prob = v
            sub_qVal = s_prob*(utility_r + discounted_value)
            q_val += sub_qVal
        return q_val

    def get_best_policy(self, state):
        """Return policy π*(s) correspond to state.
        Policy should be extracted from Q-state values using policy extraction:
        π*(s) = argmax_a Q*(s,a)
        """
        q_max = -math.inf
        best_action = None
        all_actions = self.game.get_actions(state)
        for a in all_actions:
            q_val = self.get_q_value(state, a)
            if q_val > q_max:
                q_max = q_val
                best_action = a
        return best_action

    def iterate(self):
        """Run single value iteration using Bellman equation:
        V_{k+1}(s) = max_a Q*(s,a)
        Then update values: V*(s) = V_{k+1}(s)
        """
        iter_states = self.game.states
        for state in iter_states:
            a = self.get_best_policy(state)
            q_val = self.get_q_value(state, a)
            self.values[state] = q_val


# 2. Policy Iteration
class PolicyIterationAgent(ValueIterationAgent):
    """Implement Policy Iteration Agent.

    The only difference between policy iteration and value iteration is at
    their iteration method. However,if you need to implement helper function or
    override ValueIterationAgent's methods, you can add them as well.
    """

    def iterate(self):
        """Run single policy iteration.
        Fix curent policy,iterate state vals V(s) until |V_{k+1}(s)-V_k(s)| < ε
        """
        states_iter = self.game.states
        for state in states_iter:
            a = self.get_best_policy(state)
            epsilon = 1e-6
            while (True):
                q_value = self.get_q_value(state, a)
                state_value = self.get_value(state)
                if abs(q_value - state_value) < epsilon:
                    break
                self.values[state] = q_value


# 3. Bridge Crossing Analysis
def question_3():
    discount = 0.9
    noise = 0.015
    return discount, noise


# 4. Policies
def question_4a():
    discount = 0.2
    noise = 0
    living_reward = 0
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4b():
    discount = 0.1
    noise = 0.1
    living_reward = 0.1
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4c():
    discount = 0.9
    noise = 0.05
    living_reward = 0.1
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4d():
    discount = 0.7
    noise = 0.5
    living_reward = 0.1
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4e():
    discount = 0.9
    noise = 0.15
    living_reward = 10
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


# 5. Feedback
# Just an approximation is fine.
feedback_question_1 = 20

feedback_question_2 = """
None.
"""

feedback_question_3 = """
better recitation to go over what needs be done.
"""
