import game
import neuralNet
import numpy as np

def run_game_with_parameters(weights, display, clock):
    numOfSteps = 2500
    appleScore = 0
    score1 = 0
    score2 = 0
    snakePos,applePos = game.startPositions()

    for _ in range(numOfSteps):
        collisionWithWallOrSelf = 0    
        isFrontBlocked, isRightBlocked, isLeftBlocked = game.blockedDirections(snakePos)
        snakeDirectionVecNormalized ,appleDirectionVecNormalized = game.directionVectors(snakePos, applePos)
        # print("snakeDirection", snakeDirectionVecNormalized, "appleDirection", appleDirectionVecNormalized)
        
        predictedDirection = np.argmax(np.array(neuralNet.forwardPropagation(np.array([isFrontBlocked,
        isRightBlocked, isLeftBlocked, snakeDirectionVecNormalized[0], snakeDirectionVecNormalized[1],
        appleDirectionVecNormalized[0], appleDirectionVecNormalized[1]]),weights)))
        
        # print(neuralNet.forwardPropagation(np.array([isFrontBlocked,
        # isRightBlocked, isLeftBlocked, snakeDirectionVecNormalized[0], snakeDirectionVecNormalized[1],
        # appleDirectionVecNormalized[0], appleDirectionVecNormalized[1]]),weights))
        # print("predictedDirection",predictedDirection)

        applePos, snakePos, appleScore = game.playGame(snakePos, applePos, appleScore, predictedDirection,display, clock)

        if game.collisionWithWall(snakePos):
                collisionWithWallOrSelf = 1

        if game.collisionWithSelf(snakePos):
                collisionWithWallOrSelf = 1 

        if collisionWithWallOrSelf == 1:
                print("colision")
                score1 = -1000
                break
        score2 += -10
    print("score1",score1)
    print("score2",score2)
    print("appleScore",appleScore)    
    return score1 + score2 + 5000*appleScore                     # return 1
