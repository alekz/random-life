#!/usr/bin/python
import sys
import argparse
from life.gui import LifeApplication
from life.manager import LifeManager, RandomLifeManager

presets = {
    'gnarl': ((1,), (1,), 'Gnarl'),
    'coral': ((3,), (4, 5, 6, 7, 8), 'Coral'),
    'replicator': ((1, 3, 5, 7), (1, 3, 5, 7), 'Replicator'),
    'seeds': ((2, ), (), 'Seeds'),
    'serviettes': ((2, 3, 4), (), 'Serviettes'),
    'nodeath': ((3, ), (0, 1, 2, 3, 4, 5, 6, 7, 8), 'Life without Death'),
    'assimilation': ((3, 4, 5), (4, 5, 6, 7), 'Assimilation'),
    'long': ((3, 4, 5), (5, ), 'Long Life'),
    'diamoeba': ((3, 5, 6, 7, 8), (5, 6, 7, 8), 'Diamoeba'),
    '2x2': ((3, 6), (1, 2, 5), '2x2'),
    'stains': ((3, 6, 7, 8), (2, 3, 5, 6, 7, 8), 'Stains'),
    'walled': ((4, 5, 6, 7, 8), (2, 3, 4, 5), 'Walled Cities'),
    'coagulations': ((3, 7, 8), (2, 3, 5, 6, 7, 8), 'Coagulations'),
    'move': ((3, 6, 8), (2, 4, 5), 'Move'),
    'daynight': ((3, 6, 7, 8), (3, 4, 6, 7, 8), 'Day & Night'),
    'amoeba': ((3, 5, 7), (1, 3, 5, 8), 'Amoeba'),
    'pseudo': ((3, 5, 7), (2, 3, 8), 'Pseudo Life'),
    '34': ((3, 4), (3, 4), '34 Life'),
    'highlife': ((3, 6), (2, 3), 'HighLife'),
    'maze': ((3, ), (1, 2, 3, 4, 5), 'Maze'),
    'classic': ((3, ), (2, 3), 'Classic Life'),
}

default_preset = 'classic'

def parse_args():

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-r', '--no-random', dest='no_random', action='store_true', default=False,
                        help="disables randomness and colors (enables classic Life rules)")

    parser.add_argument('-w', '--width', dest='width', type=int, default=100,
                        help="width of the field (default = %(default)s)")

    parser.add_argument('-e', '--height', dest='height', type=int, default=100,
                        help="height of the field (default = %(default)s)")

    parser.add_argument('-f', '--fps', dest='fps', type=int, default=60,
                        help="frames per second, (default = %(default)s)")

    presets_help = '\n'.join(sorted('  {0} - {1}'.format(name, title) for name, (_, _, title) in presets.items()))
    parser.add_argument('-t', '--type', dest='preset', metavar='TYPE',
                        choices=presets.keys(), default=default_preset,
                        help="the type of Life (default = %(default)s):\n" + presets_help)

    return parser.parse_args()

def run_life():
    args = parse_args()
    preset = presets[args.preset]
    if args.no_random:
        life_manager = LifeManager
    else:
        life_manager = RandomLifeManager
    life = life_manager(args.width, args.height, born_if=preset[0], alive_if=preset[1])
    app = LifeApplication(life, fps=args.fps)
    sys.exit(app.exec_())

if __name__ == '__main__':
    run_life()
