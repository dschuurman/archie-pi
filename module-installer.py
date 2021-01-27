# Friendly script to install Open Enducation Resources (OER) for the 
# ARCHIE Pi project (Another Remote Community Hotspot for Instruction and Education).
# This script installs modules which are made available at http://oer2go.org
# which are subject to their own license terms.
#
# (C) 2020 faculty and students from Calvin University
#
# License: GNU General Public License (GPL) v3
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import sys
import subprocess
import curses

# Helper functions
def do(cmd):
    ''' Execute system command and return result
    '''
    result = subprocess.run(cmd.split(), stderr=sys.stderr, stdout=sys.stdout)
    return (result.returncode == 0)

# collection of available modules
OPTIONS = { 'a':'Blockly', 'b':'Blockly (Spanish)', 'c':'CK-12', 'd':'Boundless', 'e':'Mustard Seed Books', 
            'f':'Project Gutenberg', 'g':'World Map', 'i':'openstax Textbooks', 
            'j':'Rasp Pi User Guide', 'k':'Scratch', 'h':'Khan Academy', 'l':'Khan Academy (Spanish)',
            'm':'Wikipedia', 'n':'Wikipedia (Spanish)', 'o':'Wikipedia (French)', 
            'z':'Kuyers Christian Ed Resources' }

# Prompt user to select modules to install
screen = curses.initscr()
curses.noecho()
curses.cbreak()

selections = ''
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
    screen.addstr(row+2, 5, 'Type the letter(s) for the module(s) you wish to install.')
    screen.addstr(row+3, 5, 'To quit, press "q", to begin installation, press ENTER')
    screen.refresh()
    
    c = chr(screen.getch()).lower()
    if c == 'q':                     # quit if 'q' is pressed
        curses.endwin()
        sys.exit(0)
    elif ord(c)==10 or ord(c)==13:   # check for ENTER key
        break
    elif c in selections:            # unselect if key is already selected
        selections = selections.replace(c,'')
        continue
    elif c in OPTIONS.keys():        # if key is recognized, add it to selections
        selections += c
    else:                            # Beep if key is unrecognized
        curses.beep()

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

# Install the selected modules from http://oer2go.org
for selection in selections:
    if OPTIONS[selection] == 'Wikipedia':     # Wikipedia for schools (static version does not require kiwix)
        print('Installing Wikipedia for schools...')
        do('rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-wikipedia_for_schools-static /var/www/modules') or sys.exit('Error installing content')
        print('Done')
    elif OPTIONS[selection] == 'Wikipedia (Spanish)':
        print('Installing Wikipedia for schools (Spanish)...')
        do('rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/es-wikipedia-static /var/www/modules') or sys.exit('Error installing content')
        print('Done')
    elif OPTIONS[selection] == 'Wikipedia (French)':
        print('Installing Wikipedia for schools (French)...')
        do('rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/fr-wikipedia-static /var/www/modules') or sys.exit('Error installing content')
        print('Done')
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
    elif OPTIONS[selection] == 'Khan Academy':
        print('Installing Khan Academy...')
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

# update ownership of modules folder to web user (www-data)
print('Setting module folder permissions...')
do('chown -R www-data.www-data /var/www/modules') or sys.exit('Error changing ownership of modules folder to www-data')

# Once content is installed, return root partion to read-only mode
do('mount -o remount,ro /')

print('DONE!')
