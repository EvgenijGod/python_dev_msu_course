from __future__ import absolute_import

import argparse
import sys, cmd, shlex
from cowsay import cowsay, list_cows, cowthink, THOUGHT_OPTIONS, make_bubble


def get_cow_params(arg):
    # message, cow, eyes, tongue
    options = shlex.split(arg)
    option_def_values = {
        "message": options[0],
        "cow": "default",
        "eyes" : "oo",
        "tongue" : "  "
    }
    for i in range(1, len(options)):
        if options[i].startswith("--") and options[i][2:] in option_def_values:
            option_def_values[options[i][2:]] = options[i + 1]
    return option_def_values


def get_bubble_params(arg):
    # message, brackets, width, wrap_text
    options = shlex.split(arg)
    option_def_values = {
        "message": options[0],
        "brackets": THOUGHT_OPTIONS['cowsay'],
        "width" : 40,
        "wrap_text" : False
    }
    for i in range(1, len(options)):
        if options[i] == "--brackets":
            option_def_values["brackets"] = THOUGHT_OPTIONS[options[i + 1]]
        elif options[i] == "--width":
            option_def_values["width"] = int(options[i + 1])
        elif options[i] == "--wrap_text":
            option_def_values["wrap_text"] = bool(options[3] == "true")
    print(option_def_values)
    return option_def_values


class CowSay(cmd.Cmd):
    intro = 'Let\'s make some cowsay\n'
    prompt = '(Moooo)'

    def do_exit(self, arg):
        print('Bye Bye')
        return True

    def do_list_cows(self, arg):
        """
        list_cows [dir]
        Lists all cow file names in the given directory or default cow list
        """
        print(shlex.split(arg))
        if len(arg) != 0:
            print(list_cows(shlex.split(arg)[0]))
        else:
            print(list_cows())

    def do_cowsay(self, arg):
        '''
        cowsay message [cow, eyes, tongue]
        Makes cow say
        '''
        parsed = get_cow_params(arg)
        print(cowsay(parsed['message'], cow=parsed['cow'], eyes=parsed['eyes'], tongue=parsed['tongue']))
    
    def do_cowthink(self, arg):
        '''
        cowsay message [cow, eyes, tongue]
        Makes cow think and say
        '''
        parsed = get_cow_params(arg)
        print(cowthink(parsed['message'], cow=parsed['cow'], eyes=parsed['eyes'], tongue=parsed['tongue']))

    def do_make_bubble(self, arg):
        '''
        make_buble [wrap_text, width, brackets ]
        Makes cow bubbling and saying
        '''
        parsed = get_bubble_params(arg)
        print(make_bubble(parsed['message'], brackets=parsed['brackets'], width=parsed['width'], wrap_text=parsed['wrap_text']))

if __name__ == '__main__':
    CowSay().cmdloop()
