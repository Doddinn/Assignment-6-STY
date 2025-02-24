#!/usr/bin/env python3

#
# Put your solution into the three functions in this file
#
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

def get_page_list(filename):
    page_access_list = []
    instruction_page_set = set()

    # TODO: Implement (remove this comment when you implemented something)
    PAGE_SIZE = 4096 # 4kib

    with open(filename, "r") as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split()
            if (len(parts)) < 2: # continue when there is empty lines
                continue
            
            access_type = parts[0][0]
            access_hex = parts[1]


            try: 
                # convert hex address to int
                address = int(access_hex, 16)
                page_number = address // PAGE_SIZE # // floor devision

                # handling diff access types from I to S
                if access_type == "I":
                    instruction_page_set.add(page_number)
                elif access_type in ("L", "S"):
                    page_access_list.append(page_number)
                elif access_type == "M":
                    page_access_list.append(page_number)
                    page_access_list.append(page_number)
            

            except ValueError:
                continue # if any convertions fail then continue

    return page_access_list, instruction_page_set


def export_page_trace(page_access_list, output_file):
    cleaned_page_list = [] # remove adjacent dublicates while maintaining the order
    prev_page = None
    for page in page_access_list:
        # to avoid page dublicates
        if page != prev_page:
            cleaned_page_list.append(page)
        prev_page = page

    with  open(output_file , "w") as file:
        for page in cleaned_page_list:
                file.write(f"{page}\n")
    

    return


def plot_memory_access(page_access_list, png_file=None, instruction_page_set=None):

    x = list(range(len(page_access_list)))

    # identify instruction and data accesses
    instruction_x = []
    instruction_y = []
    data_x = []
    data_y = []

    for i, page in enumerate(page_access_list):
        if instruction_page_set and page in instruction_page_set:
            instruction_x.append(i)
            instruction_y.append(page)
        else:
            data_x.append(i)
            data_y.append(page)

    print(f"Data points: {len(data_x)} memory accesses, {len(instruction_x)} instruction fetches.")

    # data plot
    plt.figure(figsize=(12, 6))
    plt.scatter(data_x, data_y, s=5, label="Data Access", color="blue")
    plt.scatter(instruction_x, instruction_y, s=5, label="Instruction Fetch", color="red")

    plt.xlabel("Memory Access Index")
    plt.ylabel("Page Number")
    plt.title("Memory Access Pattern")
    plt.legend()
    plt.grid(True)

    if png_file:
        plt.savefig(png_file, dpi=300)
        print(f"saved plot as {png_file}")
    else:
        plt.show()

    plt.close()  # Prevent memory leaks

    print("plot_memory_access() finished.")


if __name__ == "__main__":
    print("Running sim-paging.py...")

    # generate the page access list from the trace
    page_access_list, instruction_page_set = get_page_list("trace-compile.txt")
    print(f"Extracted {len(page_access_list)} pages from trace-compile.txt")

    # export the cleaned page trace
    export_page_trace(page_access_list, "trace-output.txt")
    print("Saved processed trace to trace-output.txt")

    # generate the memory access pattern plot
    plot_memory_access(page_access_list, "mempattern-1.png", instruction_page_set)
    print("Saved memory access pattern to mempattern-1.png")

    import os
    print("PNG file exists:", os.path.exists("mempattern-1.png"))

