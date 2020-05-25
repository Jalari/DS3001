import numpy as np
from problem2 import random_walk
from problem3 import compute_S 

#-------------------------------------------------------------------------
'''
    Problem 4: Adding teleportation matrix into PageRank
    In this problem, we implement the pagerank algorithm which can solve the sink node problem with incorporating teleportation matrix.
    We will consider a random surfer model where a user has 2 options at every timestep: (option 1) randomly follow a link on the page or (option 2) randomly go to any page in the graph. 
    The probabilities are as follows:
        Randomly follow a link: alpha, for example, 0.95
        Randomly go to any page in the graph: (1 - alpha), for example, 0.05
    You could test the correctness of your code by typing `nosetests test4.py` in the terminal.
'''

#--------------------------
def compute_G(A, alpha = 0.95):
    '''
        compute the pagerank transition Matrix G from adjacency matrix A, which solves the sink node problem with incorporating teleportation matrix.
        G[j][i] represents the probability of moving from node i to node j.
        If node i is a sink node, S[j][i] = 1/n.
        Input: 
                A: adjacency matrix, a (n by n) numpy matrix of binary values. If there is a link from node i to node j, A[j][i] =1. Otherwise A[j][i]=0 if there is no link.
                alpha: a float scalar value, which is the probability of choosing option 1 (randomly follow a link on the page)
        Output: 
                G: the transition matrix, a (n by n) numpy matrix of float values.  G[j][i] represents the probability of moving from node i to node j.
    The values in each column of matrix G should sum to 1.
    '''
    #########################################
    ## INSERT YOUR CODE HERE
    n = np.shape(A)[0]
    G = alpha * compute_S(A) + (1 - alpha) * np.full((n, n), 1 / n)
    #########################################
    return G



#--------------------------
def pagerank(A, alpha = 0.95):
    ''' 
        The final PageRank algorithm, which solves the sink node problem with incorporating teleportation matrix
        Given an adjacency matrix A, compute the pagerank score of all the nodes in the network. 
        Input: 
                A: adjacency matrix, a numpy matrix of binary values. If there is a link from node i to node j, A[j][i] =1. Otherwise A[j][i]=0 if there is no link.
                alpha: a float scalar value, which is the probability of choosing option 1 (randomly follow a link on the page)
        Output: 
                x: the ranking scores, a numpy vector of float values, such as np.array([[.3], [.5], [.7]])
    '''
    
    # Initialize the score vector with all one values
    num_nodes, _ = A.shape # get the number of nodes (n)
    x_0 =  np.ones((num_nodes,1)) # create an all-one vector of shape (n by 1)

    # compute the transition matrix from adjacency matrix
    G = compute_G(A, alpha)
    # random walk
    x, n_steps = random_walk(G,x_0)
    return x


