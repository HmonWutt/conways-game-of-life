import csv
import random

count = 0
dict = [] 
number_of_cells = 10
for x in range(number_of_cells):
    for y in range(10):
        dict.append({'id':count, 'x': x, 'y':y})
        count+=1  

def make_neighbours(dict):
    lst = []
    for i in dict:
        adjacency_list = []
        for neighbour in dict: 
            x_diff = abs(i['x']- neighbour['x'])%(number_of_cells-1)
            y_diff = abs(i['y'] - neighbour['y'])%(number_of_cells-1)
            if i['id']==neighbour['id']: 
                print(i['id'],neighbour['id'])
                continue
            elif x_diff <=1 and y_diff <=1:
                adjacency_list.append(neighbour['id'])
        new_dict = i
        new_dict['neighbours'] = adjacency_list
        lst.append(new_dict)
        adjacency_list = []
    return lst
               
def dead_or_alive():
    return random.randrange(0,2)


lst = make_neighbours(dict)
print(lst)
with open('nodes.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'x','y','neighbours','alive']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for each in lst:
        new_dict = each
        new_dict['alive'] = 0
        writer.writerow(new_dict)