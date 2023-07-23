##########################################################################
# Title: Patience can Pay
# Author: Preston Brubaker
# Revised: 7/22/23
# Purpose: To demonstrate the effect of rate of food into an environment
#          can affect the rate of metabolism in a group of organisms.
# Method: Organisms will the following parameters: rate of food consumption,
#         and reproduction ratio (ratio of internal food given to an offspring)
#         and reproduciton chance (chance of splitting if above the global
#         minimum requirement
############################################################################

import random
import time
import statistics
import matplotlib.pyplot as plt


#variables
org_id = []         # ID number of the organism
org_food = []       # Amount of food the organism has
org_carn = []       # Carnivorous if over 0.5, not carnivorous if under 0.5
org_age = []        # Age of organism
org_mut_frac = []       # Fraction of maximum change an organism can recieve on a trait

food = 1000   # Total food available for organisms
food_gen_rate = 20000  # Amount of food generated for global food supply each turn
mut_frac_i = 0.005     # Initial fraction of maximum change an organism can recieve on a trait
loss_linear = 1   # Fixed amount of food lost from each turn by each organism
death_note = []     # A boolean list that is continually updated with organisms to be killed each turn. True = needs killed
prior_ord = []      # A list that allows for fair priority
rep_req = 1000         # Amount of food needed to reproduce
it_c = 0            # Iteration count
met_rate = 0.001        # Rate of food use by organisms when food is around
org_c = 10000    # Initial organisms to be generated and later the index of the organisms ever generated
death_age = 100000     # Age at which an organism is killed
rand_death_chance = 0.0001    #chance of random death
carn_eff = .02       #carnivore efficiency
global hist_int
hist_int = 100

def gen_orgs():
    i = 0
    while i<org_c:
        org_id.append(int(i))
        org_food.append(rep_req * .8)
        org_carn.append(random.uniform(0,1))
        org_age.append(0)
        org_mut_frac.append(mut_frac_i)
        death_note.append(False)
        i += 1
    return "orgs generated"


def sim_loop():
    global org_cg, food

    # Add food to the environment
    food += food_gen_rate

    # Shuffling the organism ids for fairness
    random.shuffle(org_id)

    # Eat food, allow carnivorous to eat each other, loss of food from metabolism and write the death note
    for idx, i in enumerate(org_id):  # Here, idx is the index and i is the id
        # Iterate the age of each organism
        org_age[idx] += 1
        # Food eaten
        if(food >= 0 and org_carn[idx] < 0.5):
            food_eaten = met_rate * food
            org_food[idx] += food_eaten
            food -= food_eaten
        # Eat each other
        if(org_carn[idx] > 0.5):
            escape = 0
            j = idx
            while j == idx and escape <= 1000:
                j = random.randint(0,len(org_id) - 1)
                escape += 1

            food_trans = org_carn[idx] * org_food[j] * carn_eff
            org_food[idx] += food_trans
            org_food[j] -= food_trans

        # Food lost
        org_food[idx] = org_food[idx] - loss_linear
        # Write the death note
        if org_food[idx] < 0 or org_age[idx] / death_age > random.uniform(0,1) or random.uniform(0,1) < rand_death_chance:
            death_note[idx] = True

    # Execute the weak and old
    to_be_removed = [i for i, val in enumerate(death_note) if val == True]
    for i in sorted(to_be_removed, reverse=True):
        org_id.pop(i)
        death_note.pop(i)
        org_food.pop(i)
        org_carn.pop(i)
        org_age.pop(i)
        org_mut_frac.pop(i)

    # Allow organisms to reproduce
    for idx, i in enumerate(org_id):  # idx is index and i is id
        r = random.uniform(0, 1)
        if (r < 0.1 and org_food[idx] > rep_req):
            global org_c  # Declare org_c as global
            j = org_c
            org_c += 1
            org_id.append(int(j))
            death_note.append(False)  # Add a new entry to death_note for the new organism
            food_trans = org_food[idx] * 0.5  # Amount of food to be transferred from parent to offspring
            org_food.append(food_trans)
            org_food[idx] -= food_trans
            org_carn.append(org_carn[idx] * (random.uniform(1 - org_mut_frac[idx], 1 + org_mut_frac[idx])))
            org_mut_frac.append(org_mut_frac[idx] * (random.uniform(1 - org_mut_frac[idx], 1 + org_mut_frac[idx])))
            org_age.append(0)
            if org_carn[idx] > 1:
                org_carn[idx] = 1
            if org_carn[len(org_id) - 1] > 1:
                org_carn[len(org_id) - 1] = 1



    return food, org_c


# Function to get user input for the next interval
def get_next_interval():
    global hist_int
    while True:
        user_input = input("Enter the next interval for the histogram: ")
        if user_input.isdigit():
            hist_int = int(user_input)
            break
        else:
            print("Invalid input. Please enter a valid integer.")



# Initialize
print(gen_orgs())

# Time loop
while True:

    # Histogram
    if (it_c % hist_int == 0):
        # Get user input for the next interval
        get_next_interval()
        plt.figure()
        plt.hist(org_carn, bins=100, edgecolor='black')
        plt.title('Organism Carnivore Histogram   Iteration: ' + str(it_c))

        plt.figure()
        plt.hist(org_food, bins=100, edgecolor='black')
        plt.title('Organism Food Histogram   Iteration: ' + str(it_c))

        plt.figure()
        plt.hist(org_mut_frac, bins=100, edgecolor='black')
        plt.title('Organism Mutation Rate Histogram   Iteration: ' + str(it_c))

        plt.figure()
        plt.hist(org_age, bins=100, edgecolor='black')
        plt.title('Organism Age Histogram   Iteration: ' + str(it_c))

        plt.show()

    it_c += 1
    sim_loop()
    carn_count = 0
    herb_count = 0
    for i in org_carn:
        if(i > .5):
            carn_count += 1
        else:
            herb_count += 1

    rel_data = ["Iteration count: " + str(it_c), "Oranism count: " + str(len(org_id)),
                "Food available: " + str("{:.2f}".format(food)), "Avg. food per org.: " + str("{:.2f}".format(statistics.mean(org_food))),
                "Avg. carn frac.: " + str("{:.2f}".format(statistics.mean(org_carn))),"Std. dev. of carn frac.: " + str("{:.2f}".format(statistics.pstdev(org_carn))),
                "Avg. org. age: " + str("{:.2f}".format(statistics.mean(org_age))), "Carnivore count: " + str(carn_count), "Herbivore count: " + str(herb_count),
                "Avg. mut. rate: " + str("{:.6f}".format(statistics.mean(org_mut_frac)))]

    print(rel_data)


    if 1 == 0:
        time.sleep(1)   # Allow one second to pass before the next loop

