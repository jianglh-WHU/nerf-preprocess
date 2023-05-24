import cv2 as cv
import numpy as np
import argparse
import os
os.environ["OPENCV_IO_ENABLE_OPENEXR"]="1"

def parse_args():
    parser = argparse.ArgumentParser(
        description="depth exr to png.")
    
    parser.add_argument("--depth_path", type=str, default='data/edit/building/sunny/depth')

    args = parser.parse_args()
    return args

args = parse_args()
depth_path=args.depth_path
depth_files=os.listdir(depth_path)
import pdb
pdb.set_trace()
for i in depth_files:
    exr_mat = cv.imread(os.path.join(depth_path,i), cv.IMREAD_ANYCOLOR | cv.IMREAD_ANYDEPTH)
    #scale=exr_mat.max()
    prefix=i[0:i.find('.')]
    scale=25600
    exr_mat=(exr_mat/scale*255).astype(np.uint8)
    cv.imwrite(os.path.join(depth_path,f'{prefix}.png'), exr_mat)