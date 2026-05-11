#!/usr/bin/python3
# Friendly script to install Open Enducation Resources (OER) for the 
# ARCHIE Pi project (Another Remote Community Hotspot for Instruction and Education).
# This script installs modules from various open education resources
# which are subject to their own license terms and conditions.
#
# (C) 2020-2023 faculty and students from Calvin University
#
# License: GNU General Public License (GPL) v3
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import sys
import curses
from curses import wrapper
import os
import psutil
import subprocess
import tomllib

# Helper functions
def do(cmd):
    ''' Execute system command and return result
    '''
    result = subprocess.run(cmd.split(), stderr=sys.stderr, stdout=sys.stdout)
    return (result.returncode == 0)

def append_file(file, line):
    ''' Append a line to a given file
    '''
    try:
        f = open(file, 'a')
        f.write(line + '\n')
        f.close()
    except:
        return False
    return True

def get_latest_kiwix_filename(filename_prefix, url):
    ''' Kiwix zim files are constantly being updated to more recent versions.
        This function determines the latest zim filename for a given zim filename prefix.
        Zim filenames are assumed to end with a date in the form YYYY-MM-DD
    '''
    cmd = f'lynx -dump -listonly -nonumbers {url}'
    result = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
    files = result.stdout.decode('utf-8')
    files_list = files.split('\n')
    matching_filenames = []   # list of matching filenames
    for file in files_list:
        if filename_prefix in file:
            matching_filenames.append(file)
    matching_filenames.sort()
    return matching_filenames[-1]  # return the most recent file


