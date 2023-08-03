import os
import cv2
import sys
import numpy as np

def merge_three_mp4(video1_path, video2_path, video3_path, output_path):
    video1 = cv2.VideoCapture(video1_path)
    video2 = cv2.VideoCapture(video2_path)
    video3 = cv2.VideoCapture(video3_path)
    
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = None
    
    while True:
        ret1, frame1 = video1.read()
        ret2, frame2 = video2.read()
        ret3, frame3 = video3.read()
        if frame1 is None or frame2 is None or frame3 is None: break
    
        h1,w1,c1 = frame1.shape
        h2,w2,c2 = frame2.shape
        h3,w3,c3 = frame3.shape
    
        assert h1 == h2
        assert h1 == h3
        assert w1 == w2
        assert w1 == w3
        if out is None:
            out = cv2.VideoWriter(output_path, fourcc, 10.0, (w1+w2+w3, h1))
        out_frame = np.stack([frame1, frame2, frame3], 1).reshape([h1,w1+w2+w3,c1])
        out.write(out_frame)
    
    out.release()

def merge_many_mp4(video_paths, output_path):
    videos = [cv2.VideoCapture(video_path) for video_path in video_paths]
    
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = None
    
    while True:
        frames = [video.read()[1] for video in videos]
        stop = False
        for frame in frames:
            if frame is None: 
                stop=True
                continue
        if stop: break

        input_heights = [frame.shape[0] for frame in frames]
        input_widths = [frame.shape[1] for frame in frames]
        input_channels = [frame.shape[2] for frame in frames]

        out_height = min(input_heights)
        out_width = sum(input_widths)
        out_channel = input_channels[0]
    
        if out is None:
            out = cv2.VideoWriter(output_path, fourcc, 10.0, (out_width, out_height))
        if False:
            out_frame = np.zeros([out_height, out_width, out_channel]).astype('uint8')
            offset = 0
            for frame in frames:
                out_frame[:,offset:offset+frame.shape[1],:] = frame
                offset = offset + frame.shape[1]
        else:
            out_frame = np.stack(frames, 1).reshape([out_height,out_width,out_channel])
        out.write(out_frame)
    
    out.release()

def merge_many_mp4_v2(video_paths, output_path):
    videos = [cv2.VideoCapture(video_path) for video_path in video_paths]
    
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = None
    
    prev_frames = [None] * len(videos)

    while True:
        frames = [video.read()[1] for video in videos]
        num_none = 0
        for idx, frame in enumerate(frames):
            if frame is None: 
                frames[idx] = prev_frames[idx]
                num_none += 1
            else:
                prev_frames[idx] = frame
        if num_none == len(videos): break

        input_heights = [frame.shape[0] for frame in frames if frame is not None]
        input_widths = [frame.shape[1] for frame in frames if frame is not None]
        input_channels = [frame.shape[2] for frame in frames if frame is not None]

        out_height = min(input_heights)
        out_width = sum(input_widths)
        out_channel = input_channels[0]
    
        if out is None:
            out = cv2.VideoWriter(output_path, fourcc, 10.0, (out_width, out_height))
        if False:
            out_frame = np.zeros([out_height, out_width, out_channel]).astype('uint8')
            offset = 0
            for frame in frames:
                out_frame[:,offset:offset+frame.shape[1],:] = frame
                offset = offset + frame.shape[1]
        else:
            try:
                out_frame = np.stack(frames, 1).reshape([out_height,out_width,out_channel])
            except:
                import pdb; pdb.set_trace()
                pass
        out.write(out_frame)
    
    out.release()



if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: {} video1_path video2_path [video3_path] ... [videon_path] out_path'.format(sys.argv[0]))
        print('Usage: {} video1_dir video2_dir [video3_dir] ... [videon_path] out_dir'.format(sys.argv[0]))
        exit()

    if sys.argv[1].endswith('.mp4'):
        video_paths = sys.argv[1:-1]
        output_path = sys.argv[-1]
        merge_many_mp4(video_paths, output_path)
        print('save {}'.format(output_path))
    else:
        video_dirs = sys.argv[1:-1]
        output_dir = sys.argv[-1]
        if not os.path.exists(output_dir):
            os.system('mkdir -p {}'.format(output_dir))
        video_names = [fname for fname in os.listdir(video_dirs[0]) if fname.endswith('.mp4')]
        for video_name in video_names:
            video_paths = [os.path.join(video_dir, video_name) for video_dir in video_dirs]
            output_path = os.path.join(output_dir, video_name)
            if os.path.exists(output_path):
                print('{} exist'.format(output_path))
                continue

            stop = False
            for video_path in video_paths:
                if not os.path.exists(video_path):
                    stop = True
                    continue
            if stop: continue

            merge_many_mp4(video_paths, output_path)
            print('save {}'.format(output_path))
