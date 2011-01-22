import os

import jinja2
import markdown2
from pyooc.parser import Repository, Module
from pyooc.parser.tag import parse_string as parse_tag, translate

REPO = None

def markdown_doc(member):
    return MARKDOWN.convert(member.doc, member)

def resolve_tag(tag, cb=lambda x:x):
    if '(' in tag:
        mod, args = parse_tag(tag)
        if mod == 'pointer':
            return resolve_tag(translate(args[0]), cb) + '*'
        elif mod == 'reference':
            return resolve_tag(translate(args[0]), cb) + '@'
        elif mod == 'multi':
            return '(' + ', '.join(resolve_tag(translate(arg), cb) for arg in args) + ')'
        elif mod == 'Func':
            return cb('Func') # TODO: specialized functions
        else:
            return 'dunno'
    else:
        return cb(tag)

def link_tag(member, tag):
    def cb(t):
        crosslink = REPO.resolve_crosslink(member, t)
        if crosslink:
            return '<a href="%s">%s</a>' % (crosslink, t) # no need to escape i think. TODO?
        else:
            return t
    return resolve_tag(tag, cb)

def is_parent(member):
    return hasattr(member, 'members')

def is_node(member, *names):
    return any(any(cls.__name__.lower() == n for n in names) for cls in member.__class__.mro())

class MarkdownWithBenefits(markdown2.Markdown):
    def convert(self, text, member=None):
        self._member = member
        return markdown2.Markdown.convert(self, text)

    def _code_span_sub(self, match):
        """
            Actually make them links if possible.
        """
        contents = match.group(2).strip(' \t')
        code = self._encode_code(contents)
        if self._member:
            crosslink = REPO.resolve_crosslink(self._member, contents)
            if crosslink:
                code = '<a href="%s">%s</a>' % (crosslink, code)
        return '<code>%s</code>' % code

MARKDOWN = MarkdownWithBenefits()

class BrummiRepository(Repository):
    def __init__(self, ooc_path, jinja_path, out_path):
        Repository.__init__(self, ooc_path)
        self.modules = None
        self.out_path = out_path
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(jinja_path)
        )
        self.jinja_env.filters['markdown_doc'] = markdown_doc
        self.jinja_env.filters['resolve_tag'] = resolve_tag
        self.jinja_env.filters['link_tag'] = link_tag
        self.jinja_env.filters['anchor'] = self.get_anchor
        self.jinja_env.tests['parent'] = is_parent
        self.jinja_env.tests['node'] = is_node

    def resolve_crosslink(self, member, contents):
        resolved = member.resolve_name(contents)
        if resolved:
            module = member.get_module()
            return REPO.get_link(resolved, module)
        else:
            return None

    def get_anchor(self, member):
        anchor = []
        while not isinstance(member, Module):
            anchor.insert(0, member.name)
            member = member.parent
        return '-'.join(anchor)

    def get_link(self, member, start_module=None):
        path = [self.get_anchor(member)]
        if path[0]:
            path.insert(0, '#')
        path.insert(0, '.html')
        path.insert(0, member.get_module().path)
        if start_module is None:
            return '/' + ''.join(path)
        else:
            return os.path.relpath(''.join(path), os.path.dirname(start_module.path + '.html'))

    def get_out_path(self, module):
        path = os.path.join(self.out_path, module.path + '.html')
        dirpath = os.path.dirname(path)
        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)
        return path

    def build_module(self, module):
        template = self.jinja_env.get_template('module.html')
        output = template.render(module=module, modules=self.modules)
        with open(self.get_out_path(module), 'w') as f:
            f.write(output)

    def build_all_modules(self):
        self.modules = self.get_all_modules().values()
        for module in self.modules:
            self.build_module(module)

def main(ooc_path, jinja_path, out_path):
    global REPO
    repo = REPO = BrummiRepository(ooc_path, jinja_path, out_path)
    repo.build_all_modules()
