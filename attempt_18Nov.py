# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 11:59:02 2021

@author: Zuo Yi
"""
import random
import numpy as np
import matplotlib.pyplot as plt

random.seed(45)

W_surplus = ['WJ', 'EJ', 'CJ', 'S'] 
W_deficit = ['R','CK','A','J']

# Supply from each warehouse in the surplus region
# J = Java, S = Sulawesi
supply = {'WJ' : 400, 'EJ' : 500, 'CJ' : 300, 'S' : 600}
values_supply = supply.values()
values_supply_list = list(values_supply)
temp_supply = values_supply_list
total_supply = sum(values_supply)


# Demand of each warehouse in the deficit region
# R = Riau, CK = Central Kalimantan, A = Ambon
demand = {'R' : 250, 'CK' : 340, 'A' : 470, 'J' : 620}
values_demand = demand.values()
values_demand_list = list(values_demand)
temp_demand = values_demand_list
total_demand = sum(values_demand)


# Transportation Cost
cost_dict = {'WJ': {'R' : 9000, 'CK' : 9200, 'A' : 19800, 'J' : 29700},
       'EJ': {'R' : 8500, 'CK' : 6700, 'A' : 18500, 'J' : 28400},
      'CJ': {'R' : 7500, 'CK' : 8900, 'A' : 19800, 'J' : 29700},
       'S': {'R' :9999999, 'CK' : 9999999, 'A' : 17800, 'J' : 27700},
       }



cost = np.array([[9000,9200,19800,29700], [8500,6700,18500,28400],[7500,8900,19800,29700,],[9999999,9999999,17800,27700]])

# initialise parent population
#initialisation
no_of_supply = len(W_surplus)
no_of_deficit = len(W_deficit)

matrix_size = no_of_supply * no_of_deficit
population = 9
ini_pop = {}
zeros_matrix = np.zeros((no_of_supply+1,no_of_deficit+1),dtype = np.int64)


for i in range(1,population+1): #rmb to change 2 to population +1
    zeros_matrix = np.zeros((no_of_supply,no_of_deficit),dtype = np.int64)
    random_seq = random.sample(range(0,matrix_size),matrix_size)
    #print(values_supply_list)
    #print(values_demand_list)
    temp_supply = list(supply.values())
    temp_demand = list(demand.values())
    #print(temp_supply)
    #print(temp_demand)
    #print(random_seq)
    for j in random_seq:
        
        row = int(j/no_of_deficit)
        col = int(j%no_of_deficit)
        value = min(temp_supply[row],temp_demand[col])
        #print(random_seq[j],row,col,value)
        zeros_matrix[row][col] = value
        temp_supply[row] = temp_supply[row]- value
        temp_demand[col] = temp_demand[col] - value
    for k in range(0,len(temp_supply)):
        if temp_supply[k]> 0 :
            #print(k)
            extra = temp_supply[k]
            random_assign = random.sample(range(0,len(temp_demand)),k=1)
            #print("random:" + str(random_assign))
            #print("extra: " + str(temp_supply[k]))
            for l in random_assign:
                #print("value old " + str(zeros_matrix[k][l]))
                zeros_matrix[k][l] = zeros_matrix[k][l]+ extra
                #print("value new " + str(zeros_matrix[k][l]))
                #print("supply old " + str(temp_supply[k]))
                temp_supply[k] = temp_supply[k] - extra
                #print("supply new " + str(temp_supply[k]))
    ini_pop["chromosome "+str(i)] = zeros_matrix
    
    
######## done with initialisation

# Calculate objective / fitness function / evaluate parent population
    
#objective 1
obj_1_temp = {}
obj_1 = {}
p = 0
for v in ini_pop.values():
    v = v*cost
    total_cost = np.sum(np.concatenate(v))
    p = p+1
    obj_1_temp['chromosome ' + str(p)] = v
    obj_1['chromosome ' + str(p)] = total_cost
    
    
#objective 2
amount_shipped_to_R = {}
amount_shipped_to_CK = {}
amount_shipped_to_A = {}
amount_shipped_to_J = {}
  
ratio_R ={}
ratio_CK ={}
ratio_A ={}
ratio_J ={}

p = 0 

obj_2 = {}

for i in ini_pop.values():
    sum_R = i[0][0]+ i[1][0] + i[2][0] + i[3][0]
    sum_CK = i[0][1]+ i[1][1] + i[2][1] + i[3][1]
    sum_A = i[0][2]+ i[1][2] + i[2][2] + i[3][2]
    sum_J = i[0][3]+ i[1][3] + i[2][3] + i[3][3]
    ratio_R2 = 1- sum_R/demand['R']
    ratio_CK2 = 1- sum_CK/demand['CK']
    ratio_A2 = 1- sum_A/demand['A']
    ratio_J2 = 1- sum_J/demand['J']
    
    p = p+1
    amount_shipped_to_R['chromosome ' +str(p)] = sum_R
    amount_shipped_to_CK['chromosome ' +str(p)] = sum_CK
    amount_shipped_to_A['chromosome ' +str(p)] = sum_A
    amount_shipped_to_J['chromosome ' +str(p)] = sum_J
    ratio_R['ratio R ' + str(p)] = ratio_R2
    ratio_CK['ratio CK ' + str(p)] = ratio_CK2
    ratio_A['ratio A ' + str(p)] = ratio_A2
    ratio_J['ratio J ' + str(p)] = ratio_J2
    
    obj_2['chromosome' + str (p)] = ratio_R2 + ratio_CK2 + ratio_A2 + ratio_J2
    
######## done with objective 

#Min-max normalization? -> not required cause both our objectives are minimization

# plotting obj values
x = list(obj_1.values())
y = list(obj_2.values())

plt.scatter(x,y, c= "green",marker =".")
plt.xlabel('Minimize obj 1')
plt.ylabel('Minimize obj 2')

#



#gen = 0, max_gen = 100

# fitness : non-dominated sorting - assing rank to each solution using the dominance depth

# fast non-dominated sorting : stage 1

#creating coordinates list
   # https://stackoverflow.com/questions/568962/how-do-i-create-an-empty-array-matrix-in-numpy    
temp1 = np.zeros(shape = (len(x),2))

for i in range(0,len(x)):
    temp1[i][0] = x[i]
    temp1[i][1] = y[i]

temp2 = temp1

#Sp = np.array()   # create empty numpy array??

# if both x y coordinates in temp 1 are less than temp 2, print yes
Sp = {}
np = []
j = 1
k = 0
for p in temp1:
    for q in temp2:
        print(j)
        print(p,q)
        if (p < q).all():
            print("yes") # append to dictionary / list?  meaning p dominates q
            Sp["S"+ str(j)] = q
            
            
        else: 
            print(" no")
            np[k] = np[k]+1
    j = j+1
    
         


#https://stackoverflow.com/questions/41468116/python-how-to-combine-two-flat-lists-into-a-2d-array
obj = np.array(list(zip(x,y)))
    

# need to transpose??






# fast non-dominated sorting: stage 2





# Crowding distance
    
    



