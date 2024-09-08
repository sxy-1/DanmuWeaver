from concurrent.futures import ThreadPoolExecutor

import cv2
import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import hamming
from tkinter import Tk, filedialog
from switch import switch
from tqdm import tqdm


# 获取图片哈希值
def pHash(img):
    # 缩放图片为32x32灰度图片
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (32, 32), interpolation=cv2.INTER_CUBIC)

    # 创建二维列表
    h, w = img.shape[:2]
    vis0 = np.zeros((h, w), np.float32)
    vis0[:h, :w] = img

    # 二维Dct变换
    vis1 = cv2.dct(cv2.dct(vis0))
    vis1 = vis1[:8, :8]

    # 把二维list变成一维list
    img_list = vis1.flatten().tolist()

    # 计算均值, 得到哈希值
    avg = sum(img_list) * 1. / 64
    avg_list = [0 if i < avg else 1 for i in img_list]
    # print(img_list)
    return avg_list


def get_phash_sequence(video: cv2.VideoCapture, frame_interval: int, name: str, show_progress: bool = True) -> list:
    sequence = []
    i = -1
    fps = video.get(cv2.CAP_PROP_FPS)
    num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT)) / fps
    with tqdm(total=num_frames, desc=f"Processing frames for {name}", disable=not show_progress) as pbar:

        while True:
            i = i + 1
            # print(i)
            retval, frame = video.read()
            if not retval:
                break
            phash = pHash(frame)
            sequence.append(phash)
            pbar.update(1)  # 更新进度条
            # # 保存帧为图片
            # timestamp = i   # 计算时间戳，假设fps为每秒帧数
            # timestamp_min = int(timestamp / 60)  # 计算分钟
            # timestamp_sec = int(timestamp % 60)  # 计算秒钟
            # frame_number = i  # 帧编号从1开始
            #
            # save_path1 = "./frames_long/"
            # save_path2 = "./frames_long_del_60_90s/"
            # save_path3 = "./frames_short/"
            # os.makedirs(save_path1, exist_ok=True)
            # os.makedirs(save_path2, exist_ok=True)
            # os.makedirs(save_path3, exist_ok=True)
            #
            # # 保存图片
            # save_name = f"{frame_number}.jpg"
            # if name == "video1":
            #     cv2.imwrite(os.path.join(save_path2, save_name), frame)
            # elif name == "video2":
            #     cv2.imwrite(os.path.join(save_path1, save_name), frame)

            # 跳过指定帧数
            for _ in range((round(fps) * frame_interval) - 1):
                video.grab()
    return sequence


def compare_video(src_video, dst_video, frame_interval=1):
    video1 = cv2.VideoCapture(src_video)
    video2 = cv2.VideoCapture(dst_video)

    with ThreadPoolExecutor() as executor:
        future1 = executor.submit(get_phash_sequence, video1, frame_interval, "video1", show_progress=False)
        future2 = executor.submit(get_phash_sequence, video2, frame_interval, "video2", show_progress=True)

        sequence1 = future1.result()
        sequence2 = future2.result()

    # print("cao")
    distance, path = fastdtw(sequence1, sequence2, dist=hamming)

    # print(path)
    # # 可视化对齐路径
    # plt.imshow(np.array(path)[:, ::-1].T, origin='lower', cmap=plt.cm.gray, interpolation='nearest')
    # plt.show()

    # 返回归一化的距离
    # return distance / len(path)
    return path


input_ass_path = "D:\pyproject\movie\\res\\short.ass"
output_ass_path = "D:\pyproject\movie\\res\\long.ass"
input_video_path = "D:\pyproject\movie\\res\\short.mp4"
output_video_path = "D:\pyproject\movie\\res\\long.mp4"



path = compare_video(input_video_path, output_video_path, frame_interval=1)
switch(input_ass_path, output_ass_path, path)
