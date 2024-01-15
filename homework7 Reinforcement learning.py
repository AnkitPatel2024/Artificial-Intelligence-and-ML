import random
import math
from collections import defaultdict

student_name = "Ankita Patel."


# 1. Q-Learning
class QLearningAgent:
    """Implement Q Reinforcement Learning Agent using Q-table."""

    def __init__(self, game, discount, learning_rate, explore_prob):
        """Store any needed parameters into the agent object.
        Initialize Q-table.
        """
        self.game = game
        self.discount = discount
        self.learning_rate = learning_rate
        self.explore_prob = explore_prob
        self.Qvalues = defaultdict(float)
        self.Svalues = defaultdict(float)

    def get_q_value(self, state, action):
        """Retrieve Q-value from Q-table.
        For an never seen (s,a) pair, the Q-value is by default 0.
        """
        q_val = self.Qvalues[(state, action)]
        return q_val

    def get_value(self, state):
        """Compute state value from Q-values using Bellman Equation.
        V(s) = max_a Q(s,a)
        """
        avail_actions = self.game.get_actions(state)
        value = 0.0
        if len(avail_actions) != 0:
            first_a = list(avail_actions)[0]
            value = self.get_q_value(state, first_a)
        for a in avail_actions:
            q_val = self.get_q_value(state, a)
            if q_val >= value:
                value = q_val
                self.Svalues[state] = value
        return value

    def get_best_policy(self, state):
        """Compute the best action to take
        in the state using Policy Extraction.
        π(s) = argmax_a Q(s,a)

        If there are ties, return a random one for better performance.
        Hint: use random.choice().
        """
        all_actions = self.game.get_actions(state)
        best_action = []
        q_max = -math.inf
        for a in all_actions:
            q_val = self.get_q_value(state, a)
            if q_val == q_max:
                if a not in best_action:
                    best_action.append(a)
            if q_val > q_max:
                q_max = q_val
                best_action = [a]
        return random.choice(best_action)

    def update(self, state, action, next_state, reward):
        """Update Q-values using running average.
        Q(s,a) = (1 - α) Q(s,a) + α (R + γ V(s'))
        Where α is the learning rate, and γ is the discount.

        Note: You should not call this function in your code.
        """
        q_val = self.get_q_value(state, action)
        alpha = self.learning_rate
        dis_val = self.discount * self.get_value(next_state)
        q_val = ((1 - alpha) * q_val) + alpha * (reward + dis_val)
        self.Qvalues[(state, action)] = q_val
        return q_val

    # 2. Epsilon Greedy
    def get_action(self, state):
        """Compute the action to take for the agent, incorporating exploration.
        That is, with probability ε, act randomly.
        Otherwise, act according to the best policy.

        Hint: use random.random() < ε to check if exploration is needed.
        """
        avail_actions = self.game.get_actions(state)
        action_chosen = None
        eps_val = self.explore_prob
        if random.random() < eps_val:
            action_chosen = random.choice(list(avail_actions))
        else:
            action_chosen = self.get_best_policy(state)
        return action_chosen


# 3. Bridge Crossing Revisited
def question3():
    epsilon = ...
    learning_rate = ...
    return 'NOT POSSIBLE'


# 5. Approximate Q-Learning
class ApproximateQAgent(QLearningAgent):
    """Implement Approximate Q Learning Agent using weights."""

    def __init__(self, *args, extractor):
        """Initialize parameters and store the feature extractor.
        Initialize weights table."""

        super().__init__(*args)
        self.extractor = extractor
        self.weights_dict = defaultdict(float)

    def get_weight(self, feature):
        """Get weight of a feature.
        Never seen feature should have a weight of 0.
        """
        f_weight = 0.0
        f_weight = self.weights_dict[feature]
        return f_weight

    def get_q_value(self, state, action):
        """Compute Q value based on the dot product
        of feature components and weights.
        Q(s,a) = w_1 * f_1(s,a) + w_2 * f_2(s,a) + ... + w_n * f_n(s,a)
        """
        q_val = 0.0
        for f, fv in self.extractor(state, action).items():
            q_val += fv * self.get_weight(f)
        return q_val

    def update(self, state, action, next_state, reward):
        """Update weights using least-squares approximation.
        Δ = R + γ V(s') - Q(s,a)
        Then update weights: w_i = w_i + α * Δ * f_i(s, a)
        """
        disc_val = self.discount * self.get_value(next_state)
        delta = reward + disc_val - self.get_q_value(state, action)
        for fe, v in self.extractor(state, action).items():
            self.weights_dict[fe] = self.get_weight(fe) + \
                                    (self.learning_rate * delta * v)


# 6. Feedback
# Just an approximation is fine.
feedback_question_1 = 16

feedback_question_2 = """
Reading matlab code that did not come out well.
"""

feedback_question_3 = """
Human readable version of instructions
"""
