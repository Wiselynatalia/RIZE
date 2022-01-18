

#Importing required modules
import math
import numpy as np
import random
import matplotlib.pyplot as plt
from collections import Counter
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

random.seed(45)
np.random.seed(45)
def unique (list1):
    print(*Counter(list1))
#First function to optimize
def function1(x):
    """check if multiplication is correct"""
    cost = np.array([[9000,9200,19800,29700], [8500,6700,18500,28400],[7500,8900,19800,29700,],[9999999,9999999,17800,27700]])
    value = cost *x
    total_cost = np.sum(np.concatenate(value))
    return total_cost

#Second function to optimize
def function2(x,demand):
    sum_R = x[0][0]+ x[1][0] + x[2][0] + x[3][0]
    sum_CK = x[0][1]+ x[1][1] + x[2][1] + x[3][1]
    sum_A = x[0][2]+ x[1][2] + x[2][2] + x[3][2]
    sum_J = x[0][3]+ x[1][3] + x[2][3] + x[3][3]
    ratio_R = 1- sum_R/demand['R']
    ratio_CK = 1- sum_CK/demand['CK']
    ratio_A = 1- sum_A/demand['A']
    ratio_J = 1- sum_J/demand['J']
    total_ratio = ratio_R + ratio_CK + ratio_A + ratio_J
    return total_ratio

#Function to find index of list
def index_of(a,list):
    for i in range(0,len(list)):
        if list[i] == a:
            return i
    return -1

#Function to sort by values
def sort_by_values(list1, values):
    sorted_list = []
    while(len(sorted_list)!=len(list1)):
        if index_of(min(values),values) in list1:
            sorted_list.append(index_of(min(values),values))
        values[index_of(min(values),values)] = math.inf
    return sorted_list

# fast non-dominated sorting : stage 1
def fast_non_dominated_sort(values1, values2):
    S=[[] for i in range(0,len(values1))]
    front = [[]]
    n=[0 for i in range(0,len(values1))]
    rank = [0 for i in range(0, len(values1))]

    point = 0 
    for p in range(0,len(values1)):
        S[p]=[]
        n[p]=0
        for q in range(0, len(values1)):
            #check again           
            if (values1[q] > values1[p] and values2[q] > values2[p]) or (values1[q] >= values1[p] and values2[q] > values2[p]) or (values1[q] > values1[p] and values2[q] >= values2[p]):
                if q not in S[p]:
                    S[p].append(q)
            elif (values1[p] > values1[q] and values2[p] > values2[q]) or (values1[p] >= values1[q] and values2[p] > values2[q]) or (values1[p] > values1[q] and values2[p] >= values2[q]):
                n[p] = n[p] + 1
        if n[p]==0:
            rank[p] = 0
            if p not in front[0]:
                front[0].append(p)

        point = point + 1 

    i = 0
    while(front[i] != []):
        Q=[]
        for p in front[i]:
            for q in S[p]:
                n[q] =n[q] - 1
                if( n[q]==0):
                    rank[q]=i+1
                    if q not in Q:
                        Q.append(q)
        i = i+1
        front.append(Q)

    del front[len(front)-1]
    return front

def crowding_distance(values1, values2, front):
    # all distance for the curren front solutions = 0
    distance = [0 for i in range(0,len(front))]
    #sort solutions based on objective
    sorted1 = sort_by_values(front, values1[:])
    sorted2 = sort_by_values(front, values2[:])
    distance[0] = 555555555555.55
    distance[len(front) - 1] = 555555555555.55
    for k in range(1,len(front)-1):
        #seems like there's an error here? should be values1[sorted[k+1]] - values1[sorted1[k-1]]
        distance[k] = distance[k]+ (values1[sorted1[k+1]] - values1[sorted1[k-1]])/(max(values1)-min(values1))
    for k in range(1,len(front)-1):
        distance[k] = distance[k]+ (values2[sorted2[k+1]] - values2[sorted2[k-1]])/(max(values2)-min(values2))
    return distance

