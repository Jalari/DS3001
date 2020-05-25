import numpy as np
from problem2 import compute_P,random_walk

#-------------------------------------------------------------------------
'''
    Problem 3: Solving sink-node problem in PageRank
    In this problem, we implement the pagerank algorithm which can solve the sink node problem.
    You could test the correctness of your code by typing `nosetests test3.py` in the terminal.
'''


#--------------------------
def compute_S(A):
    '''
        compute the transition matrix S from addjacency matrix A, which solves sink node problem by filling the all-zero columns in A.
        S[j][i] represents the probability of moving from node i to node j.
        If node i is a sink node, S[j][i] = 1/n.
        Input: 
                A: adjacency matrix, a (n by n) numpy matrix of binary values. If there is a link from node i to node j, A[j][i] =1. Otherwise A[j][i]=0 if there is no link.
        Output: 
                S: transition matrix, a (n by n) numpy matrix of float values.  S[j][i] represents the probability of moving from node i to node j.
    The values in each column of matrix S should sum to 1.
    '''
    #########################################
    ## INSERT YOUR CODE HERE

    S = np.divide(A, np.add.reduce(A), out=np.zeros_like(A), where=np.add.reduce(A) != 0)
    # S = np.asarray(S)
    # print(type(S))
    h = S.shape[0]
    # null_check = np.zeros(S.shape)
    colSum = np.add.reduce(S)

    #  because datasizes change depending of the size of the data given
    if len(colSum.shape) == 1:
        for i in range(0, h):
            if np.all(colSum[i] == 0):
                S[:, i] = 1 / h
    else:
        for i in range(0, h):
            if np.all(colSum[:,i] == 0):
                S[:, i] = 1 / h

    # S = np.divide(A, np.sum(A, axis=0), out=np.zeros_like(A), where=np.sum(A, axis=0) != 0)
    # n = A.shape[0]
    # for idx,column in enumerate(S.T):
    #
    #     # if column is zero replace all places with 1/n
    #     if int(np.sum(column)) == 0:
    #         S[:,idx] += 1/n

    #########################################
    return S



#--------------------------
def pagerank_v2(A):
    ''' 
        A simplified version of PageRank algorithm, which solves the sink node problem.
        Given an adjacency matrix A, compute the pagerank score of all the nodes in the network. 
        Input: 
                A: adjacency matrix, a numpy matrix of binary values. If there is a link from node i to node j, A[j][i] =1. Otherwise A[j][i]=0 if there is no link.
        Output: 
                x: the ranking scores, a numpy vector of float values, such as np.array([[.3], [.5], [.7]])
    '''

    # Initialize the score vector with all one values
    num_nodes, _ = A.shape 
    x_0 =  np.asmatrix(np.ones((num_nodes,1))) 

    # compute the transition matrix from adjacency matrix
    S = compute_S(A)

    # random walk
    x, n_steps = random_walk(S,x_0)

    return x

