# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        
        # go through all iterations 
        for _ in range(0, self.iterations):
            iterValues = util.Counter()
            #iterate through all available states
            for s in self.mdp.getStates():
                #if state is one of states that for now have
                #value 0 ( are terminal states )
                if self.mdp.isTerminal(s):
                    iterValues[s] = 0
                else:
                    #using formula from notes
                    #V*(s) = max of sum T(s,a,s')[R(s,a,s') + discount * V*(s')]
                    maxV = float("-inf")
                    #going through all actions for state
                    for action in self.mdp.getPossibleActions(s):
                        total = 0
                        for sNext, prob in self.mdp.getTransitionStatesAndProbs(s,action):
                            total += prob * (self.mdp.getReward(s,action,sNext) + \
                                             (self.discount * self.values[sNext]))
                        #get max sum for current state
                        maxV = max(total, maxV)
                        iterValues[s] = maxV

            self.values = iterValues
                        
    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        #using formula for Q*(s,a)
        #Q*(s,a) = sum T(s,a,s')[R(s,a,s') + discount* V*(s')]

        total = 0
        for nextState, prob in self.mdp.getTransitionStatesAndProbs(state,action):
            total += prob * (self.mdp.getReward(state,action,nextState) + (self.discount*self.values[nextState]))
        return total
            

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        #if state is terminal retun none
        if self.mdp.isTerminal(state):
            return None
        val= float("-inf")
        policy = None
        #go throuhg all actions for state and find max values of policy
        for action in self.mdp.getPossibleActions(state):
            if self.computeQValueFromValues(state,action) > val:
                val = self.computeQValueFromValues(state,action)
                policy = action

        return policy
        
        
        

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
