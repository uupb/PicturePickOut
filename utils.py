import os
import json

config_file = 'config.json'


def load_last_selected_folder(folder_type='output'):
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config.get(f'{folder_type}_folder', '')
    return ''


def save_last_selected_folder(folder_path, folder_type='output'):
    config = {}
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)

    config[f'{folder_type}_folder'] = folder_path

    with open(config_file, 'w') as f:
        json.dump(config, f)
