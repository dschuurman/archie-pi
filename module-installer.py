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
import subprocess
import curses

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

# collection of available modules
OPTIONS = { 'a':'Blockly', 'b':'Blockly (Spanish)', 'c':'CK-12', 'd':'Boundless', 'e':'Mustard Seed Books', 
            'f':'Project Gutenberg', 'g':'World Map', 'h':'openstax Textbooks', 'i':'Rasp Pi User Guide', 
            'j':'Scratch', 'k':'Khan Academy', 'l':'Khan Academy (Spanish)',
            'm':'Wikipedia for schools', 'n':'Wikipedia (English)', 'o':'Wikipedia (Spanish)', 'p':'Wikipedia (French)', 
            'q':'Wiktionary (English)', 'r':'Wiktionary (Spanish)', 's':'Wiktionary (French)', 
            't':'Wikibooks (English)', 'u':'Wikibooks (Spanish)', 'v':'Wikibooks (French)',
            'w':'Vikidia (English)', 'x':'Vikidia (Spanish)', 'y':'Vikidia (French)', 'z':'Kuyers Christian Ed Resources',
            'A':'Wikivoyage (English)', 'B':'Wikivoyage (Spanish)', 'C':'Wikivoyage (French)',
            'D':'PhET Simulations (English)', 'E':'PhET Simulations (Spanish)', 'F':'PhET Simulations (French)' }

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
        screen.addstr(row+2, 5, 'Type the letter(s) for the module(s) you wish to install.')
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

