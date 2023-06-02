import argparse
import os
import json
import imageio
import numpy as np

def parse_args():
    parser = argparse.ArgumentParser(
        description="convert transforms_train/test to transforms.json for nerfstudio")


    parser.add_argument("--output_path",
                        type=str,
                        default='360_v2/garden')
    parser.add_argument("--input_path",
                        type=str,
                        default='360_v2/garden')

    parser.add_argument("--reso", type=int, default=4)
    
    args = parser.parse_args()
    return args


def convert_pose(C2W):
    flip_yz = np.eye(4)
    flip_yz[1, 1] = -1
    flip_yz[2, 2] = -1
    C2W = np.matmul(C2W, flip_yz)
    return C2W
if __name__ == "__main__":
    args = parse_args()
    OUTPUT_PATH=args.output_path
    INPUT_PATH=args.input_path

    with open(os.path.join(INPUT_PATH,f"transforms_train.json"), "r") as f:
        tj_train = json.load(f)

    # img_0_path = os.path.join(str(tj_train['frames'][0]['file_path']))
    # img_0 = imageio.imread(img_0_path)
    w = tj_train['w'] * (4/args.reso)
    h = tj_train['h'] * (4/args.reso)
    fl_x = tj_train['fl_x'] * (4/args.reso)
    fl_y = tj_train['fl_y'] * (4/args.reso)
    cx = tj_train['cx'] * (4/args.reso)
    cy = tj_train['cy'] * (4/args.reso)
    k1 = 0
    k2 = 0
    k3 = 0
    k4 = 0
    p1 = 0
    p2 = 0
    
    transforms = {
            "fl_x": fl_x,
            "fl_y": fl_y,
            "cx": cx,
            "cy": cy,
            "w": w,
            "h": h,
            "k1": k1,
            "k2": k2,
            "k3": k3,
            "k4": k4,
            "p1": p1,
            "p2": p2,
            "frames": []
        }
    
    split=['train','test','val']
    for s in split:
        with open(os.path.join(INPUT_PATH,f"transforms_{s}.json"), "r") as f:
            tj = json.load(f)
        
        frames = tj['frames']
    
        all_frames=[]
        for frame in frames:
            file_path = frame['file_path']
            file_path = file_path[file_path.find('/')+1:]
            file_path = os.path.join(f'images_{args.reso}',file_path)
            # if 'west' not in file_path:
            #     continue
            c2w = np.array(frame['transform_matrix'])
            # c2w[0:3, 1:3] *= -1
            # c2w = c2w[np.array([1, 0, 2, 3]), :]
            # c2w[2, :] *= -1
            # c2w = convert_pose(c2w)
            all_frames.append({'file_path':file_path,'transform_matrix':c2w.tolist()})

        for i,frame in enumerate(all_frames):
            transforms['frames'].append(frame)
    

    #TODO: save
    with open(os.path.join(OUTPUT_PATH, 'transforms.json'),"w") as outfile:
        json.dump(transforms, outfile, indent=2)