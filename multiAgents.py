# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        #print "chosenIndex = " + chosenIndex
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        foodCount = successorGameState.getNumFood()		
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        GhostDist = finddist(newGhostStates,newPos)

        minFoodDist = 99999
        foodList = newFood.asList(True)

        for x in foodList:
            curDist = util.manhattanDistance(x, newPos)
            if curDist < minFoodDist:
                minFoodDist = curDist

        index = min(xrange(len(GhostDist)), key=GhostDist.__getitem__)

        """
        If the foodCount is zero for the next successor state we should
        go there if there is no ghost near.
        """
        if foodCount == 0 and GhostDist[index] > 1:
            return 1000

        """
        If the ghost is near, return a low value
        """
        if GhostDist[index] <= 2:
            ans = GhostDist[index]
        else:
            """
            If the action is STOP, return a very low value
            """
            if currentGameState.getPacmanPosition() == newPos:
                return 0
            """
            If this successor state has a food, return a good
            value. I'm choosing 4+2 because this can be the highest
            value one can get after this stage.
            """
            if (currentGameState.getNumFood() > foodCount):
                ans = 4 + 2
                return ans
            """
            Give a slight advantage to a action where the ghost is away
            """
            ans = 4 + GhostDist[index]/1000

        """
        We would enter this case only when the ghost is near and the
        successor has food. In that case let's give a slight advantage
        based on foodCount.
        """
        if (currentGameState.getNumFood() > foodCount) and foodCount > 0:
            ans = ans + 1.0/foodCount

        """
        Give an advantage based on nearest food available to the successor state.
        """
        if (foodCount == 0):
            ans = ans + 0.5
        else:
            ans = ans + 1.0/minFoodDist

        return ans


def finddist(GhostStates, src):
    dist = []
    for Ghost in GhostStates:
        dist.append(util.manhattanDistance(Ghost.getPosition(), src))
    return dist			
		
		
def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    
    def getMinimaxAction(self,gameState,turn,depth):     

        """ 
           This function implements the minimax algorithms
           turn = 0 :  Packman
           turn > 0 :  ghost
           This function generates the successorState for an agent and finds
           the minimum value (for ghost) and maximum value(for packman) 		   
        """		
        """
        If the maximum depth is reached returns the evaluation function 
        for the state		
        """ 
	
        if (depth == self.depth):
            return (self.evaluationFunction(gameState),None)		
        Actions = gameState.getLegalActions(turn)
        #print len(Actions),turn	,depth	
        if turn == 0:
            score = -9999999999
            minimaxAction = "pacRight"			 
        else:
            score = 999999999
            minimaxAction = "gRight" 			
        			
        currdepth = depth
          		
        if ( turn == (gameState.getNumAgents()-1) ):		
            currdepth = depth + 1		
        """
		If there are no more actions from a given state return the 
        evaluationfunction for the present state		
        """
        if(len(Actions) == 0):
            return (self.evaluationFunction(gameState),"None")  		
         		 
        for action in Actions: 		
            successorState              = gameState.generateSuccessor(turn,action)			 
            (currentScore,Nextaction)   = self.getMinimaxAction(successorState,((turn+ 1)% (gameState.getNumAgents())),currdepth) 			
            if (turn == 0) and (currentScore > score):
                score = currentScore
                minimaxAction = action
            if (turn != 0) and (currentScore < score):
                score = currentScore
                minimaxAction = action 
 				
        return (score,minimaxAction)			
        		
	
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        		
        (score,action) = self.getMinimaxAction(gameState,0,0)
        return action 		
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def getalphaBetaAction(self,gameState,turn,depth,alpha,beta):
	
        """ 
           This function implements the alpha beta pruning
           turn = 0 :  Packman
           turn > 0 :  ghost
           This function generates the successorState for an agent and finds
           the minimum value (for ghost) and maximum value(for packman)
            stops expanding further nodes once beta < alpha 		   
        """		
        """
        If the maximum depth is reached returns the evaluation function 
        for the state		
        """ 	
	
        if (depth == self.depth):
            return (self.evaluationFunction(gameState),None)		
        Actions = gameState.getLegalActions(turn)
 
        if turn == 0:
            score = -9999999999
            minimaxAction = "pacRight"			 
        else:
            score = 999999999
            minimaxAction = "gRight" 			
        			
        currdepth = depth
          		
        if ( turn == (gameState.getNumAgents()-1) ):		
            currdepth = depth + 1		

        if(len(Actions) == 0):
            return (self.evaluationFunction(gameState),"None")  		
         		 
        for action in Actions: 		
            successorState              = gameState.generateSuccessor(turn,action)			 
            (currentScore,Nextaction)   = self.getalphaBetaAction(successorState,((turn+ 1)% (gameState.getNumAgents())),currdepth,alpha,beta) 			
            if (turn == 0) and (currentScore > score):
                score = currentScore
                minimaxAction = action
                alpha = max(alpha,currentScore)   				
                if (alpha > beta):
                    break; 					
            if (turn != 0) and (currentScore < score):
                score = currentScore
                beta = min(beta,currentScore)
                minimaxAction = action   				
                if (beta < alpha):
                    break; 				
  				
        return (score,minimaxAction)         	
      	
    	
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        alpha = -99999999
        beta  =  99999999 		
        (score,action) = self.getalphaBetaAction(gameState,0,0,alpha,beta)	
        return action   		
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getExpectimaxAction(self,gameState,turn,depth):     

        """ 
           This function implements the Expectiminimax
           turn = 0 :  Packman
           turn > 0 :  ghost
           This function generates the successorState for an agent and finds
           the maximum value(for packman) and average of all successorStates 
		   for gosts
            		   
        """		
        """
        If the maximum depth is reached returns the evaluation function 
        for the state		
        """
	
        if (depth == self.depth):
            return (self.evaluationFunction(gameState),None)		
        Actions = gameState.getLegalActions(turn)
        #print len(Actions),turn	,depth	
        if turn == 0:
            score = -9999999999
            minimaxAction = "pacRight"			 
        else:
            score = 0
            minimaxAction = "gRight" 			
        			
        currdepth = depth
          		
        if ( turn == (gameState.getNumAgents()-1) ):		
            currdepth = depth + 1		

        if(len(Actions) == 0):
            return (self.evaluationFunction(gameState),"None")  		
                    		 
        for action in Actions: 		
            successorState              = gameState.generateSuccessor(turn,action)			 
            (currentScore,Nextaction)   = self.getExpectiMinimaxAction(successorState,((turn+ 1)% (gameState.getNumAgents())),currdepth) 			
            if (turn == 0) and (currentScore > score):
                score = currentScore
                minimaxAction = action
            if (turn != 0) and (currentScore != 0):
                score = score + float(currentScore)/float(len(Actions))
                minimaxAction = action 
 				
        return (score,minimaxAction)
	
	
    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        (score,action) = self.getExpectimaxAction(gameState,0,0)
        return action 
		
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

