#do not modify the function names
#You are given L and M as input
#Each of your functions should return the minimum possible L value
#Or return -1 if no solution exists for the given L

#Your backtracking function implementation

import time
from copy import copy


constraintChecks = 0 

def isSafe(assignments,marker,dist):
    global constraintChecks
	
    """
	Used by Backtracking. Checks if a ruler at position marker 
    can be placed with respect to the constriants
    dist is a array with all the distances of the
    so far obtained solution
    """
    if marker in assignments.keys():
        if assignments[marker] == 1:	 
            return False		
    keys = assignments.keys()
    newdist = []
    constraintChecks = constraintChecks + 1	
    for key in keys:
        if (assignments[key]==1):
            if (abs(marker - key) in dist):
                 return False
            newdist.append(abs(marker-key))
    for d in newdist:
        dist.append(d)
    return True		
				 								
				
def BTUtil(L,M,assignments,start,dist):
    counter = M
    global constraintChecks 
	
    """
    A recursive backtrack function to check if the 
	if there is a valid assignment and calls the recurisive 
	function for the rest of the variables
	
    """
    if counter == 0 or start > L:
        if counter==0:    			 
            return True
        return False		 
    for i in range(start,L+1):
        	
        newdist = copy(dist)	
        if(isSafe(assignments,i,newdist)):
            assignments[i] = 1
            counter = counter - 1		
            x = BTUtil(L,counter,assignments,i+1,newdist)
            if  x == False:
                counter = counter + 1 
                assignments[i] = 0
            else:
                return True			
    return False			
		
        			

def BT(L, M):
    global constraintChecks
    finalkeys = []

    best = -1
    curr = L
    constraintChecks = 0
    """
    First check if there is a solution for L. If there is a solution, take
    the max length(L') in the solution and iteratively start the whole process
    with length L'-1. If there is no solution, the last obtained solution is
    the best.
    """
    while True:
        assignments = {}
        dist = []


        if BTUtil(curr, M, assignments, 0, dist):
            finalAssignments = assignments.copy()
            finalkeys = [key for key,val in finalAssignments.items() if val==1]
            best = max(finalkeys)
            curr = best -1
        else:
            break;
    print constraintChecks
    if len(finalkeys) > 0:
        print finalkeys
        return finalkeys
    else:
        print "No solution exists"
        return -1


def FCassigments(assignments,counter,marker,dist):

    """
    This is the actual Forward chain implementation. 
    First checks if the position at the ruler can be placed or not. 
  	
	for a given posiotion on the ruler it checks if it is consistent with the previous assignment.
	if true it also eliminates all other inconsistent posiitions by assigning num 2 to the assignments dictionary(domain reduction)
	 
    """
    if assignments[marker] == 2:
        return False;
    global constraintChecks		
    constraintChecks = constraintChecks + 1    
    if marker in assignments.keys():
        if assignments[marker] == 1:	 
            return False
	
    	
    keys = assignments.keys()
	
    tempdist = [] 
    for key in keys:
        if assignments[key] ==  1:
            if (marker-key) in dist:
                return False				
            tempdist.append(marker - key)
             
    assignments[marker] = 1
   	
    remaining = [key for key,val in assignments.items() if val==0 and key>marker]
    count = len(remaining)
   
    for d in tempdist:
        dist.append(d)	 
    keys = assignments.keys()    	
    for item in remaining:
        for key in keys:
            if assignments[key] == 1 and (item - key) in dist:
                count = count - 1
                assignments[item] = 2;
                break 			
	

    assignments[marker] = 0	
    return True



	
def FCUtil(L,M,assignments,start,dist):
    counter = M
    global constraintChecks

    """
	This the main forward checking function. for each unassigned variable checks if each value in its domain 
	can is consistent with the assignment given so far. 
	calls FCassigments whcih also takes care of forward chaining(the actual domain reduction)
	
    """
    if counter == 0 or start > L:	
        if counter==0:			 
            return True
        return False

	
    for i in range(start,L+1):
        ass1 = assignments.copy()
        newdist = copy(dist) 		
        if(FCassigments(ass1,counter-1,i,newdist)):
            ass1[i] = 1
            counter = counter - 1		
            x = FCUtil(L,counter,ass1,i+1,newdist)
     
            if  x == False:
                counter = counter + 1 
            else:
                for (key, value) in ass1.iteritems():
                    assignments[key] = value
                return True				
    return False	
	
