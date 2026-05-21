from VAREID.drivers.lca_driver import get_inputs as get_lca_inputs
from VAREID.drivers.lca_driver import get_outputs as get_lca_outputs
from VAREID.drivers.mid_driver import get_inputs as get_mid_inputs
from VAREID.drivers.si_driver import get_inputs as get_si_inputs
from VAREID.libraries.io.workflow_funcs import build_config, generate_targets, encode_config

configfile: "config.yaml"

config = build_config(config)
config_str = encode_config(config)


rule all:
    input:
        generate_targets(config)


rule import_videos:
    input:
        directory(config["data_dir_in"])
    output:
        config["video_out_path"]
    shell:
        "python -m VAREID.drivers.import_video_driver --config {config_str}"


rule detect_videos:
    input:
        config["video_out_path"]
    output:
        config["dt_video_out_path"]
    shell:
        "python -m VAREID.drivers.dt_video_driver --config {config_str}"


rule species_identification:
    input:
        *get_si_inputs(config)
    output:
        config["si_out_path"]
    shell:
        "python -m VAREID.drivers.si_driver --config {config_str}"


rule viewpoint_classification:
    input:
        config["si_out_path"]
    output:
        config["vc_out_path"]
    shell:
        "python -m VAREID.drivers.vc_driver --config {config_str}"


rule ia_classification:
    input:
        config["vc_out_path"]
    output:
        config["ia_out_path"]
    shell:
        "python -m VAREID.drivers.iac_driver --config {config_str}"


rule ia_filtering:
    input:
        config["ia_out_path"]
    output:
        config["ia_filtered_out_path"]
    shell:
        "python -m VAREID.drivers.iaf_driver --config {config_str}"


rule frame_sampling:
    input:
        config["ia_filtered_out_path"]
    output:
        config["fs_out_path"]
    shell:
        "python -m VAREID.drivers.fs_driver --config {config_str}"


rule miew_id:
    input:
        *get_mid_inputs(config)
    output:
        config["mid_out_path"]
    shell:
        "python -m VAREID.drivers.mid_driver --config {config_str}"


rule lca:
    input:
        *get_lca_inputs(config)
    output:
        *get_lca_outputs(config)
    shell:
        "python -m VAREID.drivers.lca_driver --config {config_str}"
