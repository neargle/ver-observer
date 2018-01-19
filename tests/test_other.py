
import os
import sys
import inspect

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utils.log import LOGGER as logger

def main():
    filter_word = ''
    try:
        filter_word = sys.argv[1]
    except IndexError:
        pass

    current_module = sys.modules[__name__]
    for member, module in inspect.getmembers(current_module):
        if member.endswith('_test') and filter_word in member:
            logger.noise("test function: %s, module: %s", member, str(module))
            getattr(current_module, member)()


if __name__ == '__main__':
    main()
