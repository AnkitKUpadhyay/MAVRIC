"""Video import convenience functions."""

import json
import os.path

from VAREID.libraries.io.video_funcs import add_videos, link_srts, update_timestamps


def _files_with_extensions(dir_in, extensions, recursive=True):
    matches = []
    extensions = tuple(f".{ext.lower().lstrip('.')}" for ext in extensions)

    if recursive:
        for root, _, files in os.walk(dir_in):
            for file_name in files:
                if file_name.lower().endswith(extensions):
                    matches.append(os.path.join(root, file_name))
    else:
        for file_name in os.listdir(dir_in):
            path = os.path.join(dir_in, file_name)
            if os.path.isfile(path) and file_name.lower().endswith(extensions):
                matches.append(path)

    return sorted(matches)


def import_video_folder(dir_in, dir_out, file_out, fps=8, max_frames=2000, recursive=True, doctest_mode=False):
    """Import videos recursively and write the pipeline video metadata JSON."""

    del doctest_mode

    path_out = os.path.join(dir_out, file_out)
    os.makedirs(dir_out, exist_ok=True)

    files = _files_with_extensions(dir_in, ["mp4", "avi"], recursive=recursive)
    srts = _files_with_extensions(dir_in, ["srt"], recursive=recursive)

    video_data = add_videos(dir_out, files, fps, max_frames)
    link_srts(video_data, srts)
    update_timestamps(video_data, fps)

    if video_data:
        with open(path_out, "w", encoding="utf-8") as json_file:
            json.dump(video_data, json_file, indent=4)
