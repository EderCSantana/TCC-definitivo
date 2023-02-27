from py3dbp import Packer, Bin, Item
import csv
import os
import subprocess
import re
import turtle
from svg_turtle import SvgTurtle
import os
packer = Packer()

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

"""
@function write_results_to_files
Save the txt documents with the results of the knapsack code 
"""
def write_results_to_files():
    os.makedirs(path2, exist_ok=True)
    for i, result in enumerate(results):
        result = result.strip()
        if result == "" or "no cuts found" in result:
            continue
        with open(path2 + f"/result_{i}.txt", "w") as f:
            f.write(result)


"""
@function read_file_lines
Gets the path of a file and organize their lines in a vector
"""
def read_file_lines(file_path):
    with open(file_path) as file:
        lines = file.readlines()
    line_lists = []
    for i, line in enumerate(lines):
        line_lists.append(f"line_{i + 1}")
        line_lists[i] = line.strip().split(" ")
    return line_lists


"""
@function create_folder
If there's no folder named cuts_of_order, it creates one and return it's directory
"""
def create_folder():
    current_dir = os.getcwd()
    cuts_of_order_dir = os.path.join(current_dir, "cuts_of_order")
    if not os.path.exists(cuts_of_order_dir):
        os.mkdir(cuts_of_order_dir)
    return cuts_of_order_dir


"""
@function print_vector_elements
Prints the elements of a vector starting after 6 positions
"""
def print_vector_elements(vector, n):
    for i in range(n):
        print(vector[i + 6])


"""
@function create_folder
Create a folder with the name 'cuts_of_order' in the current working directory
"""
def create_folder():
    folder_name = 'cuts_of_order'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

def draw_borders(x, y, t, scale_factor, width, height):
    last_x = int(x[-1]) * scale_factor
    last_y = int(y[-1]) * scale_factor
    
    t.penup()
    t.goto(0, 0)
    t.pendown()
    t.goto(0, last_y)
    
    t.penup()
    t.goto(0, last_y)
    t.pendown()
    t.goto(last_x, last_y)
    
    t.penup()
    t.goto(last_x, last_y)
    t.pendown()
    t.goto(last_x, 0)
    
    t.penup()
    t.goto(last_x, 0)
    t.pendown()
    t.goto(0, 0)
    
    


"""
@function 
Gets a vector and a parameter for turtle and draws straigt lines on x-axis
"""
def cuts_in_x(vector, t, scale_factor, width, height):
    for i in vector:
        x = int(i) * scale_factor
        y0 = 0
        y1 = int(vector[-1]) * scale_factor
        
        t.penup()
        t.goto(x, y0)
        t.pendown()
        t.goto(x, y1)
        t.write(int(i))


        
"""
@function 
Gets a vector and a parameter for turtle and draws straigt lines on x-asis
"""
def cuts_in_y(vector, t, scale_factor, width, height):
    for i in vector:
        x0 = 0
        x1 = int(vector[-1]) * scale_factor
        y = int(i) * scale_factor
        
        t.penup()
        t.goto(x0, y)
        t.pendown()
        t.goto(x1, y)
        t.write(int(i))
        
            
        
"""
@function cut_in_directions
Transfer the parameters that it gets to the cutting functions 
"""
def cut_in_directions(x, y, t, width, height):
    max_x = max(int(cut[-1]) for cut in (x, y))
    max_y = max_x
    
    image_width = max_x * 2
    image_height = max_y * 2
    
    scale_factor = 10#min(width, height) / max(image_width, image_height)*2
    
    draw_borders(x, y, t, scale_factor, width, height)
    cuts_in_x(x, t, scale_factor, width, height)
    cuts_in_y(y, t, scale_factor, width, height)

"""
@function cut_draws
Gets the sets of cuts and draws straigt cuts in a SVG
"""
def cut_draws(result_number, cut_group):
    width = 1000
    height = 1000
    
    for i in range(len(cut_group)):
        for j in range(len(cut_group)):
            if i != j:
                turtle.clearscreen()
                print(cut_group[i], cut_group[j])

                draw = lambda t: cut_in_directions(cut_group[i], cut_group[j], t, width, height)
                write_file(draw, "image_{0}_{1}.svg".format(result_number, i), width, height)


"""
@function write_file
Gets a funtion to draw, a name to a SVG and it's dimensions and creates a svg file to save a draw done with the function
"""
def write_file(draw_func, filename, width, height):
    folder_name = create_folder()
    file_path = os.path.join(folder_name, filename)
    t = SvgTurtle(width, height)
    draw_func(t)
    t.save_as(file_path)


"""
@function makes_pretty_images
Gets the results of the Paker, for each result organizes the input to the program that solves the cuts
"""
def makes_pretty_images():
    for file_name in os.listdir(directory_path):
        if file_name.startswith("result_") and file_name.endswith(".txt"):
            file_path = os.path.join(directory_path, file_name)
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
    cut_draws(file_name, cut_group)

def generate_html_with_svg_files():
    # Define the folder containing the SVG files
    folder = ".\cuts_of_order"
    
    # Get a list of all the SVG files in the folder
    svg_files = [f for f in os.listdir(folder) if f.endswith(".svg")]
    
    # Create the HTML document
    html = "<html><head><title>Packing options</title></head><body>"
    
    # Loop through each SVG file and add it to the HTML document
    for svg_file in svg_files:
        # Get the name of the SVG file without the file extension
        name = os.path.splitext(svg_file)[0]
        
        # Add the name of the SVG file to the HTML document
        html += f"<h1>{name}</h1>"
        
        # Add the SVG file to the HTML document
        html += f'<object type="image/svg+xml" data="{folder}/{svg_file}"></object>'
    
    # Close the HTML document
    html += "</body></html>"
    
    # Write the HTML document to a file
    with open("packing_options.html", "w") as f:
        f.write(html)

# File with boxes (bins) data
print("Type the name of the file to be the input (csv) for the boxes (bins): ")
filename_bins = input()

print("Type the name of the file to be the input (csv) for the items: ")
# File with items to be fitted in the boxes
filename_items = input()

size_corrector = 20
boxesDimensions = []
boxes = []
itemsDimensions = []

# Where to write the results from the calculations, relative to where this script is located
path = './results'

read_input()
# Perform the packing calculations
packer.pack()

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
path2 = "./cuts_results"  

"""
Will call the executable external program responsible for performing the box cutting calculations
"""
for filename in os.listdir(path):
    filepath = os.path.join(path, filename)
    # Uses subprocess to run external cpp compiled executable program
    output = subprocess.Popen(["DP3SUK.exe", filepath], stdout=subprocess.PIPE).communicate()[0]
    # print(output.decode())
    results.append(output.decode())

path2 = "./cuts_results"  

write_results_to_files()
#vectors to store the cuts           
Vert = [0]
Hori = [0]
Dep = [0]
cut_vec_list = [Vert, Hori, Dep]

directory_path = "./cuts_results"


makes_pretty_images()

generate_html_with_svg_files()
