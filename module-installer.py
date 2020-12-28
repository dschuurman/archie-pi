#!/usr/bin/env python
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

# List of modules to install
OPTIONS = {'a':'BLOCKLY', 'b':'WIKIPEDIA', 'c':'CK-12', 'd':'BOUNDLESS', 'e':'MUSTARD SEED BOOKS', 
           'f':'GUTENBERG', 'g':'MATH EXPRESSION', 'h':'WORLD MAP'}

# Helper functions
def do(cmd):
    ''' Execute system command and return result
    '''
    result = subprocess.run(cmd.split(), stderr=sys.stderr, stdout=sys.stdout)
    return (result.returncode == 0)

# Prompt user to select modules to install
screen = curses.initscr()
curses.noecho()
curses.cbreak()

selections = ''
while True:
    line = 1
    for key in OPTIONS.keys():
        # Highlight modules that are currently selected
        if key in selections:
            screen.addstr(line, 5, '{}) {}'.format(key,OPTIONS[key]), curses.A_BOLD|curses.A_REVERSE)
        else:
            screen.addstr(line, 5, '{}) {}'.format(key,OPTIONS[key]))
        line +=1
    screen.addstr(line+1, 5, 'Type the letter(s) for the module(s) you wish to install.')
    screen.addstr(line+2, 5, 'To quit, press "q", to begin installation, press ENTER')
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

# Install the selected modules from http://oer2go.org
for selection in selections:
    if OPTIONS[selection] == 'BLOCKLY':
        print("Installing Blockly games...")
        do('rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-blockly-games /var/www/modules') or sys.exit('error installing Blockly')
        print('Done')

    # Install Wikipedia for schools (static version does not require kiwix)
    elif OPTIONS[selection] == 'WIKIPEDIA':
        print('Installing Wikipedia for schools...')
        do('rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-wikipedia_for_schools-static /var/www/modules') or sys.exit('error installing Wikipedia')
        print('Done')

    # Install CK-12 open textbooks for schools
    elif OPTIONS[selection] == 'CK-12':
        print('Installing CK-12...')
        do('rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-ck12 /var/www/modules') or sys.exit('error installing CK-12')
        print('Done')

    # Install Boundless open textbooks for schools
    elif OPTIONS[selection] == 'BOUNDLESS':
        print('Installing Boundless...')
        do('rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-boundless-static /var/www/modules') or sys.exit('error installing Boundless open textbooks')
        print('Done\n')

    # Install mustard seed books
    elif OPTIONS[selection] == 'MUSTARD SEED BOOKS':
        print('Installing Mustard Seed Books...')
        do('rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-mustardseedbooks /var/www/modules') or sys.exit('error installing mustard seed books')
        print('Done\n')

    # Install great books from project gutenberg
    elif OPTIONS[selection] == 'GUTENBERG':
        print('Installing Project Gutenberg...')
        do('rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-ebooks /var/www/modules') or sys.exit('error installing project gutenberg')
        print('Done\n')

    # Install math expression
    elif OPTIONS[selection] == 'MATH EXPRESSION':
        print('Installing Math Expression...')
        do('rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-math_expression /var/www/modules') or sys.exit('error installing math expression')
        print('Done\n')

    # Install World Map
    elif OPTIONS[selection] == 'WORLD MAP':
        print("Installing World Map...")
        do('rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-worldmap-10 /var/www/modules') or sys.exit('error installing World Map')
        print('Done\n')

# update ownership of modules folder to web user (www-data)
do('chown -R www-data.www-data /var/www/modules') or sys.exit('Error changing ownership of modules folder to www-data')

print('DONE!')
