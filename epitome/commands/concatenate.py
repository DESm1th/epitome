#!/usr/bin/env python

import copy

def run(input_name):
    output = copy.copy(input_name) # return output unharmed

    print('\nConcatenating input runs.')

    line = ('. ${DIR_PIPE}/epitome/modules/pre/concatenate ' + str(input_name))

    return line, output
