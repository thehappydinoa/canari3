#!/usr/bin/env python

import os

from mrbob.configurator import Configurator
from mrbob.parsing import parse_config

from common import canari_main, project_tree
from framework import SubCommand, Argument

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.4'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


def parse_args(args):
    if args.transform in ['common', 'common.py']:
        print "Error: 'common' is a reserved module. Please name your transform something else."
        exit(-1)
    return args


@SubCommand(
    canari_main,
    help='Creates a new transform in the specified directory and auto-updates __init__.py.',
    description='Creates a new transform in the specified directory and auto-updates __init__.py.'
)
@Argument(
    'transform',
    metavar='<transform name>',
    help='The name of the transform you wish to create.'
)
def create_transform(args):

    opts = parse_args(args)

    transform_module = (opts.transform if not opts.transform.endswith('.py') else opts.transform[:-3]).lower()
    transform_name = ''.join([i.title() for i in transform_module.split('_')])

    if '.' in transform_module:
        print("Transform name (%r) cannot have a dot ('.')." % transform_name)
        exit(-1)
    elif not transform_module:
        print("You must specify a valid transform name.")
        exit(-1)

    target = project_tree()['root']
    transform_directory = project_tree()['transforms']

    if os.path.exists(os.path.join(transform_directory, '%s.py' % transform_module)):
        print('Transform %r already exists... quitting' % transform_module)
        exit(-1)

    variables = parse_config(os.path.join(target, '.mrbob.ini'))['variables']

    variables.update({'transform.module': transform_module, 'transform.name': transform_name})

    configurator = Configurator(
        'canari.resources.templates:create_transform',
        target,
        {'non_interactive': True},
        variables=variables
    )

    configurator.ask_questions()
    configurator.render()

    print('done!')
