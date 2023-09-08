import random
import matplotlib.pyplot as plt

def transaction(agent1,agent2,agents_array,f):
    x = random.randint(1,10)
    if agents_array[agent1]>=agents_array[agent2]:
        transaction_size = f*agents_array[agent2]
    else:
        transaction_size = f*agents_array[agent1] 
    if x>5:
        agents_array[agent1] = agents_array[agent1] + transaction_size
        agents_array[agent2] = agents_array[agent2] - transaction_size
    else:
        agents_array[agent2] = agents_array[agent2] + transaction_size
        agents_array[agent1] = agents_array[agent1] - transaction_size
    return agents_array

def transaction_det_col(agent1,agent2,agents_array):
    sum_agents = agents_array[agent1] + agents_array[agent2];
    avg_agents = sum_agents/2
    agents_array[agent1] = avg_agents
    agents_array[agent2] = avg_agents
    return agents_array

def rand_transaction(agent1,agent2,agents_array):
    r = random.random() #the ratio
    sum_agents = agents_array[agent1] + agents_array[agent2];
    agents_array[agent1] = r*sum_agents
    agents_array[agent2] = (1-r)*sum_agents
    return agents_array

def Three_agents_transaction(agent1,agent2,agent3,agents_array,r):
    #this is win-win-loose model of transaction
    agents_array[agent2] = agents_array[agent2] + (r/2)*agents_array[agent1]
    agents_array[agent3] = agents_array[agent3] + (r/2)*agents_array[agent1]
    agents_array[agent1] = agents_array[agent1] - r*agents_array[agent1]
    return agents_array

def agents(n,wealth,m,f,poor_condition,tax_bin,k,tax_rate,transaction_type,rng_init_wlth,r):
    # n - number of agents,
    # wealth - the firsy sum of each agent
    # m - the number of iteration - transaction
    # k - the num of iteration 
    t = 1 #for plotting the histogram each 10^t iteration
    
    poor_people_precentage_arr = m*[0]
    max_wealth_arr = m*[0]
    Precentage_of_largest_ten_precentage_arr = m*[0]
    
    #define the init agents_array according the type of transaction:
    agents_array_initial = n*[wealth]

    if transaction_type==2:
        for i in range(0,n):
            agents_array_initial[i] = random.randint(0,2000) 
    agents_array = agents_array_initial

    for i in range(0,m):
        agent1 = 1
        agent2 = 1
        while agent1==agent2:
            agent1 = random.randint(0,n-1)
            agent2 = random.randint(0,n-1)
        if transaction_type == 1:
            agents_array = transaction(agent1,agent2,agents_array,f)
        elif transaction_type == 2:
            agents_array = transaction_det_col(agent1,agent2,agents_array)
        elif transaction_type == 3:
            agents_array = rand_transaction(agent1,agent2,agents_array)
        else:
            agent3 = agent1
            while agent3==agent1 or agent3==agent2:
                agent3 = random.randint(0,n-1)
            agents_array = Three_agents_transaction(agent1,agent2,agent3,agents_array,r)
                
        poor_people_precentage,max_wealth,Precentage_of_largest_ten_precentage = data(wealth,agents_array,poor_condition)  
        if tax_bin == 1: #activate the tax function
            if (i+1)/k == int((i+1)/k):
                agents_array = tax(agents_array,tax_rate)   
        #update the data arrays:
        poor_people_precentage_arr[i] = poor_people_precentage
        max_wealth_arr[i] = max_wealth
        agents_array.sort()
        Precentage_of_largest_ten_precentage_arr[i] = Precentage_of_largest_ten_precentage
        
        #plot histogram:
        if (i+1) == 10**t:
            plot_histograms(agents_array,t)
            t += 1;
        
    #print the consequences:
    print("")
    print("The agent array is: ",agents_array)
    print("")
    print("The percentage of poor is: " + str(poor_people_precentage*100) + "%")
    print("The maximum of wealth is: ",max_wealth)
    print("The percentage of wealth of the top decile is: " + str(Precentage_of_largest_ten_precentage*100) +"%")
    
    
    return agents_array,agents_array_initial, poor_people_precentage_arr, max_wealth_arr, Precentage_of_largest_ten_precentage_arr


