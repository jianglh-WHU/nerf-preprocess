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
# from load_high import load_high
# from load_road import load_road


def parse_args():
    parser = argparse.ArgumentParser(
        description="generate train/test/val json.")

    parser.add_argument("--type",type=str,default='camera')

    parser.add_argument("--input_path",
                        type=str,
                        default='wukang')
    
    parser.add_argument("--input_transforms",
                        type=str,
                        default='transforms_tiejin_6_qingxie.json')
    
    parser.add_argument("--output_transforms",
                        type=str,
                        default='transforms_qingxie.json')

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()

    INPUT_PATH=args.input_path
    # OUTPUT_PATH=args.output_path
    OUTPUT_PATH = INPUT_PATH

    # SCALE = args.scale

    with open(os.path.join(INPUT_PATH,f"{args.input_transforms}"), "r") as f:
        tj = json.load(f)

    transforms = {
            "camera_model": "SIMPLE_PINHOLE",
            "orientation_override": "none",
            "frames": []
        }
    all_frames=[]
    with open(os.path.join(INPUT_PATH,f"{args.input_transforms}"), "r") as f:
        tj = json.load(f)
        
    all_frames = tj['frames']
    for j,frame in enumerate(all_frames):
        file_path = frame['file_path']
        if args.type not in file_path:
            continue
        transforms['frames'].append(frame)
    
    #TODO: save
    with open(os.path.join(OUTPUT_PATH, args.output_transforms),"w") as outfile:
        json.dump(transforms, outfile, indent=2)