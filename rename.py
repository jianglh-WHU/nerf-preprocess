import argparse
import os
import json
import imageio
import numpy as np

import argparse
import os
import json
import imageio
import numpy as np
import shutil
# from load_high import load_high
# from load_road import load_road


def parse_args():
    parser = argparse.ArgumentParser(
        description="rename images to delete the prefix, e.g. building")
    
    parser.add_argument("--input_path",
                        type=str,
                        default='edit/street')

    parser.add_argument("--type",
                        type=str,
                        default='cloudy')
    
    
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    INPUT_PATH = args.input_path
    TYPE = args.type
    
    img_folder = os.path.join(INPUT_PATH,TYPE)
    
    for file_name in os.listdir(img_folder):
        if file_name.endswith(".jpeg"): # or change to the file extension of the images you want to rename
            file_path = os.path.join(img_folder, file_name)

            # new file name with your desired format, for example, adding a prefix and a sequential number
            new_file_name=file_name[file_name.find('.')+1:]
            # new_file_name = f"prefix_{str(i)}.jpg" 
            
            new_file_path = os.path.join(img_folder, new_file_name)

            # rename the file by moving it to a new path with a new name
            shutil.move(file_path, new_file_path)