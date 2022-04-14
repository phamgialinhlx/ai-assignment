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
    return  [s, s, w, s, w, w, s, w]

def dFS(problem, presentState, path, explored):
    # print "PRESENTSTATE", presentState
    explored.add(presentState)
    if (problem.isGoalState(presentState)): 
        return True
    list = [successor for successor in problem.getSuccessors(presentState)]
    for successor in list:
        if not successor[0] in explored:
            path.append(successor[1])
            if not dFS(problem, successor[0], path, explored):
                path.pop()
            else:
                return True
    return False

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    """
    path = []
    explored = set()
    dFS(problem, problem.getStartState(), path, explored)
    # print path
    return path
    # return [direction[paths] for paths in path]
    # util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
   
    from util import Queue
    successorQueue = Queue()
    presentState = problem.getStartState()
    explored = set()
    explored.add(presentState)
    tracepath = {}
    goalSuccessor = None
    
    list = [successor for successor in problem.getSuccessors(presentState)]
    for successor in list:
        successorQueue.push(successor)
    # print [state[0] for state in successorQueue.list]
    while (not problem.isGoalState(presentState)):
        presentSuccessor = successorQueue.pop()
        presentState = presentSuccessor[0]
        # if not presentState in [state[0] for state in successorQueue.list]:
        if (not presentState in explored):        
            explored.add(presentState)
            
            if (problem.isGoalState(presentState)):
                goalSuccessor = presentSuccessor
                break
            list = [successor for successor in problem.getSuccessors(presentState)]
            for successor in list:
                if not successor[0] in explored:
                    tracepath[successor] = presentSuccessor
                    successorQueue.push(successor)
                    # if not successor in tracepath.keys():
        
    path = []
    while goalSuccessor in tracepath.keys():
        path.append(goalSuccessor[1])
        goalSuccessor = tracepath[goalSuccessor]
    path.append(goalSuccessor[1])
    path.reverse()
    return path

    # util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    from util import PriorityQueue
    pq = PriorityQueue()
    presentState = problem.getStartState()
    explored = set()
    explored.add(presentState)
    tracepath = {}
    cost = {}
    goalSuccessor = None

    list = [successor for successor in problem.getSuccessors(presentState)]
    for successor in list:
        pq.push(successor, successor[2])
        cost[successor] = successor[2]
    while (not problem.isGoalState(presentState)):
        presentSuccessor = pq.pop()
        presentState = presentSuccessor[0]
        if (not presentState in explored):
            explored.add(presentState)

            if (problem.isGoalState(presentState)):
                goalSuccessor = presentSuccessor
                break
            list = [successor for successor in problem.getSuccessors(presentState)]
            for successor in list:
                if not successor[0] in explored:
                    tracepath[successor] = presentSuccessor
                    cost[successor] = successor[2] + cost[presentSuccessor]
                    pq.push(successor, cost[successor])
    
    path = []
    while goalSuccessor in tracepath.keys():
        path.append(goalSuccessor[1])
        goalSuccessor = tracepath[goalSuccessor]
    path.append(goalSuccessor[1])
    path.reverse()
    return path

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "- YOUR CODE HERE ***"
    from util import PriorityQueue
    pq = PriorityQueue()
    presentState = problem.getStartState()
    explored = set()
    explored.add(presentState)
    tracepath = {}
    cost = {}
    goalSuccessor = None
    list = [successor for successor in problem.getSuccessors(presentState)]
    for successor in list:
        pq.push(successor, heuristic(successor[0], problem) + successor[2]) 
        cost[successor] = successor[2]
    while (not problem.isGoalState(presentState)):
        presentSuccessor = pq.pop()
        presentState = presentSuccessor[0]
        if (not presentState in explored):
            explored.add(presentState)
            if (problem.isGoalState(presentState)):
                goalSuccessor = presentSuccessor
                break
            list = [successor for successor in problem.getSuccessors(presentState)]
            for successor in list:
                if (not successor[0] in explored):
                    tracepath[successor] = presentSuccessor
                    cost[successor] = successor[2] + cost[presentSuccessor]
                    pq.push(successor, heuristic(successor[0], problem) + cost[successor])
    
    path = []
    while goalSuccessor in tracepath.keys():
        path.append(goalSuccessor[1])
        goalSuccessor = tracepath[goalSuccessor]
    path.append(goalSuccessor[1])
    path.reverse()
    # print(path)
    return path


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