def plot_agent_arr(agents_array):
    index_agent = list(range(len(agents_array)))
    for i in range(len(agents_array)):
        plt.scatter(index_agent,agents_array, color='g', marker = '.')
        #if we want only points we need to write - plt.scatter
    plt.xlabel("Index of Agent")
    plt.ylabel("Wealth")
    plt.title("Wealth of Agents")
    plt.show()
    
def data(init_wealth,agents_array,poor_condition):
    #check how many poor people:
    n = len(agents_array)
    poor_people_amount = 0
    ten_precentage = int(n/10)
    sum_largest_ten_precentage = 0
    for i in range(0,n):
        if agents_array[i] < poor_condition:
            poor_people_amount+=1
    poor_people_precentage = poor_people_amount/n
    for i in range(0,ten_precentage):
        sum_largest_ten_precentage = sum_largest_ten_precentage + agents_array[n-i-1]
    Precentage_of_largest_ten_precentage = sum_largest_ten_precentage/(init_wealth*n)
    max_wealth = max(agents_array)
    return poor_people_precentage,max_wealth,Precentage_of_largest_ten_precentage
            

#plotting: 
    
def plot_data_array(arr_poor,arr_max, arr_ten_lrgst):
    # Initialise the subplot function using number of rows and columns
    
    Iteration_vec = list(range(len(arr_ten_lrgst)))
    
    figure, axis = plt.subplots(3)
      
    # For Poor Precentage
    axis[0].plot(Iteration_vec, arr_poor)
    axis[0].set_title("Poor Precentage")
      
    # For Maximum Wealth
    axis[1].plot(Iteration_vec, arr_max)
    axis[1].set_title("Maximum Wealth")
      
    # For Ten Precetage Wealth
    axis[2].plot(Iteration_vec, arr_ten_lrgst)
    axis[2].set_title("Ten Precetage Wealth")
          
    # Combine all the operations and display
    plt.show()    

def plot_histograms(agents_array,t):
    n = len(agents_array) 
    n1 = int(n)
    plt.hist(agents_array, bins=40)
    plt.xlabel("Wealth of Agents")
    plt.title("Histogram: Wealth of Agents in iteration 10^(" +str(t) +")")
    plt.show()


#Model with tax:
def tax(agents_array,tax_rate):
    total_tax = 0
    n = len(agents_array)
    for i in range(0,n):
        total_tax += tax_rate*agents_array[i]
        agents_array[i] = agents_array[i] - tax_rate*agents_array[i]
    per_tax = total_tax/n
    for i in range(0,n):
        agents_array[i] += per_tax
    return agents_array

def main():
    
    #Global input:
    poor_condition = 100 #the condition that defines the poor people
    init_wealth = 1000 #initial wealth of each agent 
    iteration_num = 1000000 #number of transactions
    n = 10000 #number of agents
    
    #input according the transaction model:
    #Model 1:
    f = 0.25 #the size of transaction (Precentage)
    
    #tax:
    tax_bin = 0 #with tax -> 1 else no tax
    k = 1000 #the num of iteration to take a tax of the agents
    
    #Model 2: sum of the agent divide equally
    tax_rate = 0.1
    rng_init_wlth = 2000 #set the init range
    
    #Model 3:
    #just choose transaction_type = 3
   
    #Model 4:
    r = 0.5 #r is the precentage that the loser loose from his wealth
    
    #choose the Model:
    transaction_type = 4 #1,2,3
    
    
    #activate the program:
    agents_array, agents_array_initial,arr_poor, arr_max, arr_ten_lrgst = agents(n,init_wealth,iteration_num,f,poor_condition,tax_bin,k,tax_rate,transaction_type,rng_init_wlth,r)
    agents_array.sort()
    plot_agent_arr(agents_array)
    data(init_wealth,agents_array,poor_condition)
    plot_data_array(arr_poor,arr_max, arr_ten_lrgst)


    
main()