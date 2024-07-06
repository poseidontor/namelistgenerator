#!/usr/bin/env python3

"""
namelistgenerator.py is a tool for generating a Active Directory username list.

The script expects a input file with list of user's full name
Eg:
John Moris
Kevin Sparrow

And the script will output usernames in differet formats like john.moris, johnm, john, jmoris

Author @poseidontor

Most of the code is taken from https://github.com/initstring/linkedin2username
"""

import os
import re
import argparse


class NameMutator():
    """
    This class handles all name mutations.

    Init with a raw name, and then call the individual functions to return a mutation.
    """
    def __init__(self, name):
        self.name = self.split_name(name)

    

    @staticmethod
    def split_name(name):
        """
        Takes a name (string) and returns a list of individual name-parts (dict).

        Some people have funny names. We assume the most important names are:
        first name, last name, and the name right before the last name (if they have one)
        """
        # Split on spaces and dashes (included repeated)
        parsed = re.split(r'[\s-]+', name)

        # Iterate and remove empty strings
        parsed = [part for part in parsed if part]

        # Discard people without at least a first and last name
        if len(parsed) < 2:
            return None

        if len(parsed) > 2:
            split_name = {'first': parsed[0], 'second': parsed[-2], 'last': parsed[-1]}
        else:
            split_name = {'first': parsed[0], 'second': '', 'last': parsed[-1]}

        # Final sanity check to not proceed without first and last name
        if not split_name['first'] or not split_name['last']:
            return None

        return split_name

    def f_last(self):
        """jsmith"""
        names = set()
        names.add(self.name['first'][0] + self.name['last'])

        if self.name['second']:
            names.add(self.name['first'][0] + self.name['second'])

        return names

    def f_dot_last(self):
        """j.smith"""
        names = set()
        names.add(self.name['first'][0] + '.' + self.name['last'])

        if self.name['second']:
            names.add(self.name['first'][0] + '.' + self.name['second'])

        return names

    def last_f(self):
        """smithj"""
        names = set()
        names.add(self.name['last'] + self.name['first'][0])

        if self.name['second']:
            names.add(self.name['second'] + self.name['first'][0])

        return names

    def first_dot_last(self):
        """john.smith"""
        names = set()
        names.add(self.name['first'] + '.' + self.name['last'])

        if self.name['second']:
            names.add(self.name['first'] + '.' + self.name['second'])

        return names

    def first_l(self):
        """johns"""
        names = set()
        names.add(self.name['first'] + self.name['last'][0])

        if self.name['second']:
            names.add(self.name['first'] + self.name['second'][0])

        return names

    def first(self):
        """john"""
        names = set()
        names.add(self.name['first'])

        return names


def parse_arguments():
    """
    Handle user-supplied arguments
    """
    desc = ('Tool for generating Active Directory Usernames by taking a file contianing full names as input.')
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-c', '--company', type=str, action='store',
                        required=True,
                        help='Company name exactly as typed in the company '
                        'linkedin profile page URL.')
    parser.add_argument('-n', '--domain', type=str, action='store',
                        default='',
                        help='Append a domain name to username output. '
                        '[example: "-n uber.com" would output jschmoe@uber.com]'
                        )
    parser.add_argument('-o', '--output', default="namelistgenerator-output", action="store",
                        help='Output Directory, defaults to li2u-output')
    parser.add_argument('-f', '--file', default="", type=str, action="store", required=True,
                        help='File containting user\'s full name')

    args = parser.parse_args()

    

    # If appending an email address, preparing this string now:
    if args.domain:
        args.domain = '@' + args.domain

    

    return args




def write_lines(employees, name_func, domain, outfile):
    """
    Helper function to mutate names and write to an outfile

    Needs to be called with a string variable in name_func that matches the class method
    name in the NameMutator class.
    """
    for employee in employees:
        mutator = NameMutator(employee)
        if mutator.name:
            for name in getattr(mutator, name_func)():
                outfile.write(name + domain + '\n')


def write_files(company, domain, employees, out_dir):
    """Writes data to various formatted output files.

    After scraping and processing is complete, this function formats the raw
    names into common username formats and writes them into a directory called
    li2u-output unless specified.

    See in-line comments for decisions made on handling special cases.
    """

    # Check for and create an output directory to store the files.
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    

    with open(f'{out_dir}/{company}-flast.txt', 'w', encoding='utf-8') as outfile:
        write_lines(employees, 'f_last', domain, outfile)

    with open(f'{out_dir}/{company}-f.last.txt', 'w', encoding='utf-8') as outfile:
        write_lines(employees, 'f_dot_last', domain, outfile)

    with open(f'{out_dir}/{company}-firstl.txt', 'w', encoding='utf-8') as outfile:
        write_lines(employees, 'first_l', domain, outfile)

    with open(f'{out_dir}/{company}-first.last.txt', 'w', encoding='utf-8') as outfile:
        write_lines(employees, 'first_dot_last', domain, outfile)

    with open(f'{out_dir}/{company}-first.txt', 'w', encoding='utf-8') as outfile:
        write_lines(employees, 'first', domain, outfile)

    with open(f'{out_dir}/{company}-lastf.txt', 'w', encoding='utf-8') as outfile:
        write_lines(employees, 'last_f', domain, outfile)



def create_user_list(file_name):
    '''
    Read full names from the file and store
    it inside a list
    '''
    file = open(file_name, 'r')
    content = file.readlines()
    employee_list = []
    for user in content:
        employee_list.append(user.strip())
    return employee_list


def main():
    """Main Function"""
    args = parse_arguments()

    
    employees = create_user_list(args.file)

    # Write the data to some files.
    write_files(args.company, args.domain, employees, args.output)

    # Time to get hacking.
    print(f"\n\n[*] All done! Check out your lovely new files in {args.output}")


if __name__ == "__main__":
    main()