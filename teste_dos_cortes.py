import turtle
from svg_turtle import SvgTurtle
import os
        
def read_file_lines(file_path):
    with open(file_path) as file:
        lines = file.readlines()
    line_lists = []
    for i, line in enumerate(lines):
        line_lists.append(f"line_{i+1}")
        line_lists[i] = line.strip().split(" ")
    return line_lists

def create_folder():
    current_dir = os.getcwd()
    existing_folders = [f for f in os.listdir(current_dir) if os.path.isdir(f) and f.startswith("cuts_of_order")]
    folder_number = len(existing_folders) + 1
    new_folder_name = "cuts_of_order_{}".format(folder_number)
    os.mkdir(new_folder_name)
    return new_folder_name

def print_vector_elements(vector, n):
    for i in range(n):
        print(vector[i + 6])
#turtle stuff starts here      

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
        t.write("{}".format(vector[-1]))
        
def cut_in_directions(x,y, t):
    cuts_in_x(x, t)
    cuts_in_y(y, t)
    
def cut_draws(cut_group):
    for i in range(len(cut_group)):
        for j in range(len(cut_group)):
            if i != j:
                turtle.clearscreen()
                print(cut_group[i], cut_group[j])
                
                draw = lambda t: cut_in_directions(cut_group[i],cut_group[j], t)
                write_file(draw, "image{}.svg".format(i), int(cut_group[i][-1])*4, int(cut_group[j][-1])*4)

def write_file(draw_func, filename, width, height):
    folder_name = create_folder()
    file_path = os.path.join(folder_name, filename)
    t = SvgTurtle(width, height)
    draw_func(t)
    t.save_as(file_path)
#turtle stuff ends here
Vert = [0]
Hori = [0]
Dep = [0]
cut_vec_list = [Vert, Hori, Dep]

file_path = input("Enter the file path: ")
lines = read_file_lines(file_path)
for i, line_list in enumerate(lines):
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
            print(f"line_{i+1}: {line_list}")
            print("Could not convert third element to integer.")
    else:
        print(f"line_{i+1}: {line_list}")

Vert.append(lines[2][5])
Hori.append(lines[2][3])
Dep.append(lines[2][1])
print("Dep:", Dep)
print("Hori:", Hori)
print("Vert:", Vert)
cut_group = [Dep, Vert, Hori]
print(cut_group)
cut_draws(cut_group)