def selection (temp_array,pop):

    parents = list(temp_array[:,0])
    parents2 = parents.copy()
    parents_rank = list(temp_array[:,1])
    parents_cd = list(temp_array[:,2])
    temp_copy = temp_array.copy()
    np.random.shuffle(temp_copy)
    parents_shuffle = list(temp_copy[:,0])
    parents_shuffle2 = parents_shuffle.copy()
    parents_rank_shuffle = list(temp_copy[:,1])
    parents_cd_shuffle = list(temp_copy[:,2])
    after_selection = np.empty(shape=[0,3],dtype = np.float64) # create an empty numpy array and append?? 

    while (len(after_selection)<pop):
        if(len(parents)!= 0):
            
            participants = random.sample(parents,2)
            
            if(len(after_selection) < pop/2):
                index_0 = parents2.index(participants[0])
                participant0_rank = parents_rank[index_0]
                participant0_cd = parents_cd[index_0]
                index_1 = parents2.index(participants[1])
                participant1_rank = parents_rank[index_1]
                participant1_cd = parents_cd[index_1]
                
            if (len(after_selection) >= pop/2):
                index_0 = parents_shuffle2.index(participants[0])
                participant0_rank = parents_rank[index_0]
                participant0_cd = parents_cd[index_0]
                index_1 = parents_shuffle2.index(participants[1])
                participant1_rank = parents_rank[index_1]
                participant1_cd = parents_cd[index_1]
                
            if participant0_rank < participant1_rank:
                
                after_selection = np.append(after_selection,[[participants[0],participant0_rank,participant0_cd]],axis = 0)
                
    
            elif participant0_rank > participant1_rank:
                after_selection = np.append(after_selection,[[participants[1],participant1_rank,participant1_cd]],axis = 0)
               
            elif participant0_rank == participant1_rank:
                if participant0_cd > participant1_cd:
                    after_selection = np.append(after_selection,[[participants[0],participant0_rank,participant0_cd]],axis = 0)
                    
                else:
                    after_selection = np.append(after_selection,[[participants[1],participant1_rank,participant1_cd]],axis = 0)
                    
            else :
                random_select = random.sample(participants,1)
                index_random = parents2.index(random_select[0])
                participant_rd_rank = parents_rank[index_random]
                participant_rd_cd = parents_cd[index_random]
                
                
                after_selection = np.append(after_selection, [[random_select[0],participant_rd_rank,participant_rd_cd]],axis = 0)
        
        parents.remove(participants[0])
        parents.remove(participants[1])
    
        
        if (len(parents) == 0): 
            parents = parents_shuffle.copy()
            parents_rank = parents_rank_shuffle.copy()
            parents_cd = parents_cd_shuffle.copy()
            
    
    return after_selection    

def crossover(solution_array,demand_array,m,n):
    after_crossover = np.empty(shape=[0,4,4],dtype = np.int64)
    
    x = np.copy(solution_array)
    
    while(len(x)!=0):

        choose = random.sample(range(0,len(x)),2)
        participant0 = solution_array[choose[0]]
        participant1 = solution_array[choose[1]]
        kid0_temp = participant0.copy()
        kid1_temp = participant1.copy()
        row = random.sample(range(0,4),1)
        
        
        temp_row0 = participant0[row].copy()
        temp_row1 = participant1[row].copy()

        
        
        kid0_temp[row] = temp_row1
        kid1_temp[row] = temp_row0

    
        #diff array
        sum_col0 = list(np.sum(kid0_temp,axis = 0))
        sum_col1 = list(np.sum(kid1_temp,axis = 0))
        
        diff0 = list(sum_col0 - demand_array)
        diff1 = list(sum_col1 - demand_array)

        
        for i in range(0,n):
            if diff0[i] < 0:
                poverty = True
                j = 0
                while (j < n and poverty):
                    if diff0[j] > 0:
                        k = 0
                        abundance = True
                        while (k < m and abundance):
 
                            val = min(-diff0[i],diff0[j],kid0_temp[k,j])
                            kid0_temp[k,j] = kid0_temp[k,j] - val
                            kid0_temp[k,i] = kid0_temp[k,i] + val
                            diff0[i] = diff0[i] + val
                            diff0[j] = diff0[j] - val
                            if diff0[j] == 0:
                                abundance = False
                            if diff0[i] >= 0:
                                poverty = False
                            k = k +1
                    j = j+1
        
        after_crossover = np.append(after_crossover,[kid0_temp],axis = 0)            
        
        for i in range(0,n):
            if diff1[i] < 0:
                poverty = True
                j = 0
                while (j < n and poverty):
                    if diff1[j] > 0:
                        k = 0
                        abundance = True
                        while (k < m and abundance):

                            val = min(-diff1[i],diff1[j],kid1_temp[k,j])
                            kid1_temp[k,j] = kid1_temp[k,j] - val
                            kid1_temp[k,i] = kid1_temp[k,i] + val
                            diff1[i] = diff1[i] + val
                            diff1[j] = diff1[j] - val
                            if diff1[j] == 0:
                                abundance = False
                            if diff1[i] >= 0:
                                poverty = False
                            k = k +1
                    j = j+1                   
        
        after_crossover = np.append(after_crossover,[kid1_temp],axis = 0)  
        x = np.delete(x,(choose[0],choose[1]),axis = 0)
        
        
    return after_crossover

