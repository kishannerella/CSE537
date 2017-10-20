#do not modify the function names
#You are given L and M as input
#Each of your functions should return the minimum possible L value
#Or return -1 if no solution exists for the given L

#Your backtracking function implementation

import time
from copy import copy


constraintChecks = 0 

def isSafe(assignments,marker,dist):

    if marker in assignments.keys():
        if assignments[marker] == 1:	 
            return False
    global constraintChecks
    constraintChecks = constraintChecks + 1			
    keys = assignments.keys()
    newdist = []
    
    for key in keys:
        if (assignments[key]==1):
            if (abs(marker - key) in dist):
                 return False
            newdist.append(abs(marker-key))
    for d in newdist:
        dist.append(d)
    return True		
	
def isSafefinal(assignments):
    keys = assignments.keys()
    	
    #print keys	
 
    dist = [] 
    for i in range(0,len(keys)-1):
        for j in range(i+1,len(keys)):
            if assignments[keys[i]] ==  1 and assignments[keys[j]] == 1:
                if (keys[j] - keys[i]) in dist:
                    return False
                dist.append(keys[j] - keys[i])
    dist = sorted(dist)

    return True				
   				

def print_ans(assignments):
    keys = assignments.keys()
    ans = []	 
    for key in keys:
        if(assignments[key]==1):
            ans.append(key)
    #print ans			
    #print "\n"			
				
				
def BTUtil(L,M,assignments,start,dist):
    counter = M
  
    if counter == 0 or start > L:
        if counter==0:
            print_ans(assignments)
            #print constraintChecks    			 
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

    """
    First check if there is a solution for L. If there is a solution, take
    the max length(L') in the solution and iteratively start the whole process
    with length L'-1. If there is no solution, the last obtained solution is
    the best.
    """
    while True:
        assignments = {}
        dist = []
        constraintChecks = 0

        if BTUtil(curr, M, assignments, 0, dist):
            finalAssignments = assignments.copy()
            finalkeys = [key for key,val in finalAssignments.items() if val==1]
            best = max(finalkeys)
            curr = best -1
        else:
            break;

    if len(finalkeys) > 0:
        print finalkeys
        return finalkeys
    else:
        print "No solution exists"
        return -1


def FCassigmnets(assignments,counter,marker,dist):
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
    	
    for item in remaining:
        for key in keys:
            if assignments[key] == 1 and (item - key) in dist:
                count = count - 1
                assignments[item] = 2;
                break 			
	

    assignments[marker] = 0	

    if count >= counter:
        return True	

    return False	



	
def FCUtil(L,M,assignments,start,dist):
    counter = M
    global constraintChecks
    if counter == 0 or start > L:
        #print assignments	
        if counter==0:
            print_ans(assignments) 
            #print constraintChecks  			 
            return True
        return False

	
    for i in range(start,L+1):
        ass1 = assignments.copy()
        newdist = copy(dist) 		
        if(FCassigmnets(ass1,counter-1,i,newdist)):
            ass1[i] = 1
            counter = counter - 1		
            x = FCUtil(L,counter,ass1,i+1,newdist)
     
            if  x == False:
                counter = counter + 1 
                #assignments[i] = 0
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

    while True:
        assignments = {}
        dist = []
        constraintChecks = 0

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

    if len(finalkeys) > 0:
        print finalkeys
        return finalkeys
    else:
        print "No solution exists"
        return -1

#Bonus: backtracking + constraint propagation
def CP(L, M):
    "*** YOUR CODE HERE ***"
    return -1

	
#BT(8,4)
#BT(120,7)
print time.time()
BT(120, 7)
print time.time()
BT(150, 8)
print time.time()
FC(150, 9)
print time.time()
BT(0, 1)
BT(1, 2)
FC(0, 1)
FC(1, 2)
"""
BT(10, 5)
BT(11, 5)
BT(12, 5)
BT(13, 5)
BT(14, 5)
BT(15, 5)
BT(153, 5)
"""
"""	
print time.time()
BT(8,4)
BT(17,6)
BT(25,7)
BT(55,10)
print time.time() 
FC(7,4)
FC(17,6)
FC(25,7)
FC(55,10)
print time.time() 
"""