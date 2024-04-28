# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""


from util import PriorityQueue, Queue, Stack


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions

    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    state = problem.getStartState()
    actions = []

    # Check if start state is goal state then return empty list of actions
    if problem.isGoalState(state):
        return actions

    explored = set()
    # Use stack as queuing strategy to get states and actions from frontier
    frontier = Stack()
    frontier.push((state, actions))
    while not frontier.isEmpty():
        # Get last state and associated actions from queue
        curr_state, curr_actions = frontier.pop()

        if problem.isGoalState(curr_state):
            return curr_actions

        if curr_state not in explored:
            # Add current state to explored set to avoid expanding again (graph search)
            explored.add(curr_state)

            # Expand current state and add successors to queue
            for successor in problem.getSuccessors(curr_state):
                frontier.push((successor[0], curr_actions + [successor[1]]))

    # Return empty list of actions if no solution was found
    return []


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    state = problem.getStartState()
    actions = []

    if problem.isGoalState(state):
        return actions

    explored = set()
    frontier = Queue()  # only difference to DFS
    frontier.push((state, actions))
    while not frontier.isEmpty():
        curr_state, curr_actions = frontier.pop()

        if problem.isGoalState(curr_state):
            return curr_actions

        if curr_state not in explored:
            explored.add(curr_state)

            for successor in problem.getSuccessors(curr_state):
                frontier.push((successor[0], curr_actions + [successor[1]]))

    return []


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    state = problem.getStartState()
    actions = []

    if problem.isGoalState(state):
        return actions

    explored = set()
    frontier = PriorityQueue()
    frontier.push((state, actions), 0)
    while not frontier.isEmpty():
        curr_state, curr_actions = frontier.pop()

        if problem.isGoalState(curr_state):
            return curr_actions

        if curr_state not in explored:
            explored.add(curr_state)

            for successor, action, cost in problem.getSuccessors(curr_state):
                # Check if successor already in frontier and if cost can be updated
                # frontier.update does nothing if new cost is more expensive
                frontier.update(
                    (successor, curr_actions + [action]),
                    problem.getCostOfActions(curr_actions) + cost,
                )

    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    state = problem.getStartState()
    actions = []

    if problem.isGoalState(state):
        return actions

    explored = set()
    frontier = PriorityQueue()
    frontier.push((state, actions), 0)
    while not frontier.isEmpty():
        curr_state, curr_actions = frontier.pop()

        if problem.isGoalState(curr_state):
            return curr_actions

        if curr_state not in explored:
            explored.add(curr_state)

            for successor, action, cost in problem.getSuccessors(curr_state):
                # Check if successor already in frontier and if cost can be updated
                # frontier.update does nothing if new cost is more expensive
                frontier.update(
                    (successor, curr_actions + [action]),
                    problem.getCostOfActions(curr_actions)
                    + cost
                    + heuristic(successor, problem),  # only difference to UCS
                )

    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
