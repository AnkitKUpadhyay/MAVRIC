"""Workflow configuration helpers for the video pipeline."""

import base64
import json
import os


def decode_config(code):
    encoded_bytes = code.encode("utf-8")
    decoded_bytes = base64.b64decode(encoded_bytes)
    decoded_str = decoded_bytes.decode("utf-8")

    return json.loads(decoded_str)


def encode_config(config):
    config_str = json.dumps(config)
    original_bytes = config_str.encode("utf-8")
    encoded_bytes = base64.b64encode(original_bytes)

    return encoded_bytes.decode("utf-8")


def generate_targets(config):
    targets = [
        config["video_out_path"],
        config["dt_video_out_path"],
        config["si_out_path"],
        config["vc_out_path"],
        config["ia_out_path"],
        config["ia_filtered_out_path"],
        config["fs_out_path"],
        config["mid_out_path"],
    ]

    if config["lca_separate_viewpoints"]:
        targets.extend([config["post_left_in_path"], config["post_right_in_path"]])
    else:
        targets.append(config["lca_out_path"])

    return targets


def build_config(config):
    model_dir = config["model_dirname"]
    out_dir = config["data_dir_out"]

    image_dir = os.path.join(out_dir, config["image_dirname"])
    log_dir = os.path.join(out_dir, config["log_dirname"])

    video_out_path = os.path.join(out_dir, config["video_out_file"])
    import_logs = os.path.join(log_dir, config["import_logfile"])

    dt_dir = os.path.join(out_dir, config["dt_dirname"])
    dt_model_path = os.path.join(model_dir, config["dt_model"])
    dt_video_out_path = os.path.join(dt_dir, config["dt_video_out_file"])
    dt_logs = os.path.join(log_dir, config["dt_logfile"])

    si_dir = os.path.join(out_dir, config["si_dirname"])
    si_out_path = os.path.join(si_dir, config["si_out_file"])
    si_logs = os.path.join(log_dir, config["si_logfile"])

    vc_dir = os.path.join(out_dir, config["vc_dirname"])
    vc_model_path = os.path.join(model_dir, config["vc_model"])
    vc_out_path = os.path.join(vc_dir, config["vc_out_file"])
    vc_logs = os.path.join(log_dir, config["vc_logfile"])

    ia_dir = os.path.join(out_dir, config["ia_dirname"])
    ia_model_path = os.path.join(model_dir, config["ia_model"])
    ia_out_path = os.path.join(ia_dir, config["ia_out_file"])
    ia_filtered_out_path = os.path.join(ia_dir, config["ia_filtered_out_file"])
    ia_logs = os.path.join(log_dir, config["ia_logfile"])

    fs_dir = os.path.join(out_dir, config["fs_dirname"])
    fs_out_path = os.path.join(fs_dir, config["fs_out_file"])
    fs_logs = os.path.join(log_dir, config["fs_logfile"])
    fs_stage1_out_path = os.path.join(fs_dir, config["fs_stage1_out_file"]) if config["fs_stage1_out_file"] is not None else None

    mid_dir = os.path.join(out_dir, config["mid_dirname"])
    mid_out_path = os.path.join(mid_dir, config["mid_out_file"])
    mid_logs = os.path.join(log_dir, config["mid_logfile"])

    lca_dir = os.path.join(out_dir, config["lca_dirname"])
    lca_verifiers_probs_path = os.path.join(model_dir, config["lca_verifiers_probs"])
    lca_subunit_logs = os.path.join(log_dir, config["lca_subunit_logfile"])
    lca_logs = os.path.join(log_dir, config["lca_logfile"])

    post_left_in_path = os.path.join(lca_dir, f'{config["lca_out_prefix"]}_left_{config["lca_out_suffix"]}.json')
    post_right_in_path = os.path.join(lca_dir, f'{config["lca_out_prefix"]}_right_{config["lca_out_suffix"]}.json')
    lca_out_path = os.path.join(lca_dir, f'{config["lca_out_prefix"]}_{config["lca_out_suffix"]}.json')

    post_dir = os.path.join(out_dir, config["post_dirname"])
    post_db_path = os.path.join(post_dir, config["post_db_file"])
    post_left_out_path = os.path.join(post_dir, config["post_left_out_file"])
    post_right_out_path = os.path.join(post_dir, config["post_right_out_file"])
    post_logs = os.path.join(log_dir, config["post_logfile"])
    gui_logs = os.path.join(log_dir, config["gui_logfile"])

    config.update({
        "data_video": True,
        "image_dir": image_dir,
        "log_dir": log_dir,
        "video_out_path": video_out_path,
        "import_logs": import_logs,
        "dt_dir": dt_dir,
        "dt_model_path": dt_model_path,
        "dt_video_out_path": dt_video_out_path,
        "dt_logs": dt_logs,
        "si_dir": si_dir,
        "si_out_path": si_out_path,
        "si_logs": si_logs,
        "vc_dir": vc_dir,
        "vc_model_path": vc_model_path,
        "vc_out_path": vc_out_path,
        "vc_logs": vc_logs,
        "ia_dir": ia_dir,
        "ia_model_path": ia_model_path,
        "ia_out_path": ia_out_path,
        "ia_filtered_out_path": ia_filtered_out_path,
        "ia_logs": ia_logs,
        "fs_dir": fs_dir,
        "fs_out_path": fs_out_path,
        "fs_logs": fs_logs,
        "fs_stage1_out_path": fs_stage1_out_path,
        "mid_dir": mid_dir,
        "mid_out_path": mid_out_path,
        "mid_logs": mid_logs,
        "lca_dir": lca_dir,
        "lca_verifiers_probs_path": lca_verifiers_probs_path,
        "post_left_in_path": post_left_in_path,
        "post_right_in_path": post_right_in_path,
        "lca_subunit_logs": lca_subunit_logs,
        "lca_logs": lca_logs,
        "lca_out_path": lca_out_path,
        "post_dir": post_dir,
        "post_db_path": post_db_path,
        "post_left_out_path": post_left_out_path,
        "post_right_out_path": post_right_out_path,
        "post_logs": post_logs,
        "gui_logs": gui_logs,
    })

    return config
