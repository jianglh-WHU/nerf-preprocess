from PIL import Image
import os
import json
import mmcv
import argparse
import numpy as np

def parse_args():
    parser = argparse.ArgumentParser(
        description="downsample images")

    # parser.add_argument("--output_path",
    #                     type=str,
    #                     default='china_museum')
    parser.add_argument("--input_path",
                        type=str,
                        default='jinmao')
    parser.add_argument("--input_transforms",
                        type=str,
                        default='jinmao.json')

    parser.add_argument("--downsample", type=int, default=5)
    
    args = parser.parse_args()
    return args

def downsample(tasks):
    
    img_path,w,h,reso = tasks
    
    img_name = os.path.join(*img_path.split('/')[2:])
    input_path = img_path.split('/')[0]

    img = Image.open(img_path)
    img_wh=(int(w/reso), int(h/reso))

    im_resize = img.resize(img_wh, resample=Image.LANCZOS)
    img_path=os.path.join(input_path, f'images_{reso}',img_name)

    im_resize.save(img_path, quality=90)

if __name__ == "__main__":
    args = parse_args()
    
    INPUT_PATH=args.input_path
    # OUTPUT_PATH=args.output_path
    OUTPUT_PATH = INPUT_PATH
    DOWNSAMPLE = args.downsample
    
    with open(os.path.join(INPUT_PATH,f"{args.input_transforms}"), "r") as f:
        tj = json.load(f)

    os.makedirs(os.path.join(OUTPUT_PATH,f"images_{DOWNSAMPLE}"),exist_ok=True)

    for filename in os.listdir(os.path.join(INPUT_PATH,'images')):
        full_path = os.path.join(INPUT_PATH,'images', filename)
        if os.path.isdir(full_path):
            os.makedirs(os.path.join(OUTPUT_PATH,f"images_{DOWNSAMPLE}",filename),exist_ok=True)
    
    frame_1 = tj['0']
    rot_mat =np.array(frame_1["rot_mat"])
    w = rot_mat[1,-1] 
    h = rot_mat[0,-1]
    
    tasks=[]
    for i in range(len(tj)):
        frame = tj[f'{i}']
        if 'images' in frame['path']:
            file_path = os.path.join(INPUT_PATH,frame['path'])
        else:
            file_path = os.path.join(INPUT_PATH,'images',frame['path'])
        tasks.append((file_path,w,h,DOWNSAMPLE))
        # import pdb;pdb.set_trace()
    
    mmcv.track_parallel_progress(downsample,tasks,nproc=64)
    
    