#do not modify the function names
#You are given L and M as input
#Each of your functions should return the minimum possible L value
#Or return -1 if no solution exists for the given L

#Your backtracking function implementation

import time
def isSafe(assignments,marker):
    #print marker, assignments
    if marker in assignments.keys():
        if assignments[marker] == 1:	 
            return False      
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

def find_dst(nums):
   
    dist = [] 
    for i in range(0,len(nums)-1):
        for j in range(i+1,len(nums)):
                if (nums[j]-nums[i]) not in dist:			
                    dist.append(nums[j] - nums[i])
    print sum(dist),sorted(dist)

find_dst([0,1,4,10,18,23])
find_dst([0,2,3,10,16,21])
find_dst([0,1,7,11,20,23])
find_dst([0,3,4,12,18,23])
'''
0	1	4	10	18	23	25
0	2	3	10	16	21	25
0	2	6	9	14	24	25
0	1	7	11	20	23	25
0	3	4	12	18	23	
'''
	
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
    dist = sorted(dist)
    #for i in range(0,len(dist)-1):
	#    if dist[i] != dist[i+1] -1:
	#	     return False 
	
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
  
    if counter == 0 or start > L:
        if isSafefinal(assignments):
             print_ans(assignments) 		
             return True
        return False		 
    for i in range(0,L+1):		
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
    if assignments[marker] == 2:
        return False;
    
    if marker in assignments.keys():
        if assignments[marker] == 1:	 
            return False
	
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
             

   	
    remaining = [key for key,val in assignments.items() if val==0 and key>marker]
    count = len(remaining)

    	
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



	
def FCUtil(L,M,assignments,start):
    counter = M
  
    if counter == 0 or start > L:
        #print assignments	
        if isSafefinal(assignments):
             print_ans(assignments) 		
             return True
        return False

	
    for i in range(start,L+1):
        ass1 = assignments.copy()
        if(FCassigmnets(ass1,counter-1,i)):
            ass1[i] = 1
            counter = counter - 1		
            x = FCUtil(L,counter,ass1,i+1)
     
            if  x == False:
                counter = counter + 1 
                #assignments[i] = 0
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
#BT(6,4)
#BT(17,6)
print time.time() 

FC(55,10)
print time.time() 