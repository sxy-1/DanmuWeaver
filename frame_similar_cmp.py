import ctypes
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import cv2
import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import hamming
from switch import switch
from tqdm import tqdm
from tkinter import Tk, filedialog, ttk, Label, Button, messagebox


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
    if not video.isOpened():
        print("Failed to open video")
        return []

    fps = video.get(cv2.CAP_PROP_FPS)
    num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT)) / fps
    print(name, "Total frames:", num_frames, "FPS:", fps)

    with tqdm(total=num_frames, desc=f"Processing frames for {name}", disable=not show_progress) as pbar:
        last_processed_time = -frame_interval * 1000  # 初始化为负值，以确保处理第一帧
        current_time = -1
        while True:
            # # if current_time == video.get(cv2.CAP_PROP_POS_MSEC):
            # #     break
            current_time = video.get(cv2.CAP_PROP_POS_MSEC)
            # print(current_time)
            # 每隔 frame_interval 秒处理一帧
            if current_time >= last_processed_time + frame_interval * 1000:
                retval, frame = video.read()  # 读取并解码当前帧
                if not retval:
                    break

                last_processed_time = current_time // 1000 * 1000
                # print(name, "Current time:", current_time, "is being phashed")
                phash = pHash(frame)  # 假设 pHash 函数已经定义
                sequence.append(phash)
                pbar.update(1)  # 更新进度条
            else:
                video.grab()  # 跳过当前帧，避免解码不需要的帧
                if video.get(cv2.CAP_PROP_POS_MSEC) == 0:
                    print("shit")
                    break
    print(name,"seq finished")
    return sequence  # 少2秒保证稳定性


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





def compare_video(src_video, dst_video,frame_interval=1):
    video1 = cv2.VideoCapture(src_video)
    video2 = cv2.VideoCapture(dst_video)

    with ThreadPoolExecutor() as executor:
        future1 = executor.submit(get_phash_sequence, video1, frame_interval, "short", show_progress=True)
        future2 = executor.submit(get_phash_sequence, video2, frame_interval, "long", show_progress=True)

        sequence1 = future1.result()
        sequence2 = future2.result()

        print("sequence1.len:",len(sequence1))
        print("sequence2.len:",len(sequence2))


    # print("cao")
    distance, path = fastdtw(sequence1, sequence2, dist=hamming)

    # print(path)
    # # 可视化对齐路径
    # plt.imshow(np.array(path)[:, ::-1].T, origin='lower', cmap=plt.cm.gray, interpolation='nearest')
    # plt.show()

    # 返回归一化的距离
    # return distance / len(path)
    return path



globaldir = None

label_input_video_text = ""
label_output_video_text = ""
label_input_ass_path_text = ""
def get_video_path():
    # global globaldir
    root = Tk()
    root.withdraw()  # 隐藏主窗口
    video_path = filedialog.askopenfilename(title="选择视频文件", filetypes=[("视频文件", "*.mp4")])
    # globaldir = os.path.dirname(video_path)
    return video_path

def get_ass_path():
    # global globaldir
    root = Tk()
    # 调用api设置成由应用程序缩放
    # ctypes.windll.shcore.SetProcessDpiAwareness(1)
    # # 调用api获得当前的缩放因子
    # ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
    # # 设置缩放因子
    # root.tk.call('tk', 'scaling', ScaleFactor / 75)
    root.withdraw()  # 隐藏主窗口
    ass_path = filedialog.askopenfilename(title="选择字幕文件", filetypes=[("字幕文件", "*.ass")])
    # globaldir = os.path.dirname(ass_path)
    return ass_path


def tk_window():
    # 添加tkinter窗口
    root = Tk()
    root.title("文件选择面板")




    # 标签用于显示选择的路径
    label_input_video_path = Label(root, text="Input Video Path: ")
    label_output_video_path = Label(root, text="Output Video Path: ")
    label_input_ass_path = Label(root, text="Input Ass Path: ")

    # 函数用于更新标签文本
    def update_labels():
        global  label_input_video_text
        global  label_output_video_text
        global  label_input_ass_path_text
        label_input_video_text  = input_video_path.get()
        label_output_video_text=output_video_path.get()
        label_input_ass_path_text= input_ass_path.get()

    # 选择文件路径的输入框
    input_video_path = ttk.Entry(root)
    output_video_path = ttk.Entry(root)
    input_ass_path = ttk.Entry(root)



    # 选择文件路径的按钮
    button_input_video_path = Button(root, text="选择视频文件", command=lambda: input_video_path.insert(0, get_video_path()))
    button_output_video_path = Button(root, text="选择输出视频文件", command=lambda: output_video_path.insert(0, get_video_path()))
    button_input_ass_path = Button(root, text="选择字幕文件", command=lambda: input_ass_path.insert(0, get_ass_path()))

    # 确定按钮，点击后执行main函数
    button_confirm = Button(root, text="确定", command=lambda: [update_labels(), run_main(label_input_video_text,label_output_video_text,label_input_ass_path_text), root.destroy() ])

    # 布局
    label_input_video_path.grid(row=0, column=0, sticky="w", pady=5)
    input_video_path.grid(row=0, column=1, columnspan=2, pady=5)
    button_input_video_path.grid(row=0, column=3, pady=5)

    label_output_video_path.grid(row=1, column=0, sticky="w", pady=5)
    output_video_path.grid(row=1, column=1, columnspan=2, pady=5)
    button_output_video_path.grid(row=1, column=3, pady=5)

    label_input_ass_path.grid(row=2, column=0, sticky="w", pady=5)
    input_ass_path.grid(row=2, column=1, columnspan=2, pady=5)
    button_input_ass_path.grid(row=2, column=3, pady=5)

    button_confirm.grid(row=3, column=0, columnspan=4, pady=10)

    root.mainloop()



def run_main(input_video_path, output_video_path,input_ass_path):
    print("cao")
    video_file_name = os.path.basename(output_video_path)
    output_file_name_without_extension, output_file_name_extension = os.path.splitext(video_file_name)
    output_ass_path = os.path.join(os.path.dirname(input_ass_path), output_file_name_without_extension + ".ass")
    print(input_video_path, output_video_path, input_ass_path,output_ass_path)
    # time.sleep(10)
    path = compare_video(input_video_path, output_video_path,frame_interval=1)
    print(path)
    switch(input_ass_path, output_ass_path, path)
    print("over")
    messagebox.showinfo("完成", "处理完成！")

tk_window()
