
import tempfile
import random
import string
import os
import json
import wget
import subprocess
import getpass
import shutil

def create_manifest():
    info = get_json_info()

    USER = getpass.getuser()
    mods_mine_path = r'C:\Users\{}\AppData\Roaming\.minecraft'.format(USER)
    manifest_path = os.path.join(mods_mine_path, "_hylauncher_manifest.json")

    json_object = json.dumps(info, indent=4) 

    with open(manifest_path, 'w') as outfile:
        outfile.write(json_object)
    

def get_json():
    json_path = os.path.join(os.getcwd(), "app", "utils", "download_info.json")
    if os.path.exists(json_path):
        os.remove(json_path)
    url=r'https://raw.githubusercontent.com/HyLauncher/HyLauncherDeps/main/download_info.json'
    out_path = os.path.join(os.getcwd(), "app", "utils")
    wget.download(url, out=out_path)
    create_manifest()

def get_json_info():
    json_path = os.path.join(os.getcwd(), "app", "utils", "download_info.json")
    j = open(json_path)
    data = json.load(j) 
    return data

def get_deps():
    get_json()
    info = get_json_info()

    encode = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    temp_dir = os.path.join(tempfile.gettempdir(), encode)

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    url=info.get('downlaod_path')
    wget.download(url, out=temp_dir)
    prepare_mods(temp_dir)

def prepare_mods(temp_dir):
    print(f'\nExtracting mod zip to {temp_dir}')
    mods_path = os.path.join(temp_dir, "Mods.zip")
    USER = getpass.getuser()
    mods_mine_path = r'C:\Users\{}\AppData\Roaming\.minecraft\mods'.format(USER)
    zip_ext_command = f'tar -zxvf {mods_path} -C {mods_mine_path}'
    subprocess.call(zip_ext_command)
    print('All mods extracted perfectly!')
    clean_temp_dir(temp_dir)

def clean_temp_dir(temp_dir):
    print(f'\nCleaning dir: {temp_dir}')
    shutil.rmtree(temp_dir)
    print('Cleaned!')

def get_hyjson_info():

    USER = getpass.getuser()
    mods_mine_path = r'C:\Users\{}\AppData\Roaming\.minecraft'.format(USER)
    manifest_path = os.path.join(mods_mine_path, "_hylauncher_manifest.json")
    j = open(manifest_path)
    data = json.load(j) 
    return data

def get_resouce_pack():
    get_json()
    
    USER = getpass.getuser()
    rp_mine_path = r'C:\Users\{}\AppData\Roaming\.minecraft\resourcepacks'.format(USER)

    mods_mine_path = r'C:\Users\{}\AppData\Roaming\.minecraft'.format(USER)
    manifest_path = os.path.join(mods_mine_path, "_hylauncher_manifest.json")

    hyinfo = get_hyjson_info()
    info = get_json_info()

    rp_list = os.listdir(rp_mine_path)

    if rp_list == []:
        hyinfo['updated'] = "NOT"
        
    else:
        hyinfo['updated'] = "YES"



    if hyinfo.get('updated') != 'YES':
        if hyinfo.get('rp_version') != info.get('resource_pack_version'):
            url=info.get('resource_pack_path')
            wget.download(url, out=rp_mine_path)
            hyinfo['updated'] = "YES"

    hyinfo['rp_version'] = info.get('resource_pack_version')

    json_object = json.dumps(hyinfo, indent=4) 

    with open(manifest_path, 'w') as outfile:
        outfile.write(json_object)

    print('Lagunaak resource pack installed!')

        