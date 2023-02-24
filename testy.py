from py3dbp import Packer, Bin, Item
import csv
import os
import subprocess
import re

packer = Packer()


# File with boxes (bins) data
print("Type the name of the file to be the input (csv) for the boxes (bins): ")
filename_bins = input()

print("Type the name of the file to be the input (csv) for the items: ")
# File with items to be fitted in the boxes
filename_items = input()

boxesDimensions = []
boxes = []
itemsDimensions = []

# Where to write the results from the calculations, relative to where this script is located
path = './results'

"""
@function read_inputs
Reads the content of the csv files with the bins (boxes) dimensions and maximum weight, save results for later
"""
def read_input():
    with open(filename_bins, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            if row[0] == "a":
                continue
            packer.add_bin(Bin(row[0], round(float(row[1])), round(float(row[2])), round(float(row[3])), round(float(row[4]))))
            boxesDimensions.append("{0} {1} {2} {3}".format(round(float(row[1])), round(float(row[2])), round(float(row[3])), round(float(row[4]))))

    with open(filename_items, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            if row[0] == "a":
                continue
            packer.add_item(Item(row[0], float(row[1]), float(row[2]), float(row[3]), float(row[4])))

read_input()
# Perform the packing calculations
packer.pack()

"""
@function set_items_to_box
Extract the dimensions of each item and save results to boxes array, prints result of items that fit to console
"""
def set_items_to_box():
    for i, b in enumerate(packer.bins):
        print(":::::::::::", b.string())
        boxes.append([])

        print("FITTED ITEMS:")
        for item in b.items:
            item_parsed = extract_dimensions(item.string())
            boxes[i].append(item_parsed)

"""
@function extract_dimensions
Gets the dimensions and weight from the strings that represent it in the csv input files, using regex
"""
def extract_dimensions(stringP):
    match = re.search(r'(\d+\.\d+)x(\d+\.\d+)x(\d+\.\d+), weight: (\d+\.\d+)', stringP)
    length, width, height, weight = match.groups()
    return "{0} {1} {2}".format(round(float(length)), round(float(width)), round(float(height)))

set_items_to_box()

"""
Will write the result of the calculations to a series of text files in the designated folder
"""
for i, b in enumerate(packer.bins):
    # Creates result folder if one doesn't exist
    os.makedirs(path, exist_ok=True)
    with open(path + '/' + str(i) + '.txt', mode='w', newline='') as file:
        file.writelines([str(len(boxes[i]))+"\n"])
        if (i != 3):
            file.writelines([boxesDimensions[i]+"\n"])
        file.writelines([item+"\n" for item in boxes[i]])
        file.writelines([b.string()])

print()
print("===========  Result from processing: ")
print()

results = []

"""
Will call the executable external program responsible for performing the box cutting calculations
"""
for filename in os.listdir(path):
    filepath = os.path.join(path, filename)
    # Uses subprocess to run external cpp compiled executable program
    output = subprocess.Popen(["teste_de_cmaismais.exe", filepath], stdout=subprocess.PIPE).communicate()[0]
    # print(output.decode())
    results.append(output.decode())

path2 = "./cuts_results"

def write_results_to_files():
    os.makedirs(path2, exist_ok=True)
    for i, result in enumerate(results):
        result = result.strip()
        if result == "" or "no cuts found" in result:
            continue
        with open(path2 + f"/result_{i}.txt", "w") as f:
            f.write(result)

write_results_to_files()

""""DRAWING GOES HERE ==========================================="""""

import turtle
from svg_turtle import SvgTurtle
import os

def read_file_lines(file_path):
    with open(file_path) as file:
        lines = file.readlines()
    line_lists = []
    for i, line in enumerate(lines):
        line_lists.append(f"line_{i + 1}")
        line_lists[i] = line.strip().split(" ")
    return line_lists


def create_folder():
    current_dir = os.getcwd()
    cuts_of_order_dir = os.path.join(current_dir, "cuts_of_order")
    if not os.path.exists(cuts_of_order_dir):
        os.mkdir(cuts_of_order_dir)
    return cuts_of_order_dir



def print_vector_elements(vector, n):
    for i in range(n):
        print(vector[i + 6])


# turtle stuff starts here

def cuts_in_x(vector, t):
    for i in vector:
        t.penup()
        t.goto(int(i), 0)
        t.pendown()
        t.goto(int(i), int(vector[-1]))


def cuts_in_y(vector, t):
    for i in vector:
        t.penup()
        t.goto(0, int(i))
        t.pendown()
        t.goto(int(vector[-1]), int(i))


def cut_in_directions(x, y, t):
    cuts_in_x(x, t)
    cuts_in_y(y, t)


def cut_draws(cut_group):
    for i in range(len(cut_group)):
        for j in range(len(cut_group)):
            if i != j:
                turtle.clearscreen()
                print(cut_group[i], cut_group[j])

                draw = lambda t: cut_in_directions(cut_group[i], cut_group[j], t)
                write_file(draw, "image{}.svg".format(i), int(cut_group[i][-1]) * 4, int(cut_group[j][-1]) * 4)


def write_file(draw_func, filename, width, height):
    folder_name = create_folder()
    file_path = os.path.join(folder_name, filename)
    t = SvgTurtle(width, height)
    draw_func(t)
    t.save_as(file_path)


# turtle stuff ends here
Vert = [0]
Hori = [0]
Dep = [0]
cut_vec_list = [Vert, Hori, Dep]

file_path = "./cuts_results/result_4.txt"
lines = read_file_lines(file_path)
new_lines = []
for line_list in lines:
    if line_list[0] == '':
        continue
    new_lines.append(line_list)

print(new_lines)

for i, line_list in enumerate(new_lines):
    if len(line_list) > 2:
        try:
            n = int(line_list[2])
            if line_list[3] == "Depth":
                for j in range(n):
                    Dep.append(line_list[j + 6])
            elif line_list[3] == "Horizontal":
                for j in range(n):
                    Hori.append(line_list[j + 6])
            elif line_list[3] == "Vertical":
                for j in range(n):
                    Vert.append(line_list[j + 6])

            print_vector_elements(line_list, n)

        except ValueError:
            print(f"line_{i + 1}: {line_list}")
            print("Could not convert third element to integer.")
    else:
        print(f"line_{i + 1}: {line_list}")

Vert.append(new_lines[2][5])
Hori.append(new_lines[2][3])
Dep.append(new_lines[2][1])
print("Dep:", Dep)
print("Hori:", Hori)
print("Vert:", Vert)
cut_group = [Dep, Vert, Hori]
print(cut_group)
cut_draws(cut_group)