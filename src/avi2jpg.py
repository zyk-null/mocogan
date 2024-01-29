import os
import cv2
import torch
from torchvision import transforms

def extract_frames_and_save_as_jpg(input_folder, output_folder, num_frames=64, target_size=(64, 64)):
    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    # 定义转换
    preprocess = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize(target_size),
        transforms.ToTensor()
    ])

    # 遍历文件夹内所有avi文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".avi"):
            video_path = os.path.join(input_folder, filename)

            # 使用OpenCV读取视频
            cap = cv2.VideoCapture(video_path)

            # 初始化张量列表
            frames_tensor_list = []

            # 获取视频总帧数和帧率
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)

            # 计算每隔多少帧采样一次，以确保总共采样 num_frames 帧
            sampling_interval = max(total_frames // num_frames, 1)

            for i in range(0, total_frames, sampling_interval):
                # 设置帧位置
                cap.set(cv2.CAP_PROP_POS_FRAMES, i)

                # 读取视频帧
                ret, frame = cap.read()

                if not ret:
                    break

                # 调整大小并转换为PyTorch张量
                tensor_image = preprocess(frame)

                # 添加到张量列表
                frames_tensor_list.append(tensor_image)

            # 关闭视频流
            cap.release()

            # 水平拼接所有张量
            result_tensor = torch.cat(frames_tensor_list, dim=2)

            # 构造输出文件路径
            output_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.jpg")

            # 将结果张量保存为图像文件
            transforms.ToPILImage()(result_tensor).save(output_file)


if __name__ == "__main__":
    # 输入文件夹路径（包含avi文件）
    input_folder_path = "../data/TaiChi/0"

    # 输出图像文件路径
    output_image_path = "../data/TaiChi-img/0"

    # 调用函数进行处理
    extract_frames_and_save_as_jpg(input_folder_path, output_image_path)
