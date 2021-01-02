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
OPTIONS = {'a':'Blockly', 'b':'Wikipedia', 'c':'CK-12', 'd':'Boundless', 'e':'Mustard Seed Books', 
           'f':'Project Gutenberg', 'g':'Math Expression', 'h':'World Map', 'i':'Algebra2Go', 
           'j':'Understanding Algebra', 'k':'Khan Academy' }

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
            column = 40
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
    if OPTIONS[selection] == 'Blockly':
        print("Installing Blockly games...")
        do('rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-blockly-games /var/www/modules') or sys.exit('Error installing Blockly')
        print('Done')

    # Install Wikipedia for schools (static version does not require kiwix)
    elif OPTIONS[selection] == 'Wikipedia':
        print('Installing Wikipedia for schools...')
        do('rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-wikipedia_for_schools-static /var/www/modules') or sys.exit('Error installing Wikipedia')
        print('Done')

    # Install CK-12 open textbooks for schools
    elif OPTIONS[selection] == 'CK-12':
        print('Installing CK-12...')
        do('rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-ck12 /var/www/modules') or sys.exit('Error installing CK-12')
        print('Done')

    # Install Boundless open textbooks for schools
    elif OPTIONS[selection] == 'Boundless':
        print('Installing Boundless...')
        do('rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-boundless-static /var/www/modules') or sys.exit('Error installing Boundless open textbooks')
        print('Done\n')

    # Install mustard seed books
    elif OPTIONS[selection] == 'Mustard Seed Books':
        print('Installing Mustard Seed Books...')
        do('rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-mustardseedbooks /var/www/modules') or sys.exit('Error installing mustard seed books')
        print('Done\n')

    # Install great books from project gutenberg
    elif OPTIONS[selection] == 'Project Gutenberg':
        print('Installing Project Gutenberg...')
        do('rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-ebooks /var/www/modules') or sys.exit('Error installing project gutenberg')
        print('Done\n')

    # Install math expression
    elif OPTIONS[selection] == 'Math Expression':
        print('Installing Math Expression...')
        do('rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-math_expression /var/www/modules') or sys.exit('Error installing math expression')
        print('Done\n')

    # Install World Map
    elif OPTIONS[selection] == 'World Map':
        print("Installing World Map...")
        do('rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-worldmap-10 /var/www/modules') or sys.exit('Error installing World Map')
        print('Done\n')

    # Install Algebra2Go
    elif OPTIONS[selection] == 'Algebra2Go':
        print("Installing Algebra2Go...")
        do('rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-algebra2go /var/www/modules') or sys.exit('Error installing Algebra2Go')
        print('Done\n')

   # Install Understanding Algebra
    elif OPTIONS[selection] == 'Understanding Algebra':
        print("Installing Understanding Algebra...")
        do('rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-understanding_algebra /var/www/modules') or sys.exit('Error installing Understanding Algebra')
        print('Done\n')

   # Install Khan Academy
    elif OPTIONS[selection] == 'Khan Academy':
        print('Installing Khan Academy...')
        do("rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-kaos /var/www/modules")or sys.exit('Error installing Khan Academy content')
        print('Done\n')

# update ownership of modules folder to web user (www-data)
do('chown -R www-data.www-data /var/www/modules') or sys.exit('Error changing ownership of modules folder to www-data')

# Once content is installed, return root partion to read-only mode
do('mount -o remount,ro /')

print('DONE!')
