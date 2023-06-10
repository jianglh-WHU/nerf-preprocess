import argparse
import os
import json
import imageio
import numpy as np
import torch

def parse_args():
    parser = argparse.ArgumentParser(
        description="add 2+ json into 1 json")

    # parser.add_argument("--output_path",
    #                     type=str,
    #                     default='china_museum')
    parser.add_argument("--input_path",
                        type=str,
                        default='wukang')
    
    parser.add_argument("--input_transforms",
                        type=str,
                        nargs='+')
    
    parser.add_argument("--output_transforms",
                        type=str,
                        default='transforms_tiejin.json')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    
    INPUT_PATH=args.input_path
    # OUTPUT_PATH=args.output_path
    OUTPUT_PATH = INPUT_PATH

    transforms = {
            "camera_model": "SIMPLE_PINHOLE",
            "orientation_override": "none",
            "frames": []
        }
    all_frames=[]
    # import pdb;pdb.set_trace()
    for i in args.input_transforms:
        with open(os.path.join(INPUT_PATH,f"{i}"), "r") as f:
            tj = json.load(f)
        
        all_frames = tj['frames']
        for j,frame in enumerate(all_frames):
            file_path = frame['file_path']
            # correct=False
            # for type in args.type:
            #     # print(type)
            #     if type in file_path:
            #         correct=True
            #         break
            # # if args.type not in file_path:
            # #     continue
            # if correct==False:
            #     continue
            transforms['frames'].append(frame)
    
    #TODO: save
    with open(os.path.join(OUTPUT_PATH, args.output_transforms),"w") as outfile:
        json.dump(transforms, outfile, indent=2)