# Install the selected modules from various open education resources
for selection in selections:
    if OPTIONS[selection] == 'Wikipedia for schools':     # Wikipedia for schools (static version does not require kiwix)
        print('Installing Wikipedia for schools...')
        do('rsync -Paz --info=progress2 --info=name0 rsync://dev.worldpossible.org/rachelmods/en-wikipedia_for_schools-static /var/www/modules') or sys.exit('Error installing content')
        print('Done')
    elif OPTIONS[selection] == 'Wikipedia (English)':
        print('Installing Wikipedia (English)...')
        do('mkdir /var/www/modules/en-wikipedia')
        do('wget -nv --show-progress -O /var/www/modules/en-wikipedia/en-wikipedia.zim https://download.kiwix.org/zim/wikipedia/wikipedia_en_all_mini_2021-01.zim')
        do('/home/pi/kiwix/kiwix-manage /home/pi/kiwix/library_zim.xml add /var/www/modules/en-wikipedia/en-wikipedia.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/en-wikipedia">Wikipedia (English)</a></h2>\n</div>'
        append_file('/var/www/modules/en-wikipedia/index.htmlf', html)
        print('Done')
    elif OPTIONS[selection] == 'Wikipedia (Spanish)':
        print('Installing Wikipedia (Spanish)...')
        do('mkdir /var/www/modules/es-wikipedia')
        do('wget -nv --show-progress -O /var/www/modules/es-wikipedia/es-wikipedia.zim https://download.kiwix.org/zim/wikipedia/wikipedia_es_all_mini_2021-01.zim')
        do('/home/pi/kiwix/kiwix-manage /home/pi/kiwix/library_zim.xml add /var/www/modules/es-wikipedia/es-wikipedia.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/es-wikipedia">Wikipedia (Spanish)</a></h2>\n</div>'
        append_file('/var/www/modules/es-wikipedia/index.htmlf', html)
        print('Done')
    elif OPTIONS[selection] == 'Wikipedia (French)':
        print('Installing Wikipedia (French)...')
        do('mkdir /var/www/modules/fr-wikipedia')
        do('wget -nv --show-progress -O /var/www/modules/fr-wikipedia/fr-wikipedia.zim https://download.kiwix.org/zim/wikipedia/wikipedia_fr_all_mini_2021-01.zim')
        do('/home/pi/kiwix/kiwix-manage /home/pi/kiwix/library_zim.xml add /var/www/modules/fr-wikipedia/fr-wikipedia.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/fr-wikipedia">Wikipedia (French)</a></h2>\n</div>'
        append_file('/var/www/modules/fr-wikipedia/index.htmlf', html)
        print('Done')
    elif OPTIONS[selection] == 'Wiktionary (English)':
        print('Installing Wiktionary (English)...')
        do('mkdir /var/www/modules/en-wiktionary')
        do('wget -nv --show-progress -O /var/www/modules/en-wiktionary/en-wiktionary.zim https://download.kiwix.org/zim/wiktionary/wiktionary_en_all_maxi_2020-12.zim')
        do('/home/pi/kiwix/kiwix-manage /home/pi/kiwix/library_zim.xml add /var/www/modules/en-wiktionary/en-wiktionary.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/en-wiktionary">Wiktionary (English)</a></h2>\n</div>'
        append_file('/var/www/modules/en-wiktionary/index.htmlf', html)
        print('Done')
    elif OPTIONS[selection] == 'Wiktionary (Spanish)':
        print('Installing Wiktionary (Spanish)...')
        do('mkdir /var/www/modules/es-wiktionary')
        do('wget -nv --show-progress -O /var/www/modules/es-wiktionary/es-wiktionary.zim https://download.kiwix.org/zim/wiktionary/wiktionary_es_all_maxi_2020-12.zim')
        do('/home/pi/kiwix/kiwix-manage /home/pi/kiwix/library_zim.xml add /var/www/modules/es-wiktionary/es-wiktionary.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/es-wiktionary">Wiktionary (Spanish)</a></h2>\n</div>'
        append_file('/var/www/modules/es-wiktionary/index.htmlf', html)
        print('Done')
    elif OPTIONS[selection] == 'Wiktionary (French)':
        print('Installing Wiktionary (French)...')
        do('mkdir /var/www/modules/fr-wiktionary')
        do('wget -nv --show-progress -O /var/www/modules/fr-wiktionary/fr-wiktionary.zim https://download.kiwix.org/zim/wiktionary/wiktionary_fr_all_maxi_2020-12.zim')
        do('/home/pi/kiwix/kiwix-manage /home/pi/kiwix/library_zim.xml add /var/www/modules/fr-wiktionary/fr-wiktionary.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/fr-wiktionary">Wiktionary (French)</a></h2>\n</div>'
        append_file('/var/www/modules/fr-wiktionary/index.htmlf', html)
        print('Done')
    elif OPTIONS[selection] == 'Wikibooks (English)':
        print('Installing Wikibooks (English)...')
        do('mkdir /var/www/modules/en-wikibooks')
        do('wget -nv --show-progress -O /var/www/modules/en-wikibooks/en-wikibooks.zim https://download.kiwix.org/zim/wikibooks/wikibooks_en_all_maxi_2021-01.zim')
        do('/home/pi/kiwix/kiwix-manage /home/pi/kiwix/library_zim.xml add /var/www/modules/en-wikibooks/en-wikibooks.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/en-wikibooks">Wikibooks (English)</a></h2>\n</div>'
        append_file('/var/www/modules/en-wikibooks/index.htmlf', html)
        print('Done')
    elif OPTIONS[selection] == 'Wikibooks (Spanish)':
        print('Installing Wikibooks (Spanish)...')
        do('mkdir /var/www/modules/es-wikibooks')
        do('wget -nv --show-progress -O /var/www/modules/es-wikibooks/es-wikibooks.zim https://download.kiwix.org/zim/wikibooks/wikibooks_es_all_maxi_2021-01.zim')
        do('/home/pi/kiwix/kiwix-manage /home/pi/kiwix/library_zim.xml add /var/www/modules/es-wikibooks/es-wikibooks.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/es-wikibooks">Wikibooks (Spanish)</a></h2>\n</div>'
        append_file('/var/www/modules/es-wikibooks/index.htmlf', html)
        print('Done')
    elif OPTIONS[selection] == 'Wikibooks (French)':
        print('Installing Wikibooks (French)...')
        do('mkdir /var/www/modules/fr-wikibooks')
        do('wget -nv --show-progress -O /var/www/modules/fr-wikibooks/fr-wikibooks.zim https://download.kiwix.org/zim/wikibooks/wikibooks_fr_all_maxi_2021-01.zim')
        do('/home/pi/kiwix/kiwix-manage /home/pi/kiwix/library_zim.xml add /var/www/modules/fr-wikibooks/es-wikibooks.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/fr-wikibooks">Wikibooks (French)</a></h2>\n</div>'
        append_file('/var/www/modules/fr-wikibooks/index.htmlf', html)
        print('Done')
    elif OPTIONS[selection] == 'Vikidia (English)':
        print('Installing Vikidia (English)...')
        do('mkdir /var/www/modules/en-vikidia')
        do('wget -nv --show-progress -O /var/www/modules/en-vikidia/en-vikidia.zim https://download.kiwix.org/zim/vikidia/vikidia_en_all_maxi_2021-01.zim')
        do('/home/pi/kiwix/kiwix-manage /home/pi/kiwix/library_zim.xml add /var/www/modules/en-vikidia/en-vikidia.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/en-vikidia">Vikidia (English)</a></h2>\n</div>'
        append_file('/var/www/modules/en-vikidia/index.htmlf', html)
        print('Done')
    elif OPTIONS[selection] == 'Vikidia (Spanish)':
        print('Installing Vikidia (Spanish)...')
        do('mkdir /var/www/modules/es-vikidia')
        do('wget -nv --show-progress -O /var/www/modules/es-vikidia/es-vikidia.zim https://download.kiwix.org/zim/vikidia/vikidia_es_all_maxi_2021-01.zim')
        do('/home/pi/kiwix/kiwix-manage /home/pi/kiwix/library_zim.xml add /var/www/modules/es-vikidia/es-vikidia.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/es-vikidia">Vikidia (Spanish)</a></h2>\n</div>'
        append_file('/var/www/modules/es-vikidia/index.htmlf', html)
        print('Done')
    elif OPTIONS[selection] == 'Vikidia (French)':
        print('Installing Vikidia (French)...')
        do('mkdir /var/www/modules/fr-vikidia')
        do('wget -nv --show-progress -O /var/www/modules/fr-vikidia/fr-vikidia.zim https://download.kiwix.org/zim/vikidia/vikidia_fr_all_maxi_2021-01.zim')
        do('/home/pi/kiwix/kiwix-manage /home/pi/kiwix/library_zim.xml add /var/www/modules/fr-vikidia/fr-vikidia.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/fr-vikidia">Vikidia (French)</a></h2>\n</div>'
        append_file('/var/www/modules/fr-vikidia/index.htmlf', html)
        print('Done')
    elif OPTIONS[selection] == 'Wikivoyage (English)':
        print('Installing Wikivoyage (English)...')
        do('mkdir /var/www/modules/en-wikivoyage')
        do('wget -nv --show-progress -O /var/www/modules/en-wikivoyage/en-wikivoyage.zim https://download.kiwix.org/zim/wikivoyage/wikivoyage_en_all_maxi_2021-01.zim')
        do('/home/pi/kiwix/kiwix-manage /home/pi/kiwix/library_zim.xml add /var/www/modules/en-wikivoyage/en-wikivoyage.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/en-wikivoyage">Wikivoyage (English)</a></h2>\n</div>'
        append_file('/var/www/modules/en-wikivoyage/index.htmlf', html)
        print('Done')
    elif OPTIONS[selection] == 'Wikivoyage (Spanish)':
        print('Installing Wikivoyage (Spanish)...')
        do('mkdir /var/www/modules/es-wikivoyage')
        do('wget -nv --show-progress -O /var/www/modules/es-wikivoyage/es-wikivoyage.zim https://download.kiwix.org/zim/wikivoyage/wikivoyage_es_all_maxi_2021-01.zim')
        do('/home/pi/kiwix/kiwix-manage /home/pi/kiwix/library_zim.xml add /var/www/modules/es-wikivoyage/es-wikivoyage.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/es-wikivoyage">Wikivoyage (Spanish)</a></h2>\n</div>'
        append_file('/var/www/modules/es-wikivoyage/index.htmlf', html)
        print('Done')
    elif OPTIONS[selection] == 'Wikivoyage (French)':
        print('Installing Wikivoyage (French)...')
        do('mkdir /var/www/modules/fr-wikivoyage')
        do('wget -nv --show-progress -O /var/www/modules/fr-wikivoyage/fr-wikivoyage.zim https://download.kiwix.org/zim/wikivoyage/wikivoyage_fr_all_maxi_2021-01.zim')
        do('/home/pi/kiwix/kiwix-manage /home/pi/kiwix/library_zim.xml add /var/www/modules/fr-wikivoyage/fr-wikivoyage.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/fr-wikivoyage">Wikivoyage (French)</a></h2>\n</div>'
        append_file('/var/www/modules/fr-wikivoyage/index.htmlf', html)
        print('Done')
    elif OPTIONS[selection] == 'PhET Simulations (English)':
        print('Installing PhET Simulations (English)...')
        do('mkdir /var/www/modules/en-phet')
        do('wget -nv --show-progress -O /var/www/modules/en-phet/en-phet.zim https://download.kiwix.org/zim/phet/phet_en_2021-01.zim')
        do('/home/pi/kiwix/kiwix-manage /home/pi/kiwix/library_zim.xml add /var/www/modules/en-phet/en-phet.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/en-phet">PhET Interactive Simulations (English)</a></h2>\n</div>'
        append_file('/var/www/modules/en-phet/index.htmlf', html)
        print('Done')
    elif OPTIONS[selection] == 'PhET Simulations (Spanish)':
        print('Installing PhET Simulations (Spanish)...')
        do('mkdir /var/www/modules/es-phet')
        do('wget -nv --show-progress -O /var/www/modules/es-phet/es-phet.zim https://download.kiwix.org/zim/phet/phet_es_2021-01.zim')
        do('/home/pi/kiwix/kiwix-manage /home/pi/kiwix/library_zim.xml add /var/www/modules/es-phet/es-phet.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/es-phet">PhET Interactive Simulations (Spanish)</a></h2>\n</div>'
        append_file('/var/www/modules/es-phet/index.htmlf', html)
        print('Done')
    elif OPTIONS[selection] == 'PhET Simulations (French)':
        print('Installing PhET Simulations (French)...')
        do('mkdir /var/www/modules/fr-phet')
        do('wget -nv --show-progress -O /var/www/modules/fr-phet/fr-phet.zim https://download.kiwix.org/zim/phet/phet_fr_2021-01.zim')
        do('/home/pi/kiwix/kiwix-manage /home/pi/kiwix/library_zim.xml add /var/www/modules/fr-phet/fr-phet.zim')
        html = '<div class="indexmodule">\n<h2><a href="http://<?php echo $_SERVER["SERVER_ADDR"]?>:81/fr-phet">PhET Interactive Simulations (French)</a></h2>\n</div>'
        append_file('/var/www/modules/fr-phet/index.htmlf', html)
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

print('DONE! Note that a reboot is required for some modules to become active')
print('Please note that each content module is subject to its own license terms and conditions.')