#mutation
def mutation(solution_array,supply,m,n):
    
    solution_copy = np.copy(solution_array)
    after_mutation = np.empty(shape=[0,4,4],dtype = np.int64)
    
    for s in solution_copy:
        rows = random.sample(range(0,m),2)
        row_temp1 = np.copy(s[rows[0]])
        row_temp2 = np.copy(s[rows[1]])

        s[rows[0]] = row_temp2
        s[rows[1]] = row_temp1

        
        sum_row = list(np.sum(s,axis = 1))
                
        diff = supply[rows[0]]-supply[rows[1]]

        if diff > 0:
            positive_row = rows[1]
            negative_row = rows[0]
        else:
            positive_row = rows[0]
            negative_row = rows[1]
            
        diff = abs(diff)
        for a in range(0,n):
            val = min(s[positive_row,a],diff)
            s[positive_row, a] = s[positive_row, a] - val
            s[negative_row, a] = s[negative_row, a] + val
            diff = diff-val
            if diff == 0: 
                break 
        
        sum_row2 = list(np.sum(s,axis = 1))

            
        after_mutation = np.append(after_mutation,[s],axis = 0) 
                
        
    return after_mutation

#Main program starts here

@app.route("/")
def home():
    print("Home")
    return "Home"

@app.route("/hello")
def hello():
    print("Hello World")
    return "Hello World"

