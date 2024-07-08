"""
Reads clips from youtube. Saves the clip, a trimmed version of the clip between specified times, the frames of the
trimmed clip and the clip's frame rate.
"""
import os
import pickle as pkl

from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from pytube import YouTube

from common.constants import CLIPS_URLS_DICT, DATA_DIR


def download_clip(url: str, output_path: str, file_name: str) -> None:
    """
    Download the highest resolution clip from a given youtube url
    :param url:
    :param output_path:
    :param file_name:
    :return:
    """
    yt = YouTube(url)
    yt = yt.streams.get_highest_resolution()
    yt.download(output_path=output_path, filename=file_name)


def trim_and_get_frames(path: str, clip_name: str, start_time: int, end_time: int) -> int:
    """
    Trims a video clip to a specified duration and extracts frames from the trimmed clip.

    This function first trims the original video clip to the specified start and end times,
    then extracts and saves the frames of the trimmed clip to a designated directory.
    The frames are saved in a sequence with filenames indicating their order.

    Parameters:
    - path (str): The directory path where the original clip is located and where the trimmed clip will be saved.
    - clip_name (str): The filename of the original clip.
    - start_time (int): The start time in seconds from which the clip will be trimmed.
    - end_time (int): The end time in seconds to which the clip will be trimmed.

    Returns:
    - int: The frames per second (fps) of the trimmed clip, which can be useful for further processing or analysis.
    """

    input_path = os.path.join(path, clip_name)
    output_path = os.path.join(path, f"trimmed_{clip_name}")
    ffmpeg_extract_subclip(input_path, start_time, end_time, targetname=output_path)
    clip = VideoFileClip(output_path)
    clip.write_images_sequence(
        f"{path}/{clip_name.split('.')[0]}/frames/{clip_name.split('.')[0]}_frame%04d.jpg", fps=clip.fps
    )
    return clip.fps


def main() -> None:
    clips_fps_dict = {}
    for i, url in enumerate(CLIPS_URLS_DICT.keys()):
        clip_name = f"clip_{i}.mp4"
        download_clip(url, DATA_DIR, clip_name)
        os.makedirs(os.path.join(DATA_DIR, f"clip_{i}", "frames"), exist_ok=True)
        clips_fps_dict[i] = trim_and_get_frames(
            path=DATA_DIR, clip_name=clip_name, start_time=CLIPS_URLS_DICT[url][0], end_time=CLIPS_URLS_DICT[url][1]
        )

    with open(os.path.join(DATA_DIR, "clips_fps_dict.pkl"), "wb") as f:
        pkl.dump(clips_fps_dict, f)


if __name__ == "__main__":
    main()
