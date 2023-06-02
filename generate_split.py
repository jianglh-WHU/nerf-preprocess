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

    parser.add_argument("--train_skip",
                        type=int,
                        default=10,
                        help="index%train_skip==9 -> test")

    parser.add_argument("--input_path",
                        type=str,
                        default='china_museum')

    args = parser.parse_args()
    return args



if __name__ == "__main__":
    args = parse_args()
    
    INPUT_PATH = args.input_path
    TRAIN_SKIP = args.train_skip

    with open(os.path.join(INPUT_PATH,"transforms.json"), "r") as f:
        tj = json.load(f)
        
    img_0_path = os.path.join(INPUT_PATH,TYPE,'rgb',str(tj['frames'][0]['frame_index']).zfill(4)+'.jpeg')
    img_0 = imageio.imread(img_0_path)
    
    angle_x = tj['camera_angle_x']
    frames = tj['frames']
    w = float(img_0.shape[1])
    h = float(img_0.shape[0])
    fl_x = float(.5 * w / np.tan(.5 * angle_x))
    fl_y = fl_x
    k1 = 0
    k2 = 0
    k3 = 0
    k4 = 0
    p1 = 0
    p2 = 0
    cx = w / 2
    cy = h / 2
    
    
    all_frames=[]
    c2ws=[]
    for frame in frames:
        
        c2w = np.array(frame['transformation_matrix'])
        c2w[:3,:3] *= 100
        c2w[...,3] /= SCALE
        c2ws.append(c2w)
        
        
    c2ws=np.array(c2ws)
    origins = c2ws[..., :3, 3]

    mean_origin = np.mean(origins, axis=0)
    c2ws[..., :3, 3] -= mean_origin
    
    for i,frame in enumerate(frames):
        c2w=c2ws[i]
        file_path = os.path.join('rgb',str(frame['frame_index']).zfill(4)+'.jpeg')
        all_frames.append({'file_path':file_path,'transform_matrix':c2w.tolist()})
        
    train_json = {
            "camera_angle_x": angle_x,
            "fl_x": fl_x,
            "fl_y": fl_y,
            "k1": k1,
            "k2": k2,
            "k3": k3,
            "k4": k4,
            "p1": p1,
            "p2": p2,
            "cx": cx,
            "cy": cy,
            "w": w,
            "h": h,
            "aabb_scale": AABB_SCALE,
            "frames": []
        }

    test_json = {
        "camera_angle_x": angle_x,
        "fl_x": fl_x,
        "fl_y": fl_y,
        "k1": k1,
        "k2": k2,
        "k3": k3,
        "k4": k4,
        "p1": p1,
        "p2": p2,
        "cx": cx,
        "cy": cy,
        "w": w,
        "h": h,
        "aabb_scale": AABB_SCALE,
        "frames": []
    }
    
    for i,frame in enumerate(all_frames):
        if i % TRAIN_SKIP == 9:
            test_json['frames'].append(frame)
        else:
            train_json['frames'].append(frame)
    val_json = test_json
    
    #TODO: save
    with open(os.path.join(INPUT_PATH, 'transforms_train.json'),"w") as outfile:
        json.dump(train_json, outfile, indent=2)
    with open(os.path.join(INPUT_PATH, 'transforms_test.json'),"w") as outfile:
        json.dump(test_json, outfile, indent=2)
    with open(os.path.join(INPUT_PATH, 'transforms_val.json'), "w") as outfile:
        json.dump(val_json, outfile, indent=2)