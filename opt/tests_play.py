# pylint: disable=no-member
# pylint: disable=import-outside-toplevel
import pathlib as pl

# Setup
from SMIT.application import Application
app = Application(True)
################################################
# pylint: disable=no-member 
# folders = [] 
# for folder, folder_path in app.Folder.items():
#     print(f'Folder: {folder}')
#     print(f'Folder Path: {folder_path}')
    
# for folder_path in app.Folder.values():
#     print(folder_path)
# modules = app._load_modules()
# for key, value in modules.items():
#     print(f'Key: {key} - Value: {value}')

print(app.rsa._load_rsa_keys().public_key)