import pkg_resources

from . import BrummiRepository

DEFAULTS = {
    'templates': pkg_resources.resource_filename('brummi', 'templates'),
    'out_path': 'docs',
}

class Config(object):
    def __init__(self, options):
        self.options = DEFAULTS.copy()
        self.options.update(options)

    def launch(self):
        repo = BrummiRepository(
            self.options['ooc_path'],
            self.options['templates'],
            self.options['out_path']
            )
        repo.build_all_modules()