def main(screen):
    ''' module installer main function
    '''

    # collection of available modules and related information
    # OPTIONS = { 'a':'Algebra2Go (1.2GB)', 'b':'Blockly (English) (4.5MB)', 'c':'CK-12 (2.1GB)', 'd':'Boundless (3.5GB)', 'e':'Mustard Seed Books (39MB)', 
    #             'f':'Project Gutenberg (897MB)', 'g':'World Map (20GB)', 'h':'openstax Textbooks (2.9GB)', 'i':'Rasp Pi User Guide (6MB)', 
    #             'j':'Scratch (254MB)', 'k':'Khan Academy (English) (12GB)', 'l':'Khan Academy (Spanish) (8.7GB)',
    #             'm':'Wikipedia for schools (6.1GB)', 'n':'Wikipedia (English) (367MB)', 'o':'Wikipedia (Spanish) (187MB)', 'p':'Wikipedia (French) (1.5GB)', 
    #             'q':'Wiktionary (English) (48MB)', 'r':'Wiktionary (Spanish) (658MB)', 's':'Wiktionary (French) (1.5GB)', 
    #             't':'Vikidia (English) (47MB)', 'u':'Vikidia (Spanish) (47MB)', 'v':'Vikidia (French) (712MB)', 'w':'Kuyers Christian Ed Resources (44MB)',
    #             'x':'Wikivoyage (English) (761MB)', 'y':'Wikivoyage (Spanish) (94MB)', 'z':'Wikivoyage (French) (157MB)',
    #             'A':'PhET Simulations (English) (66MB)', 'B':'PhET Simulations (Spanish) (69MB)', 'C':'PhET Simulations (French) (68MB)',
    #             'S':'Science Made Easy videos (1.7GB)' }
    with open("modules.toml", "rb") as f:
        MODULES_INFO = tomllib.load(f)

    # root URL for Kiwix resources
    KIWIX_URL = 'http://download.kiwix.org/zim/'

    # Set home folder location (username may be different than the default pi)
    HOME = f'/home/{os.getlogin()}'

    selections: list[chr] = []
    try:
        while True:
            row = 1
            column = 5
            for key in MODULES_INFO.keys():

                # Highlight modules that are currently selected
                if key in selections:
                    screen.addstr(row, column, '{}) {}'.format(key,MODULES_INFO[key]["name"]), curses.A_BOLD|curses.A_REVERSE)
                else:
                    screen.addstr(row, column, '{}) {}'.format(key,MODULES_INFO[key]["name"]))
                # Alternate between left and right columns
                if column == 5:
                    column = 48
                else:
                    column = 5
                    row += 1

            screen.addstr(row+2, 5, f"Type the letter(s) for the module(s) you wish to install ({(psutil.disk_usage('/').free)//(2**30)}GB free).")
            screen.addstr(row+3, 5, 'To quit, press "ctrl-c", to begin installation, press ENTER')
            screen.refresh()
            
            c = chr(screen.getch())
            if ord(c)==10 or ord(c)==13:     # check for ENTER key
                break
            elif c in selections:            # unselect if key is already selected
                selections.remove(c)
                continue
            elif c in MODULES_INFO.keys():        # if key is recognized, add it to selections
                selections.append(c)
            else:                            # Beep if key is unrecognized
                curses.beep()
    except KeyboardInterrupt:                # quit gracefully if ctrl-c is pressed
        sys.exit(0)

    curses.endwin()
    if len(selections) == 0:
        print('No modules selected... Done')
        sys.exit(0)

    # List selected modules to install
    print('The following modules will be installed: ', end='')
    for selection in selections:
        print(MODULES_INFO[selection]["name"], end=', ')
    print('\b\b...\n')

    # Temporarily mount root partion in read-write mode for adding content
    do('mount -o remount,rw /')

    # Set current date and time
    do('timedatectl set-ntp true') or sys.exit('Error: cannot set date and time')

    # Install the selected modules from various open education resources
    for selection in selections:
        module_info = MODULES_INFO.get(selection)
        if module_info is None:
            print(f"Could not find module for selection {selection}")

        source_info = module_info.get("source_info")
        if source_info is None:
            print(f"Could not find source_info field for module {module_info['name']}")
        
        print(f'Installing {module_info["name"]}...')
        match(module_info["source"]):
            case "rachelmods":
                do(f'rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/{source_info["rachel_uri"]} /var/www/modules') or sys.exit('Error installing content')

            case "kiwix":
                do(f'mkdir /var/www/modules/{source_info["module_path"]}')
                kiwix_url = KIWIX_URL + source_info["kiwix_directory"]
                filename = get_latest_kiwix_filename(source_info["kiwix_filename_prefix"],kiwix_url)
                print(f'Downloading {filename}...')
                zim_path = f'/var/www/modules/{source_info["module_path"]}/{source_info["module_path"]}.zim'
                do(f'wget --no-check-certificate -nv --show-progress -O {zim_path} {filename}')
                do(f'{HOME}/kiwix/kiwix-manage {HOME}/kiwix/library_zim.xml add {zim_path}')
                html = f'<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/{source_info["module_path"]}">{module_info["name"]}</a></h2>\n</div>'
                append_file(f'/var/www/modules/{source_info["module_path"]}/index.htmlf', html)

            case "github":
                do(f'git clone --depth 1 https://github.com/{source_info["repo_host"]}/{source_info["repo_name"]}.git') or sys.exit('Error installing content')
                do(f'rm -rf {source_info["repo_name"]}/.git')
                do(f'mv {source_info["repo_name"]} /var/www/modules') or sys.exit('Error moving content')

            case _:
                print(f'Did not recognize module source {module_info["source"]} for module {module_info["name"]}')

        print('Done')

    # update ownership and permissions of modules
    print('Setting module folder permissions and ownerships (this may take a while)...')
    do('chown -R www-data.www-data /var/www/modules') or sys.exit('Error changing ownership of modules folder to www-data')
    do('chmod -R 755 /var/www/modules') or sys.exit('Error changing permissions of module files')

    # restart kiwix server
    do('pkill -SIGHUP kiwix-serve')   # restart kiwix server

    # Once content is installed and configured, return root partition to read-only mode
    do('mount -o remount,ro /')

    print(f"\nDONE! ({(psutil.disk_usage('/').free)//(2**30)}GB free).")
    print('** Each content module is subject to its own license terms and conditions.')
    print('** Note that a reboot is recommended.')
    print("** To reboot, type 'sudo reboot' at the command-line.")

# Use wrapper function to ensure original state of terminal is restored on exit
wrapper(main)
