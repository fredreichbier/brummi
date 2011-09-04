import sys
import json
import pkg_resources

from .config import Config

def run_brummi():
    try:
        cfg_path = sys.argv[1]
    except IndexError:
        print 'Usage: brummi config.json'
        return 0
    with open(cfg_path, 'r') as f:
        cfg = Config(json.load(f))
    cfg.launch()
