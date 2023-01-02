from BaseAI import BaseAI
from Grid import Grid
import sys
import random
import time
import numpy as np
    
class IntelligentAgent(BaseAI):
    def getMove(self, grid):
        self.prevTime = time.perf_counter()
        moves = [0,1,2,3]

        move = moves[0]
        max = float('-inf')
        a = max
        b = -max

        for i in moves:
            g = grid.clone()
            if g.move(i):
                val = self.expectiminimax(g,1,1.0,a,b)
                if val > max:
                    max = val
                    if max >= b:
                        return i
                    if max > a:
                        a = max
                    move = i
        return move
        

    def expectiminimax(self, grid, depth, probability, a, b):
        moves = [0,1,2,3]
        if (time.perf_counter() - self.prevTime > 0.2):
            return self.heuristic(grid)
        if depth == 0:
            return self.heuristic(grid)
        else:
            empty = len(grid.getAvailableCells())
            min = float('inf')
            for i in range(len(moves)):
                for j in range(len(moves)):
                    if grid.map[i][j] == 0:
                        sum_prob = self.probability()
                        row = list(grid.map[i])
                        utility = self.utility_func(i,j,probability,depth,empty,row,grid,a,b)
                        self.restore(i,j,grid,row,0)
                        if sum_prob != 0:
                            utility = utility / sum_prob
                        else:
                            utility = self.heuristic(grid)      
                        if utility < min:
                            min = utility
                        if (min > a) and min < b:
                            beta = min
                        else:
                            break

            return min

    def restore(self,i,j,grid,row,val):
        row[j] = val
        grid.map[i] = row

    def probability(self):
        sum_prob = 0
        tiles = ((0.9, 2), (0.1, 4))
        for p,v in tiles:
            sum_prob += p 
        return sum_prob

   
    def utility_func(self,i,j,probability,depth,empty,row,grid,a,b):
        utility = 0
        moves = [0,1,2,3]
        tiles = ((0.9, 2), (0.1, 4))
        for p,v in tiles:
            updated = p * probability
            if ((empty <= 3) or (0.9 * updated >= 0.1)):
                self.restore(i,j,grid,row,v)
                max = float('-inf')
                for d in moves:
                    g = grid.clone()
                    if g.move(d):
                        depth_new = depth - 1
                        util = self.expectiminimax(g,depth_new,updated,a,b)
                        if util > max:
                            max = util
                        if (max < b) and (max > a):
                            a = max
                        elif (max >= b):
                            break
            utility += probability * max
        return utility


    def heuristic(self, grid):
        return 0.5*(len(grid.getAvailableCells())**3)+ 0.5 * self.smoothness(grid)

    def smoothness(self, grid):
        g_1, g_2, g_3, g_4 = grid.map[0]
        g_5, g_6, g_7, g_8 = grid.map[1]
        g_9, g_10, g_11, g_12 = grid.map[2]
        g_13, g_14, g_15, g_16 = grid.map[3]

        tiles = [[g_1, g_2, g_3, g_4],[g_5, g_6, g_7, g_8],[g_9, g_10, g_11, g_12],[g_13, g_14, g_15, g_16]]
  
        values = [2,4]
        row = len(tiles)
        col = len(tiles[0])
        
        for r in range(row):
            for c in range(col):
                if tiles[r][c] == 0:
                    tiles[r][c] = random.choices(values,cum_weights=(0.9,0.1), k=1)

        smoothness = 0
        # last column
        smoothness -= abs(g_4-g_3)+abs(g_4-g_8)+abs(g_8-g_7)+abs(g_8-g_4)+abs(g_8-g_12)+abs(g_12-g_11)+abs(g_12-g_8)+abs(g_12-g_16)+abs(g_16-g_15)+abs(g_16-g_12)

        # first column
        smoothness -= abs(g_1-g_2)+abs(g_1-g_5) +abs(g_5-g_1)+abs(g_5-g_6)+abs(g_5-g_9)+abs(g_9-g_5)+abs(g_9-g_10)+abs(g_9-g_13)+abs(g_13-g_9)+abs(g_13-g_14)

        # top row
        smoothness -= abs(g_2-g_1)+abs(g_2-g_6)+abs(g_2-g_3)+abs(g_3-g_2)+abs(g_3-g_7)+abs(g_3-g_4)

        #bottom row
        smoothness -= abs(g_14-g_13)+abs(g_14-g_10)+abs(g_14-g_15)+abs(g_15-g_14)+abs(g_15-g_11)+abs(g_15-g_11)

        # second row
        smoothness -= abs(g_6-g_2)+abs(g_6-g_5)+abs(g_6-g_10)+abs(g_6-g_7)+abs(g_7-g_6)+abs(g_7-g_3)+abs(g_7-g_11)+abs(g_7-g_8)

        # third row
        smoothness -= abs(g_10-g_6)+abs(g_10-g_9)+abs(g_10-g_14)+abs(g_10-g_11)+abs(g_11-g_10)+abs(g_11-g_7)+abs(g_11-g_15)+abs(g_11-g_12)
        
        return smoothness
	    

