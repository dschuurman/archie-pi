#!/usr/bin/python3
# Friendly script to remove a module from the
# ARCHIE Pi (Another Remote Community Hotspot for Instruction and Education).
#
# (C) 2023 faculty and students from Calvin University
#
# License: GNU General Public License (GPL) v3
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import sys
import os
import psutil
import subprocess
import xmltodict

# map of directories and corresponding module names
DIRS_NAMES = { 'en-blockly-games':'Blockly)', 'es-blockly-games':'Blockly (Spanish)', 'en-ck12':'CK-12', 'en-boundless-static':'Boundless', 
            'en-mustardseedbooks':'Mustard Seed Books', 'f':'Project Gutenberg', 'en-worldmap-10':'World Map', 'en-openstax':'openstax Textbooks', 
            'en-rpi_guide':'Rasp Pi User Guide', 'en-scratch':'Scratch', 'en-kaos':'Khan Academy (English)', 'es-kaos':'Khan Academy (Spanish)',
            'en-wikipedia_for_schools-static':'Wikipedia for schools', 'en-wikipedia':'Wikipedia (English)', 'es-wikipedia':'Wikipedia (Spanish)', 'fr-wikipedia':'Wikipedia (French)', 
            'en-wiktionary':'Wiktionary (English)', 'es-wiktionary':'Wiktionary (Spanish)', 'fr-wiktionary':'Wiktionary (French)', 
            'en-vikidia':'Vikidia (English)', 'es-vikidia':'Vikidia (Spanish)', 'fr-vikidia':'Vikidia (French)', 'en-kuyers-cer':'Kuyers Christian Ed Resources',
            'en-wikivoyage':'Wikivoyage (English)', 'es-wikivoyage':'Wikivoyage (Spanish)', 'fr-wikivoyage':'Wikivoyage (French)',
            'en-phet':'PhET Simulations (English)', 'es-phet':'PhET Simulations (Spanish)', 'fr-phet':'PhET Simulations (French)',
            'en-science-made-easy':'Science Made Easy videos' }

# Set home folder location (username may be different than the default pi)
HOME = f'/home/{os.getlogin()}'

# Helper functions
def do(cmd):
    ''' Execute system command and return result
    '''
    result = subprocess.run(cmd.split(), stderr=sys.stderr, stdout=sys.stdout)
    return (result.returncode == 0)

def get_dir_size(path):
    ''' Return the size of a directory
    '''
    size = subprocess.check_output(['du','-sh', path]).split()[0].decode('utf-8')
    return size

def get_zim_id(zim_file):
    ''' Return the ZIM ID for an installed ZIM module
    '''
    with open(f'{HOME}/kiwix/library_zim.xml', 'rb') as file:
        zim_dict = xmltodict.parse(file)

    for item in zim_dict['library']['book']:
        if zim_file in item['@path']:
            return item['@id']
    return None

# Display all installed modules

print('\nSearching for all installed modules (this will take a few moments)...')
print('Installed modules:')
counter = 0
installed_modules = {}
with os.scandir('/var/www/modules/') as modules:
    for module in modules:
        if module.is_dir():
            counter += 1
            filepath = f'/var/www/modules/{module.name}'
            # Skip unrecognized modules
            if DIRS_NAMES.get(module.name) == None:
                print(f'{counter}: {module.name} ({get_dir_size(filepath)})')
            else:
                print(f'{counter}: {DIRS_NAMES[module.name]} ({get_dir_size(filepath)})')
            installed_modules[counter] = module.name

selection = input("\nEnter the number of the module you wish to remove (enter 'q' to quit): ")
if selection == '':
    print('No module selected... Done')
    sys.exit(0)
elif selection == 'q':
    print('Exiting...')
    sys.exit(0)

# Store module directory name corresponing to selection
module_dir = installed_modules[int(selection)]

# Temporarily mount root partion in read-write mode for removing content
do('mount -o remount,rw /')

# check for Kixix modules first since they require a special kiwix_mange step
if module_dir in ['en-wikipedia','es-wikipedia','fr-wikipedia','en-wiktionary','es-wiktionary','fr-wiktionary',
                  'en-vikidia','es-vikidia','fr-vikidia','en-wikivoyage','es-wikivoyage','fr-wikivoyage','en-phet','es-phet','fr-phet']:
    print(f'Removing {DIRS_NAMES[module_dir]}...')
    zimpath = f'/var/www/modules/{module_dir}'
    id = get_zim_id(zimpath)
    do(f'{HOME}/kiwix/kiwix-manage {HOME}/kiwix/library_zim.xml remove {id}')
    do(f'rm -rf /var/www/modules/{module_dir}')

# Otherwise, if this is not a Kiwix module, simply delete the corresponding folder
else:
    print(f'Removing /var/www/modules/{module_dir}...')
    do(f'rm -rf /var/www/modules/{module_dir}') or sys.exit('Error moving content')
    print('Done')

# Once content is installed and configured, return root partion to read-only mode
do('mount -o remount,ro /')

print(f"\nDONE! ({(psutil.disk_usage('/').free)//(2**30)}GB free).")
print('** Each content module is subject to its own license terms and conditions.')
print('** Note that a reboot may be required.')
print("** To reboot, type 'sudo reboot' at the command-line.")
