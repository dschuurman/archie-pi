# Script to configure wifi country using an ISO 3166 alpha2 country code
# for the ARCHIE Pi (Another Remote Community Hotspot for Instruction and Education)
# on a Raspberry Pi (all versions) running Raspberry Pi OS Lite.
#
# (C) 2023 faculty and students from Calvin University
#
# License: GNU General Public License (GPL) v3
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import pycountry
import sys
import fileinput
import subprocess

# Helper functions
def do(cmd):
    ''' Execute system command and return result
    '''
    result = subprocess.run(cmd.split(), stderr=sys.stderr, stdout=sys.stdout)
    return (result.returncode == 0)

def replace_line(orig_line, new_line, infile):
    ''' Replace a line with matching text in a specified file
    '''
    found = False
    for line in fileinput.input(infile, inplace = True):
        if not found and orig_line in line:
            print(line.replace(line, new_line), end='')
            found = True
        else:
            print(line, end='')
    return found

print('For reference, here is a list of countries and their corresponding country codes:')
codes = []
for country in list(pycountry.countries):
    print(f'{country.name}={country.alpha_2}',end=' ')
    codes.append(country.alpha_2)

code = input('\n\nPlease enter the country code for the ARCHIE Pi Wi-Fi setup: ')
if code not in codes:
    print('Sorry, uncrecognized country code...')
    sys.exit(1)

# Temporarily mount root partion in read-write mode for adding content
do('mount -o remount,rw /')

# Add the country code to wpa_supplicant.conf in case it is needed
replace_line('country=', f'country={code}', '/etc/wpa_supplicant/wpa_supplicant.conf') or sys.exit('Error changing country code')
replace_line('REGDOMAIN=', f'REGDOMAIN={code}', '/etc/default/crda') or sys.exit('Error changing regulatory domain setting')

# Once content is installed and configured, suggest a reboot
print("** Update requires a reboot to activate: type 'sudo reboot' at the command-line.")
print('\nDONE!')