@app.route('/process', methods=['GET', 'POST'])
def main_func():
    if request.method == 'POST':
        
        W_surplus = ['WJ', 'EJ', 'CJ', 'S'] 
        W_deficit = ['R','CK','A','J']

        # Supply from each warehouse in the surplus region
        # J = Java, S = Sulawesi
        supply = {'WJ' : 400, 'EJ' : 500, 'CJ' : 300, 'S' : 600}
        values_supply = supply.values()
        #values_supply_list = list(values_supply)
        temp_supply = list(values_supply)
        total_supply = sum(values_supply)
        supply_array = np.array(temp_supply)


        # Demand of each warehouse in the deficit region
        # R = Riau, CK = Central Kalimantan, A = Ambon
        demand = {'R' : 250, 'CK' : 340, 'A' : 470, 'J' : 620}
        values_demand = demand.values()
        #values_demand_list = list(values_demand)
        temp_demand = list(values_demand)
        total_demand = sum(values_demand)
        demand_array = np.array(temp_demand)


        # Transportation Cost
        cost_dict = {'WJ': {'R' : 9000, 'CK' : 9200, 'A' : 19800, 'J' : 29700},
            'EJ': {'R' : 8500, 'CK' : 6700, 'A' : 18500, 'J' : 28400},
            'CJ': {'R' : 7500, 'CK' : 8900, 'A' : 19800, 'J' : 29700},
            'S': {'R' :9999999, 'CK' : 9999999, 'A' : 17800, 'J' : 27700},
            }



        cost = np.array([[9000,9200,19800,29700], [8500,6700,18500,28400],[7500,8900,19800,29700,],[9999999,9999999,17800,27700]])
        pop_size = 100 #pop size must be even number
        max_gen = 50


        #Initialization

        no_of_supply = len(W_surplus)
        no_of_deficit = len(W_deficit)
        matrix_size = no_of_supply * no_of_deficit
        solution = np.zeros((pop_size,no_of_supply,no_of_deficit),dtype = np.int64) #initial population
            
        for i in range(0,pop_size):

            shipped_matrix = np.zeros((no_of_supply,no_of_deficit),dtype = np.int64)
            random_seq = random.sample(range(0,matrix_size),matrix_size)

            temp_supply = list(supply.values())
            temp_demand = list(demand.values())

            for j in random_seq:
                
                row = int(j/no_of_deficit)
                col = int(j%no_of_deficit)
                value = min(temp_supply[row],temp_demand[col])

                shipped_matrix[row][col] = value
                temp_supply[row] = temp_supply[row]- value
                temp_demand[col] = temp_demand[col] - value
            for k in range(0,len(temp_supply)):
                if temp_supply[k]> 0 :
                    
                    extra = temp_supply[k]
                    random_assign = random.sample(range(0,len(temp_demand)),k=1)

                    for l in random_assign:

                        shipped_matrix[k][l] = shipped_matrix[k][l]+ extra
                        temp_supply[k] = temp_supply[k] - extra

            solution[i] = shipped_matrix
            
        ### above : generate random solutions to initialise pop_sizes
        gen_no=0
        while(gen_no < max_gen):

            
            
            function1_values = [function1(solution[i])for i in range(0,pop_size)]
            function2_values = [function2(solution[i],demand)for i in range(0,pop_size)]
            #returns front
            non_dominated_sorted_solution = fast_non_dominated_sort(function1_values[:],function2_values[:])
            count = 0
            werty= np.empty(shape=[0,4,4],dtype = np.int64)
            werty2 = []
            print("The best front for Generation number ",gen_no, " is")
            for valuess in non_dominated_sorted_solution[0]:
                print(solution[valuess],end=" ")
                print("\n")
            
            
            best = []
            for valuess in non_dominated_sorted_solution[0]:
                best.append(solution[valuess])
            

            
            #print("unique")
            #unique(ha)
            
            best2 = np.array(best)
            best_unique = (np.unique(best2,axis = 0))
            

            for haha in best_unique:
                print(haha)
                print("\n")
            
            function1_best = [function1(best_unique[i])for i in range(0,len(best_unique))]
            function2_best = [function2(best_unique[i],demand)for i in range(0,len(best_unique))]
            
            print("\n")
            crowding_distance_values=[]
            for i in range(0,len(non_dominated_sorted_solution)):
                crowding_distance_values.append(crowding_distance(function1_values[:],function2_values[:],non_dominated_sorted_solution[i][:]))
            sol_temp = solution[:]

            #create a temp array to store solution index, crowding distance value and rank
            temp = np.zeros((pop_size,3),dtype = np.float64)
            j= 0
            for a in non_dominated_sorted_solution:
                for b in a:
                    
                    temp[j][0] = b #points no 
                    temp[j][1] = non_dominated_sorted_solution.index(a) #rank no
                    j = j+1
                    
            j = 0
            for a in crowding_distance_values:
                for b in a:
                    temp[j][2] = b
                    j = j+1
                    
            #selection
            selected_parents = selection(temp,pop_size)
            selected_parents2 = np.copy(selected_parents[:,1:3])
            #create an array to store transportation matrix, f1 and f2 values, rank/front and crowding distance?

            #test = list(selected_parents[:,1])
            selected_points = list(map(int,list(selected_parents[:,0])))
            selected_rank = list(map(int,list(selected_parents[:,1])))
            selected_cd= list(map(float,list(selected_parents[:,2])))
            selected_sol = np.empty(shape=[0,4,4],dtype = np.int64)
            #boo = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[1,2,3,4]])
            #selected_sol = np.append(selected_sol,[boo],axis = 0)
            #selected_sol = np.stack((boo,selected_sol))
            new_points_index = []
            for i in range(0,len(selected_points)):
                new_points_index.append(i)
            selected_f1 = []
            selected_f2 = []
            for i in selected_points:
                selected_sol = np.append(selected_sol,[solution[i]],axis = 0)
                selected_f1.append(function1_values[i])
                selected_f2.append(function2_values[i])   
            

            
            #generating offsprings
            #crossover
            sol_crossover = crossover(selected_sol,demand_array,no_of_supply,no_of_deficit)
            
            #select random matrix from solutions/array
            
            
            #mutation
            sol_mutation = mutation(sol_crossover,supply_array,no_of_supply,no_of_deficit)
            
            solution2 = np.append(sol_temp,sol_mutation,axis = 0)
            
            ### straight copy
            function1_values2 = [function1(solution2[i])for i in range(0,2*pop_size)]
            function2_values2 = [function2(solution2[i],demand)for i in range(0,2*pop_size)]
            non_dominated_sorted_solution2 = fast_non_dominated_sort(function1_values2[:],function2_values2[:])
            crowding_distance_values2=[]
            for i in range(0,len(non_dominated_sorted_solution2)):
                crowding_distance_values2.append(crowding_distance(function1_values2[:],function2_values2[:],non_dominated_sorted_solution2[i][:]))
            new_solution= []
            for i in range(0,len(non_dominated_sorted_solution2)):
                non_dominated_sorted_solution2_1 = [index_of(non_dominated_sorted_solution2[i][j],non_dominated_sorted_solution2[i] ) for j in range(0,len(non_dominated_sorted_solution2[i]))]
                front22 = sort_by_values(non_dominated_sorted_solution2_1[:], crowding_distance_values2[i][:])
                front = [non_dominated_sorted_solution2[i][front22[j]] for j in range(0,len(non_dominated_sorted_solution2[i]))]
                front.reverse()
                for value in front:
                    new_solution.append(value)
                    if(len(new_solution)==pop_size):
                        break
                if (len(new_solution) == pop_size):
                    break
            solution = [solution2[i] for i in new_solution]
            
            gen_no = gen_no + 1

        #Lets plot the final front now

        print("The best solutions based on an initial population of " + str(pop_size) + " and after " + str(gen_no) + " iterations is ")
        print(best_unique)
        print("Total cost for each of these solutions (f1 values) are : ")
        print(function1_best)
        print("Ratio of unfulfilled demand for each of these ratios are (f2 values) are : ")
        print(function2_best)
        #index of min cost
        print("Minimum Cost Index")
        cindex = function1_best.index(min(function1_best))
        print(cindex)
        print(best_unique[cindex])
        #index of min distribution
        print("Max Distribution")
        dindex = function2_best.index(min(function2_best))
        print(dindex)
        print(best_unique[dindex])

       
        best_unique[cindex] = best_unique[cindex].tolist()
        best_unique[dindex] = best_unique[dindex].tolist()
     

        react = {"min": {"11": best_unique[cindex][0][0].tolist(), "12":best_unique[cindex][0][1].tolist(), "13":best_unique[cindex][0][2].tolist(), "14":best_unique[cindex][0][3].tolist(),
         "21": best_unique[cindex][1][0].tolist(), "22":best_unique[cindex][1][1].tolist(), "23":best_unique[cindex][1][2].tolist(), "24":best_unique[cindex][1][3].tolist(),
         "31": best_unique[cindex][2][0].tolist(), "32":best_unique[cindex][2][1].tolist(), "33":best_unique[cindex][2][2].tolist(), "34":best_unique[cindex][2][3].tolist(),
         "41": best_unique[cindex][3][0].tolist(), "42":best_unique[cindex][3][1].tolist(), "43":best_unique[cindex][3][2].tolist(), "44":best_unique[cindex][3][3].tolist(),"cost": function1_best[cindex].item()}, 
         "max": {"11": best_unique[dindex][0][0].tolist(), "12":best_unique[dindex][0][1].tolist(), "13":best_unique[dindex][0][2].tolist(), "14":best_unique[dindex][0][3].tolist(),
         "21": best_unique[dindex][1][0].tolist(), "22":best_unique[dindex][1][1].tolist(), "23":best_unique[dindex][1][2].tolist(), "24":best_unique[dindex][1][3].tolist(),
         "31": best_unique[dindex][2][0].tolist(), "32":best_unique[dindex][2][1].tolist(), "33":best_unique[dindex][2][2].tolist(), "34":best_unique[dindex][2][3].tolist(),
         "41": best_unique[dindex][3][0].tolist(), "42":best_unique[dindex][3][1].tolist(), "43":best_unique[dindex][3][2].tolist(), "44":best_unique[dindex][3][3].tolist(),"cost": function1_best[dindex].item()
         
         }}

        print("Final Result", react)
        return(jsonify(react))
    else:
        return "Not a POST request"

