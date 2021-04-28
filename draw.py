#################################################################################
# Data visualization with calculation
# importing other three python files
#################################################################################
from dataBase import *
from api import *
from driver import *
from matplotlib import pyplot as plt

# import the data from database
def import_database():
    '''
    Takes in the data
    '''
    artist_list, track_list, genre_list, price_list, listeners, url = get_data()
    return track_list, listeners, price_list


### Module 1: plot the price graph
# plotting the price graph
def plotting_price(price_list):
    '''
    plot the price list by using matplotlib
    '''
    new_list = list()
    for i in price_list:
        if i >= 0:
            new_list.append(i)
    plt.plot(new_list)
    plt.title("Price distribution")
    plt.xlabel("Frequencies")
    plt.ylabel('Price')
    plt.ylim(ymin=0)
    plt.ylim(ymax=2)
    plt.legend(['Distribution line'])
    plt.show()


### Module 2: draw min and max value
# calculate the maximum
def maximum(price_list):
    return max(price_list)

# calculate the minimum
def minimum(price_list):
    return min(price_list)

# calculate the average
def average(price_list):
    return sum(price_list)/len(price_list)

# plotting min max and average
def plotting_min_max_avg(price_list):
    new_list = list()
    for i in price_list:
        if i >= 0:
            new_list.append(i)
    price_list = new_list
    max_val = maximum(price_list)
    min_val = minimum(price_list)
    avg_val = average(price_list)
    plt.title("Maximum, Minimum, and Average")
    plt.ylabel("Prices")
    value_list = [max_val, min_val, avg_val]
    title_list = ['maximum', 'minimum', 'average']
    plt.bar(title_list, value_list, color="green", width=0.3)
    plt.show()


### Module 3: how many higher than 1$
# sort and store data that higher than 1 dollor
def sorting(price_list):
    larger = 0
    smaller = 0
    for i in price_list:
        if i >= 1:
            larger += 1
        else:
            smaller += 1
    return [smaller, larger]

# plot the graph
def plotting_pie(price_list):
    sizes = sorting(price_list)
    labels = ['Price greater than 1', 'Price smaller than 1']
    explode = (0,0.1)
    plt.title("Price percentage")
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90, explode=explode)
    plt.show()


### Extra Module 4 - Listener Distribution Plotting
# using dictionary to store and separate data
def sorting_data(track_list, listeners):
    total_dict = dict()
    return_dict = dict()

    for i in range(60):
        total_dict[track_list[i]] = listeners[i]
    sorted_dict = sorted(total_dict.items(), key=lambda x:x[1], reverse=True)
    return sorted_dict[:5]

# plotting the data
def plotting_listener(track_list, listeners):
    sorted_tuple = sorting_data(track_list, listeners)
    key_list = list()
    value_list = list()
    for i in sorted_tuple:
        key_list.append(i[0])
        value_list.append(i[1])
    plt.figure(figsize=(20,10))
    plt.title('Artist vs Listener', fontsize=25)
    plt.ylabel('Number of listeners', fontsize=20)
    plt.xlabel('Name of tracks', fontsize=20)
    plt.bar(key_list, value_list, width=0.3, color='grey')
    plt.show()




def main():
    track_list, listeners, price_list = import_database()
    #plotting_price(price_list)
    #plotting_min_max_avg(price_list)
    #plotting_pie(price_list)
    plotting_listener(track_list, listeners)

main()