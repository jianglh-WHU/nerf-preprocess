import argparse
import os
import json
import imageio
import numpy as np
import torch


def parse_args():
    parser = argparse.ArgumentParser(
        description="convert cc json to transforms.json for nerfstudio")

    # parser.add_argument("--output_path",
    #                     type=str,
    #                     default='china_museum')
    parser.add_argument("--input_path",
                        type=str,
                        default='china_museum')
    
    parser.add_argument("--camera_path_json",
                        type=str,
                        default='test_traj.json')
    
    args = parser.parse_args()
    return args

def three_js_perspective_camera_focal_length(fov: float, image_height: int):
    """Returns the focal length of a three.js perspective camera.

    Args:
        fov: the field of view of the camera in degrees.
        image_height: the height of the image in pixels.
    """
    if fov is None:
        print("Warning: fov is None, using default value")
        return 50
    pp_h = image_height / 2.0
    focal_length = pp_h / np.tan(fov * (np.pi / 180.0) / 2.0)
    return focal_length

    
if __name__ == "__main__":
    args = parse_args()
    
    camera_path = os.path.join(args.input_path,'camera_paths',f"{args.camera_path_json}")
    os.makedirs(os.path.join(args.input_path,'camera_transforms'),exist_ok=True)
    output_path = os.path.join(args.input_path,'camera_transforms',f"{args.camera_path_json}")
    
    with open(camera_path, "r", encoding="utf-8") as f:
        camera_path = json.load(f)
    seconds = camera_path["seconds"]
    
    image_height = camera_path["render_height"]
    image_width = camera_path["render_width"]

    c2ws = []
    fov = camera_path["camera_path"][0]["fov"]
    angle_x = fov/180*np.pi
    focal_length = three_js_perspective_camera_focal_length(fov, image_height)
    fl_x=focal_length
    fl_y=focal_length
    cx=image_width / 2
    cy=image_height / 2
    
    
    for camera in camera_path["camera_path"]:
        # pose
        c2w = torch.tensor(camera["camera_to_world"]).view(4, 4)[:3]
        c2ws.append(c2w)
        
        # field of view
        
    camera_to_worlds = torch.stack(c2ws, dim=0)
    # import pdb; pdb.set_trace()
    transforms = {
            "camera_angle_x": angle_x,
            "camera_model": "SIMPLE_PINHOLE",
            "fl_x": fl_x,
            "fl_y": fl_y,
            "cx": cx,
            "cy": cy,
            "w": image_width,
            "h": image_height,
            "frames": []
        }
    
    all_frames=[]
    
    for i in range(camera_to_worlds.shape[0]):
        all_frames.append({'transform_matrix':camera_to_worlds[i].numpy().tolist()})
    
    for i,frame in enumerate(all_frames):
        transforms['frames'].append(frame)
        
    with open(os.path.join(output_path),"w") as outfile:
        json.dump(transforms, outfile, indent=2)