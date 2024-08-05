import asyncio
from typing import NoReturn

import cv2
import numpy as np
import torch

from video.camera import Camera
from menovideo.menovideo import DeVTr
import multiprocessing


def check_deviant(
        data: torch.Tensor,
        running_model: torch.nn.Module
) -> None:
    with torch.no_grad():
        print(running_model(data).item())


def run_checking(
        data: torch.Tensor,
        model: torch.nn.Module
) -> multiprocessing.Process:
    return multiprocessing.Process(
        target=check_deviant,
        args=(
            data,
            model
        )
    )


async def run_deviant_check_loop(
        camera: Camera
) -> NoReturn:
    model = DeVTr(w="default", base='default')
    model.to("cpu")
    model.eval()
    process: multiprocessing.Process | None = None

    with camera:
        HEIGHT, WIDTH = 200, 200
        RGB = 3
        TIME_STEP = 40

        frames_buffer = np.zeros((1, TIME_STEP, RGB, HEIGHT, WIDTH), dtype=np.float32)
        current_frame_id = 0
        print("Start loop")
        while True:
            if process is not None and process.is_alive():
                await asyncio.sleep(0.01)
                continue

            ret, frame = camera.get_frame()
            if ret:
                frame = cv2.resize(frame, (HEIGHT, WIDTH))
                frames_buffer[0][current_frame_id] = frame.reshape((RGB, HEIGHT, WIDTH))
                current_frame_id += 1
                if current_frame_id >= TIME_STEP:
                    print("Start process")
                    if process is not None:
                        print(process, process.is_alive())
                    process = run_checking(
                        torch.from_numpy(frames_buffer),
                        model
                    )
                    process.start()
                    print("Process started")
                    current_frame_id = 0
                    frames_buffer = np.zeros((1, TIME_STEP, RGB, HEIGHT, WIDTH), dtype=np.float32)

            await asyncio.sleep(0.01)
