"""Utility functions module"""
import hashlib
import json


def save_file(filename: str, filedata: bin) -> str:
    """Save file to disk"""
    fpath = f"app/tmp/{filename}"
    if isinstance(filedata, str):
        filedata = filedata.encode('utf-8')
    with open(fpath, 'wb') as f:
        f.write(filedata)
        with open(f"app/tmp/{filename}.md5", "wb") as f:
            hashmd5 = hashlib.md5(filedata).hexdigest()
            f.write(hashmd5.encode())
    return fpath


def load_json(path: str) -> dict:
    """Loads json file and returns as a dictionary"""
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def process_config(fpath: str) -> dict:
    """Process configuration file"""
    conf = load_json(fpath)
    filtered_confs = {}
    cluster_confs = {
        'atena02': ['instance_type', 'image_name', 'account'],
        'dev': ['instance_type', 'image_name', 'account']
    }
    target_cluster = conf['runner_location']
    general_confs = ['runner_location', 'dataset_name',
                     'train_script_name', 'experiment_name']

    for param in general_confs:
        filtered_confs[param] = conf[param]

    for param in cluster_confs[target_cluster]:
        cluster_param = conf['clusters'][target_cluster]['infra_config'][param]
        filtered_confs[param] = cluster_param
    return filtered_confs
