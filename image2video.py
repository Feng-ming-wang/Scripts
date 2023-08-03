import os
import cv2


def images2video(input_list, video_path, delete_orig=False):
    image_list = [cv2.imread(img_file) for img_file in input_list]
    h, w, c = image_list[0].shape
    h_min = h
    w_min = w
    for img in image_list:
        h, w, c = img.shape
        h_min = min(h, h_min)
        w_min = min(w, w_min)

    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter(video_path, fourcc, 10.0, (w_min, h_min))
    for img in image_list:
        img = img[:h_min, :w_min]
        out.write(img)
    out.release()

    if delete_orig:
        for img_path in input_list:
            os.system("rm {}".format(img_path))


save_dir = './video/'
video_path = "{}/{}_demo.mp4".format(save_dir, '000')
height_curve_paths = [os.path.join(save_dir, item) for item in os.listdir(save_dir) if item.startswith('heightfloor_') and item.endswith('.png')]
height_curve_paths.sort()
images2video(height_curve_paths, video_path, delete_orig=False)