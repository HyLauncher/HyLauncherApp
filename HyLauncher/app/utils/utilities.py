import os
import zipfile
import get_deps as gd

def apply_resources(mine_path):

    gd.get_resouce_pack()

    resouce_path = 'resourcePacks:["vanilla","mod_resources","programer_art","file/Lagunaak_Resource_Pack.zip"]'

    op_path = f'{mine_path}\options.txt'
    try:
        with open(op_path) as f:
            for line in f.readlines():
                if 'resourcePacks:' in line:
                    if line == resouce_path:
                        return True
                    else:
                        replacetext(op_path, line)
    except:
        return None

def replacetext(op_path, search_text):
    resouce_path = 'resourcePacks:["vanilla","mod_resources","programer_art","file/Lagunaak_Resource_Pack.zip"]\n'

    with open(op_path, 'r') as file:
        data = file.read()
        data = data.replace(search_text, resouce_path)

    with open(op_path, 'w') as file:
        file.write(data)
    return "Text replaced"
  

def get_command(good_version, username, server):
    version = get_version(good_version)
    minecraft_command = f'portablemc start forge:{version} -u {username} -s {server}'

    return minecraft_command

def get_version(good_version):
    # versions_path = os.path.join(mine_path, 'versions')
    # vers = os.listdir(versions_path)
    # local_versions = []
    
    # for v in vers:
    #     id = v
    #     if good_version in id:
    #         local_versions.append(id)
    #     else:
    #         continue
    # if len(local_versions) > 0:
    #     return local_versions[0]
    # else:
    #     return download_version(good_version)
    return good_version


def check_version(mine_path, good_version):
    versions_path = os.path.join(mine_path, 'versions')
    try:
        vers = os.listdir(versions_path)
        for v in vers:
            if good_version.replace('-40.1.0', '') in v:
                return True
    except:
        return False

def download_deault_version(mine_path, CURRENT_PATH ):
    if not os.path.exists(mine_path):
        os.mkdir(mine_path)
    
    zip_path = os.path.join(CURRENT_PATH, 'bin', 'versions', 'minecraft.zip')

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(mine_path)

