import os
import shutil

def static_to_public():
    if not os.path.exists('static'):
        raise Exception('Static directory does not exist')

    if os.path.exists('public'):
        print('Public already exists. Removing...')
        shutil.rmtree('public')

    shutil.copytree('static', 'public')
