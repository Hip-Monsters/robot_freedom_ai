#!/usr/bin/python
# -*- coding: utf-8 -*-
  
"""   
""" 
import numpy as np 
 

class GDS():

    def __init__(self, x, y, prior_weights, learning_rate, 
                 m=1, max_iterations=100, verbose=False):
        """
        theta  = self.prior_weights
        
        """
        self.x = np.array(x)
        self.y = np.array(y)
        self.prior_weights = prior_weights
        self.learning_rate = learning_rate
        self.m  = m
        self.max_iterations = max_iterations
        self._weights = []
        self.verbose = verbose 

    def weights(self):
        """
        """  
        return self._weights.tolist()
 
    def train(self):
        """
        """
        xTrans = self.x.transpose()
        theta  = self.prior_weights 
      
        for i in range(0, self.max_iterations):
            hypothesis = np.dot(self.x, theta)
            loss = hypothesis - self.y 
            cost = np.sum(loss ** 2) / (2 * self.m)
            if self.verbose:
                print("Iteration %d | Cost: %f" % (i, cost))
            
            gradient = np.dot(xTrans, loss) / self.m 
            theta =  theta - self.learning_rate * gradient

        if self.verbose: 
            print(self._weights) 

        self._weights =   theta
 