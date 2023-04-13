#!/usr/bin/python3
# Friendly script to install Open Enducation Resources (OER) for the 
# ARCHIE Pi project (Another Remote Community Hotspot for Instruction and Education).
# This script installs modules from various open education resources
# which are subject to their own license terms and conditions.
#
# (C) 2020 faculty and students from Calvin University
#
# License: GNU General Public License (GPL) v3
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import sys
import curses
import os
import psutil
import subprocess

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

# collection of available modules
OPTIONS = { 'a':'Blockly', 'b':'Blockly (Spanish)', 'c':'CK-12', 'd':'Boundless', 'e':'Mustard Seed Books', 
            'f':'Project Gutenberg', 'g':'World Map', 'h':'openstax Textbooks', 'i':'Rasp Pi User Guide', 
            'j':'Scratch', 'k':'Khan Academy (English)', 'l':'Khan Academy (Spanish)',
            'm':'Wikipedia for schools', 'n':'Wikipedia (English)', 'o':'Wikipedia (Spanish)', 'p':'Wikipedia (French)', 
            'q':'Wiktionary (English)', 'r':'Wiktionary (Spanish)', 's':'Wiktionary (French)', 
            't':'Vikidia (English)', 'u':'Vikidia (Spanish)', 'v':'Vikidia (French)', 'w':'Kuyers Christian Ed Resources',
            'x':'Wikivoyage (English)', 'y':'Wikivoyage (Spanish)', 'z':'Wikivoyage (French)',
            'A':'PhET Simulations (English)', 'B':'PhET Simulations (Spanish)', 'C':'PhET Simulations (French)' }

# root URL for Kiwix resources
KIWIX_URL = 'http://download.kiwix.org/zim/'

# Set home folder location (username may be different than the default pi)
HOME = f'/home/{os.getlogin()}'

# Prompt user to select modules to install
screen = curses.initscr()
curses.noecho()
curses.cbreak()

selections = ''
try:
    while True:
        row = 1
        column = 5
        for key in OPTIONS.keys():
            # Highlight modules that are currently selected
            if key in selections:
                screen.addstr(row, column, '{}) {}'.format(key,OPTIONS[key]), curses.A_BOLD|curses.A_REVERSE)
            else:
                screen.addstr(row, column, '{}) {}'.format(key,OPTIONS[key]))
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
            selections = selections.replace(c,'')
            continue
        elif c in OPTIONS.keys():        # if key is recognized, add it to selections
            selections += c
        else:                            # Beep if key is unrecognized
            curses.beep()
except KeyboardInterrupt:                # quit gracefully if ctrl-c is pressed
    curses.endwin()
    sys.exit(0)

curses.endwin()
if selections == '':
    print('No modules selected... Done')
    sys.exit(0)

# List selected modules to install
print('The following modules will be installed: ', end='')
for letter in OPTIONS.keys():
    if letter in selections:
        print(OPTIONS[letter], end=', ')
print('\b\b...\n')

# Temporarily mount root partion in read-write mode for adding content
do('mount -o remount,rw /')

# Ensure lynx dependency is installed
do('apt -y install lynx') or sys.exit('Error: cannot install lynx dependency')

