#!/usr/bin/python

import sys
import argparse
import subprocess

DESCRIPTION = """Minimalist Xargs for Windows, currently following options
are implemented:

    -I              replace_str
    -t, --verbose   Verbose mode

Example:
    * Create str(s) to operate on and write to a file
        echo hi> test.txt
        echo there>>test.txt
        echo how?>>test.txt
        
    * Pipe the contents of the text file to the file to execute:
        type test.txt | xargswin.exe -I{} "echo {}"

    * Alternatively, query string does not need to be specified:
        type test.txt | xargswin.exe echo {}
"""

def parse_user_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-I", dest="replace_str", action="store",
                        help="replace-str")
    parser.add_argument("-t","--verbose", dest="verbose_mode",
                        action="store_true", help="verbose mode")
    parser.add_argument(metavar="cmd with args", nargs="+", dest="cmd_with_args",
                        action="store", help="command to execute with user arguments",
                        type=str)
    args = parser.parse_args()
    replace_str = args.replace_str
    verbose_mode = args.verbose_mode
    cmd_with_args = args.cmd_with_args
    
    return (replace_str, verbose_mode, cmd_with_args)

def validate_user_args(replace_str, verbose_mode, cmd_with_args):
    verbose_mode_validated = verbose_mode
    replace_str_validated = replace_str    
    cmd_with_args_validated = ' '.join(cmd_with_args)
    
    return (replace_str_validated, verbose_mode_validated, cmd_with_args_validated)

def apply_cmd(piped_input, replace_str, cmd_to_exec_template, verbose):
    for item in piped_input.split("\n"):
        if replace_str:
            cmd_to_exec = cmd_to_exec_template.replace(replace_str, item)
        else:
            cmd_to_exec = cmd_to_exec_template + " " + item
        
        try:
            p = subprocess.Popen(cmd_to_exec, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, shell=True)
            if verbose:
                print "[*] Executing '" + cmd_to_exec + "'"
            (out, err) = p.communicate()
            if err:
                print err.strip()
            if out:
                print out.strip()
        except WindowsError as e:
            print "[-] WindowsError: " + str(e)
            
if __name__ == "__main__":
    
    # Parser user-provided arguments
    replace_str, verbose_mode, cmd_with_args = parse_user_args()

    # Take user input via pipe, or directly from stdin
    piped_input = sys.stdin.read().strip()

    # Perform any necessary filtering on user-provided arguments
    replace_str, verbose_mode, cmd_with_args = validate_user_args(replace_str, verbose_mode,
                                                                  cmd_with_args)

    # Apply the command on each line of the piped input
    apply_cmd(piped_input, replace_str, cmd_with_args, verbose_mode)

