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

import util


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


def depthFirstSearch(problem):
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
   
    # Initialize the explored set to be empty
    Ex = set()

    # Initialize the frontier using the initial state of problem.
    st = util.Stack()
    st.push((problem.getStartState(),[]))
    
    while(True):

        if st.isEmpty():
            return False
            
        # node ← POP(frontier)
        node, path = st.pop()
        
        Ex.add(node)
       
        if problem.isGoalState(node):
            return path

        succ = problem.getSuccessors(node)

        for x in succ:
            if (x[0] not in Ex):
                newPath = path + [x[1]]
                st.push((x[0],newPath))     # this is a tuple changes


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    queue = util.Queue()
    start_state = problem.getStartState()
    actions = []
    visited = set()
    parents = {}
    queue.push(start_state)
    visited.add(start_state)

    while queue:
        current_state = queue.pop()

        if problem.isGoalState(current_state):
            while current_state != start_state:
                next_state, action = parents[current_state]
                current_state = next_state
                actions.append(action)

            return actions[::-1]

        successors = problem.getSuccessors(current_state)

        for successor in successors:
            next_state, action, _ = successor

            if next_state not in visited:
                queue.push(next_state)
                visited.add(next_state)
                parents[next_state] = (current_state, action)


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    priority_queue = util.PriorityQueue()
    start_state = problem.getStartState()
    actions = []
    distances = {start_state: 0}
    parents = {}
    priority_queue.push(start_state, 0)

    while priority_queue:
        current_state = priority_queue.pop()

        if problem.isGoalState(current_state):
            while current_state != start_state:
                next_state, action = parents[current_state]
                current_state = next_state
                actions.append(action)

            return actions[::-1]

        successors = problem.getSuccessors(current_state)

        for successor in successors:
            next_state, action, cost = successor

            if next_state not in distances:
                distances[next_state] = distances[current_state] + cost
                priority_queue.push(next_state, distances[next_state])
                parents[next_state] = (current_state, action)

            elif distances[next_state] > distances[current_state] + cost:
                priority_queue.update(next_state, distances[next_state] + cost)
                parents[next_state] = (current_state, action)
                distances[next_state] = distances[current_state] + cost


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    priority_queue = util.PriorityQueue()
    start_state = problem.getStartState()
    actions = []
    distances = {start_state: 0}
    parents = {}
    priority_queue.push(start_state, 0)

    while priority_queue:
        current_state = priority_queue.pop()

        if problem.isGoalState(current_state):
            while current_state != start_state:
                next_state, action = parents[current_state]
                current_state = next_state
                actions.append(action)

            return actions[::-1]

        successors = problem.getSuccessors(current_state)

        for successor in successors:
            next_state, action, cost = successor
            
            if next_state not in distances:
                distances[next_state] = distances[current_state] + cost
                priority_queue.update(next_state, distances[next_state] + heuristic(next_state, problem))
                parents[next_state] = (current_state, action)

            elif distances[next_state] > distances[current_state] + cost:
                distances[next_state] = distances[current_state] + cost
                priority_queue.update(next_state, distances[next_state] + heuristic(next_state, problem))
                parents[next_state] = (current_state, action)

            # if next_state not in distances:
            #     distances[next_state] = distances[current_state] + cost
            #     priority_queue.push(next_state, distances[next_state] + heuristic(next_state, problem))
            #     parents[next_state] = (current_state, action)
            # 
            # elif distances[next_state] > distances[current_state] + cost:
            #     priority_queue.update(next_state, distances[next_state] + cost)
            #     parents[next_state] = (current_state, action)
            #     distances[next_state] = distances[current_state] + cost


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