# Install the selected modules from various open education resources
for selection in selections:
    if OPTIONS[selection] == 'Wikipedia for schools':     # Wikipedia for schools (static version does not require kiwix)
        print('Installing Wikipedia for schools...')
        do('rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-wikipedia_for_schools-static /var/www/modules') or sys.exit('Error installing content')
        print('Done')
    elif OPTIONS[selection] == 'Wikipedia (English)':
        print('Installing Wikipedia (English)...')
        do('mkdir /var/www/modules/en-wikipedia')
        kiwix_url = KIWIX_URL + 'wikipedia'
        # use the "simple mini" version with smaller ZIM file to accommodate limited memory of Raspberry Pi
        filename = get_latest_kiwix_filename('wikipedia_en_simple_all_mini_',kiwix_url)
        print(f'Downloading {filename}...')
        do(f'wget --no-check-certificate -nv --show-progress -O /var/www/modules/en-wikipedia/en-wikipedia.zim {filename}')
        do(f'{HOME}/kiwix/kiwix-manage {HOME}/kiwix/library_zim.xml add /var/www/modules/en-wikipedia/en-wikipedia.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/en-wikipedia">Wikipedia (English)</a></h2>\n</div>'
        append_file('/var/www/modules/en-wikipedia/index.htmlf', html)
        print('Done - this module will become active after the next reboot')
    elif OPTIONS[selection] == 'Wikipedia (Spanish)':
        print('Installing Wikipedia (Spanish)...')
        do('mkdir /var/www/modules/es-wikipedia')
        kiwix_url = KIWIX_URL + 'wikipedia'
        # use the "top mini" version with smaller ZIM file to accommodate limited memory of Raspberry Pi
        filename = get_latest_kiwix_filename('wikipedia_es_top_mini_',kiwix_url)
        print(f'Downloading {filename}...')
        do(f'wget --no-check-certificate -nv --show-progress -O /var/www/modules/es-wikipedia/es-wikipedia.zim {filename}')
        do(f'{HOME}/kiwix/kiwix-manage {HOME}/kiwix/library_zim.xml add /var/www/modules/es-wikipedia/es-wikipedia.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/es-wikipedia">Wikipedia (Spanish)</a></h2>\n</div>'
        append_file('/var/www/modules/es-wikipedia/index.htmlf', html)
        print('Done - this module will become active after the next reboot')
    elif OPTIONS[selection] == 'Wikipedia (French)':
        print('Installing Wikipedia (French)...')
        do('mkdir /var/www/modules/fr-wikipedia')
        kiwix_url = KIWIX_URL + 'wikipedia'
        # use the "top mini" version with smaller ZIM file to accommodate limited memory of Raspberry Pi
        filename = get_latest_kiwix_filename('wikipedia_fr_top_mini_',kiwix_url)
        print(f'Downloading {filename}...')
        do(f'wget --no-check-certificate -nv --show-progress -O /var/www/modules/fr-wikipedia/fr-wikipedia.zim {filename}')
        do(f'{HOME}/kiwix/kiwix-manage {HOME}/kiwix/library_zim.xml add /var/www/modules/fr-wikipedia/fr-wikipedia.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/fr-wikipedia">Wikipedia (French)</a></h2>\n</div>'
        append_file('/var/www/modules/fr-wikipedia/index.htmlf', html)
        print('Done - this module will become active after the next reboot')
    elif OPTIONS[selection] == 'Wiktionary (English)':
        print('Installing Wiktionary (English)...')
        do('mkdir /var/www/modules/en-wiktionary')
        kiwix_url = KIWIX_URL + 'wiktionary'
        # use the "simple" version with smaller ZIM file to accommodate limited memory of Raspberry Pi
        filename = get_latest_kiwix_filename('wiktionary_en_simple_all_maxi_',kiwix_url)
        print(f'Downloading {filename}...')
        do(f'wget --no-check-certificate -nv --show-progress -O /var/www/modules/en-wiktionary/en-wiktionary.zim {filename}')
        do(f'{HOME}/kiwix/kiwix-manage {HOME}/kiwix/library_zim.xml add /var/www/modules/en-wiktionary/en-wiktionary.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/en-wiktionary">Wiktionary (English)</a></h2>\n</div>'
        append_file('/var/www/modules/en-wiktionary/index.htmlf', html)
        print('Done - this module will become active after the next reboot')
    elif OPTIONS[selection] == 'Wiktionary (Spanish)':
        print('Installing Wiktionary (Spanish)...')
        do('mkdir /var/www/modules/es-wiktionary')
        kiwix_url = KIWIX_URL + 'wiktionary'
        filename = get_latest_kiwix_filename('wiktionary_es_all_maxi_',kiwix_url)
        print(f'Downloading {filename}...')
        do(f'wget --no-check-certificate -nv --show-progress -O /var/www/modules/es-wiktionary/es-wiktionary.zim {filename}')
        do(f'{HOME}/kiwix/kiwix-manage {HOME}/kiwix/library_zim.xml add /var/www/modules/es-wiktionary/es-wiktionary.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/es-wiktionary">Wiktionary (Spanish)</a></h2>\n</div>'
        append_file('/var/www/modules/es-wiktionary/index.htmlf', html)
        print('Done - this module will become active after the next reboot')
    elif OPTIONS[selection] == 'Wiktionary (French)':
        print('Installing Wiktionary (French)...')
        do('mkdir /var/www/modules/fr-wiktionary')
        kiwix_url = KIWIX_URL + 'wiktionary'
        filename = get_latest_kiwix_filename('wiktionary_fr_app_maxi_',kiwix_url)
        print(f'Downloading {filename}...')
        do(f'wget --no-check-certificate -nv --show-progress -O /var/www/modules/fr-wiktionary/fr-wiktionary.zim {filename}')
        do(f'{HOME}/kiwix/kiwix-manage {HOME}/kiwix/library_zim.xml add /var/www/modules/fr-wiktionary/fr-wiktionary.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/fr-wiktionary">Wiktionary (French)</a></h2>\n</div>'
        append_file('/var/www/modules/fr-wiktionary/index.htmlf', html)
        print('Done - this module will become active after the next reboot')
    elif OPTIONS[selection] == 'Vikidia (English)':
        print('Installing Vikidia (English)...')
        do('mkdir /var/www/modules/en-vikidia')
        kiwix_url = KIWIX_URL + 'vikidia'
        filename = get_latest_kiwix_filename('vikidia_en_all_maxi_',kiwix_url)
        print(f'Downloading {filename}...')
        do(f'wget --no-check-certificate -nv --show-progress -O /var/www/modules/en-vikidia/en-vikidia.zim {filename}')
        do(f'{HOME}/kiwix/kiwix-manage {HOME}/kiwix/library_zim.xml add /var/www/modules/en-vikidia/en-vikidia.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/en-vikidia">Vikidia (English)</a></h2>\n</div>'
        append_file('/var/www/modules/en-vikidia/index.htmlf', html)
        print('Done - this module will become active after the next reboot')
    elif OPTIONS[selection] == 'Vikidia (Spanish)':
        print('Installing Vikidia (Spanish)...')
        do('mkdir /var/www/modules/es-vikidia')
        kiwix_url = KIWIX_URL + 'vikidia'
        filename = get_latest_kiwix_filename('vikidia_es_all_maxi_',kiwix_url)
        print(f'Downloading {filename}...')
        do(f'wget --no-check-certificate -nv --show-progress -O /var/www/modules/es-vikidia/es-vikidia.zim {filename}')
        do(f'{HOME}/kiwix/kiwix-manage {HOME}/kiwix/library_zim.xml add /var/www/modules/es-vikidia/es-vikidia.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/es-vikidia">Vikidia (Spanish)</a></h2>\n</div>'
        append_file('/var/www/modules/es-vikidia/index.htmlf', html)
        print('Done - this module will become active after the next reboot')
    elif OPTIONS[selection] == 'Vikidia (French)':
        print('Installing Vikidia (French)...')
        do('mkdir /var/www/modules/fr-vikidia')
        kiwix_url = KIWIX_URL + 'vikidia'
        filename = get_latest_kiwix_filename('vikidia_fr_all_maxi_',kiwix_url)
        print(f'Downloading {filename}...')
        do(f'wget --no-check-certificate -nv --show-progress -O /var/www/modules/fr-vikidia/fr-vikidia.zim {filename}')
        do(f'{HOME}/kiwix/kiwix-manage {HOME}/kiwix/library_zim.xml add /var/www/modules/fr-vikidia/fr-vikidia.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/fr-vikidia">Vikidia (French)</a></h2>\n</div>'
        append_file('/var/www/modules/fr-vikidia/index.htmlf', html)
        print('Done - this module will become active after the next reboot')
    elif OPTIONS[selection] == 'Wikivoyage (English)':
        print('Installing Wikivoyage (English)...')
        do('mkdir /var/www/modules/en-wikivoyage')
        kiwix_url = KIWIX_URL + 'wikivoyage'
        filename = get_latest_kiwix_filename('wikivoyage_en_all_maxi_',kiwix_url)
        print(f'Downloading {filename}...')
        do(f'wget --no-check-certificate -nv --show-progress -O /var/www/modules/en-wikivoyage/en-wikivoyage.zim {filename}')
        do(f'{HOME}/kiwix/kiwix-manage {HOME}/kiwix/library_zim.xml add /var/www/modules/en-wikivoyage/en-wikivoyage.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/en-wikivoyage">Wikivoyage (English)</a></h2>\n</div>'
        append_file('/var/www/modules/en-wikivoyage/index.htmlf', html)
        print('Done - this module will become active after the next reboot')
    elif OPTIONS[selection] == 'Wikivoyage (Spanish)':
        print('Installing Wikivoyage (Spanish)...')
        do('mkdir /var/www/modules/es-wikivoyage')
        kiwix_url = KIWIX_URL + 'wikivoyage'
        filename = get_latest_kiwix_filename('wikivoyage_es_all_maxi_',kiwix_url)
        print(f'Downloading {filename}...')
        do(f'wget --no-check-certificate -nv --show-progress -O /var/www/modules/es-wikivoyage/es-wikivoyage.zim {filename}')
        do(f'{HOME}/kiwix/kiwix-manage {HOME}/kiwix/library_zim.xml add /var/www/modules/es-wikivoyage/es-wikivoyage.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/es-wikivoyage">Wikivoyage (Spanish)</a></h2>\n</div>'
        append_file('/var/www/modules/es-wikivoyage/index.htmlf', html)
        print('Done - this module will become active after the next reboot')
    elif OPTIONS[selection] == 'Wikivoyage (French)':
        print('Installing Wikivoyage (French)...')
        do('mkdir /var/www/modules/fr-wikivoyage')
        kiwix_url = KIWIX_URL + 'wikivoyage'
        filename = get_latest_kiwix_filename('wikivoyage_fr_all_maxi_',kiwix_url)
        print(f'Downloading {filename}...')
        do(f'wget --no-check-certificate -nv --show-progress -O /var/www/modules/fr-wikivoyage/fr-wikivoyage.zim {filename}')
        do(f'{HOME}/kiwix/kiwix-manage {HOME}/kiwix/library_zim.xml add /var/www/modules/fr-wikivoyage/fr-wikivoyage.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/fr-wikivoyage">Wikivoyage (French)</a></h2>\n</div>'
        append_file('/var/www/modules/fr-wikivoyage/index.htmlf', html)
        print('Done - this module will become active after the next reboot')
    elif OPTIONS[selection] == 'PhET Simulations (English)':
        print('Installing PhET Simulations (English)...')
        do('mkdir /var/www/modules/en-phet')
        kiwix_url = KIWIX_URL + 'phet'
        filename = get_latest_kiwix_filename('phet_en_',kiwix_url)
        print(f'Downloading {filename}...')
        do(f'wget --no-check-certificate -nv --show-progress -O /var/www/modules/en-phet/en-phet.zim {filename}')
        do(f'{HOME}/kiwix/kiwix-manage {HOME}/kiwix/library_zim.xml add /var/www/modules/en-phet/en-phet.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/en-phet">PhET Interactive Simulations (English)</a></h2>\n</div>'
        append_file('/var/www/modules/en-phet/index.htmlf', html)
        print('Done - this module will become active after the next reboot')
    elif OPTIONS[selection] == 'PhET Simulations (Spanish)':
        print('Installing PhET Simulations (Spanish)...')
        do('mkdir /var/www/modules/es-phet')
        kiwix_url = KIWIX_URL + 'phet'
        filename = get_latest_kiwix_filename('phet_es_',kiwix_url)
        print(f'Downloading {filename}...')
        do(f'wget --no-check-certificate -nv --show-progress -O /var/www/modules/es-phet/es-phet.zim {filename}')
        do(f'{HOME}/kiwix/kiwix-manage {HOME}/kiwix/library_zim.xml add /var/www/modules/es-phet/es-phet.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/es-phet">PhET Interactive Simulations (Spanish)</a></h2>\n</div>'
        append_file('/var/www/modules/es-phet/index.htmlf', html)
        print('Done - this module will become active after the next reboot')
    elif OPTIONS[selection] == 'PhET Simulations (French)':
        print('Installing PhET Simulations (French)...')
        do('mkdir /var/www/modules/fr-phet')
        kiwix_url = KIWIX_URL + 'phet'
        filename = get_latest_kiwix_filename('phet_fr_',kiwix_url)
        print(f'Downloading {filename}...')
        do(f'wget --no-check-certificate -nv --show-progress -O /var/www/modules/fr-phet/fr-phet.zim {filename}')
        do(f'{HOME}/kiwix/kiwix-manage {HOME}/kiwix/library_zim.xml add /var/www/modules/fr-phet/fr-phet.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/fr-phet">PhET Interactive Simulations (French)</a></h2>\n</div>'
        append_file('/var/www/modules/fr-phet/index.htmlf', html)
        print('Done - this module will become active after the next reboot')
    elif OPTIONS[selection] == 'Blockly':
        print("Installing Blockly games...")
        do('rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-blockly-games /var/www/modules') or sys.exit('Error installing content')
        print('Done')
    elif OPTIONS[selection] == 'Blockly (Spanish)':
        print("Installing Blockly games (Spanish)...")
        do('rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/es-blockly-games /var/www/modules') or sys.exit('Error installing content')
        print('Done')
    elif OPTIONS[selection] == 'CK-12':
        print('Installing CK-12...')
        do('rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-ck12 /var/www/modules') or sys.exit('Error installing content')
        print('Done')
    elif OPTIONS[selection] == 'Boundless':
        print('Installing Boundless...')
        do('rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-boundless-static /var/www/modules') or sys.exit('Error installing content')
        print('Done\n')
    elif OPTIONS[selection] == 'Mustard Seed Books':
        print('Installing Mustard Seed Books...')
        do('rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-mustardseedbooks /var/www/modules') or sys.exit('Error installing content')
        print('Done\n')
    elif OPTIONS[selection] == 'Project Gutenberg':
        print('Installing Project Gutenberg...')
        do('rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-ebooks /var/www/modules') or sys.exit('Error installing content')
        print('Done\n')
    elif OPTIONS[selection] == 'World Map':
        print("Installing World Map...")
        do('rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-worldmap-10 /var/www/modules') or sys.exit('Error installing content')
        print('Done\n')
    elif OPTIONS[selection] == 'Khan Academy (English)':
        print('Installing Khan Academy (English)...')
        do("rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-kaos /var/www/modules") or sys.exit('Error installing content')
        print('Done\n')
    elif OPTIONS[selection] == 'Khan Academy (Spanish)':
        print('Installing Khan Academy (Spanish)...')
        do("rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/es-kaos /var/www/modules") or sys.exit('Error installing content')
        print('Done\n')
    elif OPTIONS[selection] == 'openstax Textbooks':
        print('Installing openstax Textbooks...')
        do("rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-openstax /var/www/modules") or sys.exit('Error installing content')
        print('Done\n')
    elif OPTIONS[selection] == 'Rasp Pi User Guide':
        print('Installing Rasp Pi User Guide...')
        do("rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-rpi_guide /var/www/modules") or sys.exit('Error installing content')
        print('Done\n')
    elif OPTIONS[selection] == 'Scratch':
        print('Installing Scratch...')
        do("rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-scratch /var/www/modules") or sys.exit('Error installing content')
        print('Done\n')
    elif OPTIONS[selection] == 'Kuyers Christian Ed Resources':
        print('Installing Kuyers Christian Education Resources...')
        do('git clone --depth 1 https://github.com/dschuurman/en-kuyers-cer.git') or sys.exit('Error installing content')
        do('mv en-kuyers-cer /var/www/modules') or sys.exit('Error moving content')
        print('Done')

# update ownership and permissions of modules
print('Setting module folder permissions and ownership (this may take a moment)...')
do('chown -R www-data.www-data /var/www/modules') or sys.exit('Error changing ownership of modules folder to www-data')
do('chmod -R 755 /var/www/modules') or sys.exit('Error changing permissions of module files')

# Once content is installed and configured, return root partion to read-only mode
do('mount -o remount,ro /')

print('\nDONE!')
print('** Each content module is subject to its own license terms and conditions.')
print('** Note that a reboot may be required for some modules to become active.')
print("** To reboot, type 'sudo reboot' at the command-line.")