import numpy as np
from Setup import Transportation

class VogelsApproximationMethod:

    def __init__(self, trans):

        self.trans = trans
        self.table = trans.table.copy()
        self.alloc = []

    def allocation(self, x, y):
        
        mins = min([self.table[x, -1], self.table[-1, y]])
        self.alloc.append([self.table[x, 0], self.table[0, y], mins])
        
        if self.table[x, -1] < self.table[-1, y]:
            #delete row and supply x then change value of demand y
            self.table = np.delete(self.table, x, 0)
            self.table[-1, y] -= mins
            
        elif self.table[x, -1] > self.table[-1, y]:
            #delete column and demand y then change value of supply x
            self.table = np.delete(self.table, y, 1)
            self.table[x, -1] -= mins
            
        else:
            #delete row and supply x, column and demand y
            self.table = np.delete(self.table, x, 0)
            self.table = np.delete(self.table, y, 1)

    def penalty(self, cost):
        #return gaps between two lowest cost in row/column
        gaps = np.zeros(cost.shape[0])
        for i, c in enumerate(cost):
            try:
                x, y = sorted(c)[:2]
            except ValueError:
                x, y = c[0], 0
            gaps[i] = abs(x - y)
        return gaps

    def solve(self, show_iter=False):

        while self.table.shape != (2, 2):

            cost = self.table[1:-1, 1:-1]
            supply = self.table[1:-1, -1]
            demand = self.table[-1, 1:-1]
            n = cost.shape[0]

            #compute row and column penalties
            row_penalty = self.penalty(cost)
            col_penalty = self.penalty(cost.T)

            #check if maximum penalties value has a tie
            P = np.append(row_penalty, col_penalty)

            max_alloc = -np.inf
            for i in np.where(P == max(P))[0]:

                if i - n < 0:
                    r = i
                    L = cost[r]
                else:
                    c = i - n
                    L = cost[:, c]

                #check if minimum cost has a tie
                #in maximum row/columns penalties
                for j in np.where(L == min(L))[0]:
                    if i - n < 0:
                        c = j
                    else:
                        r = j

                    alloc = min([supply[r], demand[c]])
                    if alloc > max_alloc:
                        max_alloc = alloc
                        x, y = r, c

            #allocated row x to column y or vice versa  
            self.allocation(x + 1, y + 1)

            #print table
            if show_iter:
                self.trans.print_frame(self.table)
            
        return np.array(self.alloc, dtype=object)


if __name__ == "__main__":
    
    #example 1 balance problem
    cost = np.array([[19, 30, 50, 10],
                    [70, 30, 40, 60],
                    [40,  8, 70, 20]])
    supply = np.array([7, 9, 18])
    demand = np.array([5, 8, 7, 14])

    #example 2 unbalance problem
    cost = np.array([[ 4,  8,  8],
                    [16, 24, 16],
                    [ 8, 16, 24]])
    supply = np.array([76, 82, 77])
    demand = np.array([72, 102, 41])

    #initialize transportation problem
    trans = Transportation(cost, supply, demand)

    #setup transportation table.
    #minimize=True for minimization problem, change to False for maximization, default=True.
    #ignore this if problem is minimization and already balance
    trans.setup_table(minimize=True)

    #initialize Vogel's method with table that has been prepared before.
    VAM = VogelsApproximationMethod(trans)

    #solve problem and return allocation lists which consist n of (Ri, Cj, v)
    #Ri and Cj is table index where cost is allocated and v it's allocated value.
    #(R0, C1, 3) means 3 cost is allocated at Row 0 and Column 1.
    #show_iter=True will showing table changes per iteration, default=False.
    allocation = VAM.solve(show_iter=False)

    #print out allocation table in the form of pandas DataFrame.
    #(doesn't work well if problem has large dimension).
    trans.print_table(allocation)

#Result from example problem above
'''
example 1 balance problem
           C0    C1     C2      C3 Supply
R0      19(5)    30     50   10(2)      7
R1         70    30  40(7)   60(2)      9
R2         40  8(8)     70  20(10)     18
Demand      5     8      7      14     34

TOTAL COST: 779

example 2 unbalance problem
           C0      C1      C2  Dummy Supply
R0          4   8(76)       8      0     76
R1         16  24(21)  16(41)  0(20)     82
R2      8(72)   16(5)      24      0     77
Demand     72     102      41     20    235

TOTAL COST: 2424
'''