#Your backtracking+Forward checking function implementation
def FC(L, M):
    global constraintChecks	
    finalkeys = []

    """
    First check if there is a solution for L. If there is a solution, take
    the max length(L') in the solution and iteratively start the whole process
    with length L'-1. If there is no solution, the last obtained solution is
    the best.
    """
    best = -1
    curr = L
    constraintChecks = 0
    while True:
        assignments = {}
        dist = []


        remaining = range(0, curr+1)
        for item in remaining:
            assignments[item] = 0

        if FCUtil(curr, M, assignments, 0, dist):
            finalAssignments = assignments.copy()
            finalkeys = [key for key,val in finalAssignments.items() if val==1]
            best = max(finalkeys)
            curr = best - 1
        else:
            break;
    print constraintChecks
    if len(finalkeys) > 0:
        print finalkeys
        return finalkeys
    else:
        print "No solution exists"
        return -1

		
def CPassigments(assignments,counter,marker,dist):

    """
    This is the actual Constraint Propagation implementation. 
    First checks if the position at the ruler can be placed or not. 
  	
	Then for a given position on the ruler it checks if it is consistent with the previous assignment.
	if true it also eliminates all other inconsistent positions by assigning num 2 to the assignments dictionary(domain reduction)
	and counts num of consitent positions. Returns false if they are less than the number of remaining markers to be placed else true
    
    	
    """

    if assignments[marker] == 2:
        return False;
    global constraintChecks		
    constraintChecks = constraintChecks + 1    
    if marker in assignments.keys():
        if assignments[marker] == 1:	 
            return False
	
    	
    keys = assignments.keys()
	
    tempdist = [] 
    for key in keys:
        if assignments[key] ==  1:
            if (marker-key) in dist:
                return False				
            tempdist.append(marker - key)
             
    assignments[marker] = 1
   	
    remaining = [key for key,val in assignments.items() if val==0 and key>marker]
    count = len(remaining)
   
    for d in tempdist:
        dist.append(d)	 
    keys = assignments.keys()    	
    for item in remaining:
        for key in keys:
            if assignments[key] == 1 and (item - key) in dist:
                count = count - 1
                assignments[item] = 2;
                break 			
	

    assignments[marker] = 0	
#    return True
    if count >= counter:
        return True	

    return False		
		
def CPUtil(L,M,assignments,start,dist):


    """
	This the main constraint propagation function. for each unassigned variable it checks if each value in its domain 
	is consistent with the assignment given so far. 
	calls CPassigments  which also takes care of Constarint Propagation
	
    """

    counter = M
    global constraintChecks
    if counter == 0 or start > L:	
        if counter==0:			 
            return True
        return False

	
    for i in range(start,L+1):
        ass1 = assignments.copy()
        newdist = copy(dist) 		
        if(CPassigments(ass1,counter-1,i,newdist)):
            ass1[i] = 1
            counter = counter - 1		
            x = CPUtil(L,counter,ass1,i+1,newdist)
     
            if  x == False:
                counter = counter + 1 
                #assignments[i] = 0
            else:
                for (key, value) in ass1.iteritems():
                    assignments[key] = value
                return True				
    return False		
		
#Bonus: backtracking + constraint propagation
def CP(L, M):
    global constraintChecks	
    finalkeys = []

    """
    First check if there is a solution for L. If there is a solution, take
    the max length(L') in the solution and iteratively start the whole process
    with length L'-1. If there is no solution, the last obtained solution is
    the best.
    """
    best = -1
    curr = L
    constraintChecks = 0
    while True:
        assignments = {}
        dist = []
        #constraintChecks = 0

        remaining = range(0, curr+1)
        for item in remaining:
            assignments[item] = 0

        if CPUtil(curr, M, assignments, 0, dist):
            finalAssignments = assignments.copy()
            finalkeys = [key for key,val in finalAssignments.items() if val==1]
            best = max(finalkeys)
            curr = best - 1
        else:
            break;
    print constraintChecks 
    if len(finalkeys) > 0:
        print finalkeys
        return finalkeys
    else:
        print "No solution exists"
        return -1
BT(34,8)
FC(34,8)
CP(34,8)
