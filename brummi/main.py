import sys

import pkg_resources

from . import main

def run_brummi():
    try:
        repo_path = sys.argv[1]
        out_path = sys.argv[2]
    except IndexError:
        print 'Usage: brummi REPO_PATH OUT_PATH'
        return 0
    jinja_path = pkg_resources.resource_filename('brummi', 'templates')
    print jinja_path
    main(repo_path, jinja_path, out_path)
