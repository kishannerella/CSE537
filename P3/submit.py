#do not modify the function names
#You are given L and M as input
#Each of your functions should return the minimum possible L value
#Or return -1 if no solution exists for the given L

#Your backtracking function implementation

import time
def isSafe(assignments,marker):
    assignments[marker] = 1	
    keys = assignments.keys()
 	
    dist = [] 
    for i in range(0,len(keys)-1):
        for j in range(i+1,len(keys)):
            if assignments[i] ==  1 and assignments[j] == 1:
                if (j-i) in dist:
                    assignments[marker] = 0					
                    return False				
                dist.append(j - i)
    assignments[marker] = 0				
    return True				
   				
def isSafefinal(assignments):
    keys = assignments.keys()
 	
    dist = [] 
    for i in range(0,len(keys)-1):
        for j in range(i+1,len(keys)):
            if assignments[i] ==  1 and assignments[j] == 1:
                if (keys[j] - keys[i]) in dist:
                    return False
                dist.append(keys[j] - keys[i])
    #print sorted(dist)				
				
    return True				
   				

def print_ans(assignments):
    keys = assignments.keys()
    ans = []	 
    for key in keys:
        if(assignments[key]==1):
            ans.append(key)
    print ans			
    print "\n"			
				
				
def BTUtil(L,M,assignments,start):
    counter = M
  
    if counter == 0:
        #print assignments	
        if isSafefinal(assignments):
             print_ans(assignments) 		
             return False
        return False		 
    for i in range(start,L+1):		
        if(isSafe(assignments,i)):
            assignments[i] = 1
            counter = counter - 1		
            x = BTUtil(L,counter,assignments,i+1)

            if  x == False:
                counter = counter + 1 
                assignments[i] = 0
            else:
                return True			
    return False			
		
    #print assignments       		
        			

def BT(L, M):
    "*** YOUR CODE HERE ***"
	
    counter = M
    assignments = {}
    return BTUtil(L,M,assignments,0)
    return -1


def FCassigmnets(assignments,counter,marker):
    assignments[marker] = 1	
    keys = assignments.keys()
    #print assignments	 	
    dist = [] 
    for i in range(0,len(keys)-1):
        for j in range(i+1,len(keys)):
            if assignments[i] ==  1 and assignments[j] == 1:
                if (j-i) in dist:
                    assignments[marker] = 0					
                    return False				
                dist.append(j - i)
             

   	
    remaining = [key for key,val in assignments.items() if val==0 and key>marker]
    count = len(remaining)

    	
    for item in remaining:
        for key in keys:
            if assignments[key] == 1 and (item - key) in dist:
                count = count - 1
                break				 			
	

    assignments[marker] = 0	
    if count >= counter:
        return True	

    return False	



	
def FCUtil(L,M,assignments,start):
    counter = M
  
    if counter == 0:
        #print assignments	
        if isSafefinal(assignments):
             print_ans(assignments) 		
             return False
        return False		 
    for i in range(start,L+1):		
        if(FCassigmnets(assignments,counter-1,i)):
            assignments[i] = 1
            counter = counter - 1		
            x = FCUtil(L,counter,assignments,i+1)
     
            if  x == False:
                counter = counter + 1 
                assignments[i] = 0
            else:
                return True			
    return False	
	
#Your backtracking+Forward checking function implementation
def FC(L, M):
    "*** YOUR CODE HERE ***"
	
    counter = M
    assignments = {}
    remaining =  range(0,L+1)
	
    for item in remaining:
         assignments[item] = 0	
    #print remaining
    return FCUtil(L,M,assignments,0)     	
    return -1

#Bonus: backtracking + constraint propagation
def CP(L, M):
    "*** YOUR CODE HERE ***"
    return -1

	
print time.time()
BT(34,8)
print time.time() 

FC(34,8)
print time.time() 