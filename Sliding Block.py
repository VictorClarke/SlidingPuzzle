__author__ = 'Victor'

import copy
import time
import random
from collections import deque
from heapq import *



# A state in a sliding-block puzzle environment.
class SlidingBlockState(object):
    # Set up a grid with all the numbers in order.    0 1 2
    # For example, if size is 3, the grid should be:  3 4 5
    # The 0 will represent the empty space.           6 7 8
    def __init__(self, size):
        self.grid = list()
        n = 0
        for r in range(size):
            row = list()
            self.grid.append(row)  # grid was initially a single empty list, now it's an empty 2D list for each row
            for c in range(size):
                row.append(n)
                n += 1

    # Print the grid.
    def display(self):
        for row in self.grid:
            for number in row:
                print(number, end=" ")
            print()
        print()

    # Return a list of moves available in this state.
    # You'll have to decide how to represent moves.
    def moves(self):
        moves = list()
        for r in range(len(self.grid)):
            for c in range(len(self.grid)):
                if self.grid[r][c] == 0:
                    if r != 0:
                        moves.append(("down", self.grid[r - 1][c]))
                    if r != len(self.grid) - 1:
                        moves.append(("up", self.grid[r + 1][c]))
                    if c != 0:
                        moves.append(("right", self.grid[r][c - 1]))
                    if c != len(self.grid) - 1:
                        moves.append(("left", self.grid[r][c + 1]))
        return moves

    # Return another state like this one but with one move made.
    # Make sure there isn't any aliasing between the two states.
    def neighbor(self, move):
        neighbor = copy.deepcopy(self)  # takes copy of object without aliasing
        (dir, number) = move
        for r in range(len(self.grid)):
            for c in range(len(self.grid)):
                if neighbor.grid[r][c] == number:
                    if dir == "up":
                        neighbor.grid[r - 1][c] = number
                        neighbor.grid[r][c] = 0
                        return neighbor
                    if dir == "down":
                        neighbor.grid[r + 1][c] = number
                        neighbor.grid[r][c] = 0
                        return neighbor
                    if dir == "left":
                        neighbor.grid[r][c - 1] = number
                        neighbor.grid[r][c] = 0
                        return neighbor
                    if dir == "right":
                        neighbor.grid[r][c + 1] = number
                        neighbor.grid[r][c] = 0
                        return neighbor
        return neighbor

    def wins(self):
        initial_string = ''
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                initial_string += str(self.grid[i][j])
        return initial_string == '012345678'

    def distance(self, other):
        sum = 0
        for i in range(other.size):
            for j in range(other.size):
                num = other.grid[i][j]
                if num != 0:
                    goalI = num // other.size
                    goalJ = num - (other.size*goalI)
                    sum += (abs(goalJ - j) + abs(goalI - i))
        return sum

    # These methods make equivalent states be recognized as == (similiar to say ".equals()")
    def __hash__(self):  #hash method; whenever you do equals and not-equals you have to include a hash method
        initial_string = ''
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                initial_string += str(self.grid[i][j])
        return hash(initial_string)

    def __eq__(self, other):  #(similiar to say ".equals()")
        return self.grid == other.grid

    def __ne__(self, other):  #like saying is opposite
        return not self == other  #But you cant say != bc it would be circular

    def __lt__(self, other):
        return self.grid < other.grid


# An agent that uses breadth-first search to escape the maze.
class SimpleSearchAgent(object):
    #psuedo code from notebook implemented
    def plan(self, start):

        #create an empty dictionary
        plan = dict()
        plan[start] = list()
        frontier = deque()
        frontier.append(state)  #put the state on the end of the queue as initial state
        while len(frontier) > 0:
            parent = frontier.popleft()  #parent is going to be a MazeState object
            for move in parent.moves():
                print(parent.moves())
                child = parent.neighbor(move)
                if child not in plan:
                    frontier.append(child)
                    plan[child] = plan[parent] + [
                        move]  #python adds lists together into one list and creates a copy automatically
                    if child.wins():
                        return plan[child]


#An agent that uses A* search to escape the maze
class HeuristicSearchAgent(object):
    def plan(self, start, goal):
        # Keep a map of states -> move sequences that reach them
        plan = dict()
        plan[start] = list()

        #For a regular queue we used a deque; for priority queue we're using heapq
        # Use list as a heap for a priority queue
        frontier = list()
        #heappush(frontier, (priority, item))
        heappush(frontier, (start.distance(goal), start))
        #finished set; keep track of finished states with a set
        finished = set()  #similar to a hashtable

        # Take states off the frontier
        while len(frontier) > 0:
            (priority, parent) = heappop(frontier)  #this takes the parent of the frontier
            finished.add(parent)
            #now check if the parent is the goal; stop if we finished the goal state
            if parent == goal:
                return plan[goal]
            # Look at all the neighbors (children)
            for move in parent.moves():
                child = parent.neighbor(move)
                # Only consider ones we haven't finished
                if child not in finished:
                    # Form a new plan or update to a better one
                    if child not in plan or len(plan[parent]) + 1 < len(plan[child]):
                        plan[child] = plan[parent] + [move]
                        heappush(frontier, (len(plan[child]) + child.distance(goal), child))


# An agent that makes random moves.
class RandomAgent(object):
    def move(self, state1):
        return random.choice(state1.moves())

# Create a puzzle and watch a few random moves.
if __name__ == '__main__':

    state = SlidingBlockState(3)
    state.display()
    state.wins()

    agent = RandomAgent()

    for turn in range(7):
        move = agent.move(state)
        state = state.neighbor(move)

        time.sleep(1)
        state.display()

    print("start")

    agent2 = SimpleSearchAgent()
    plan = agent2.plan(state)

    for move in plan:
        state = state.neighbor(move)

        time.sleep(1)
        state.display()
