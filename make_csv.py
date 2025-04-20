import csv
import random

count = 0
dict = [] 
number_of_cells = 100
for x in range(number_of_cells):
    for y in range(number_of_cells):
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
with open('nodes.csv', 'w', newline='') as all, open('all.csv', 'w', newline='') as from_to:
    fieldnames = ['id', 'x','y','neighbours','alive']
    fieldnames_from_to =['id','id_alive','neighbour','neighbour_alive']
    writer = csv.DictWriter(all, fieldnames=fieldnames)
    writer_to_from = csv.DictWriter(from_to, fieldnames=fieldnames_from_to)
    writer.writeheader()
    writer_to_from.writeheader()
    for each in lst:
        new_dict = each
        new_dict['alive'] = 0
        writer.writerow(new_dict)
        print(each)
        id = each['id']
        neighbours = each['neighbours']     
        for i in neighbours:
            writer_to_from.writerow({"id":id,"id_alive":0,"neighbour":i,"neighbour_alive":0})