import os

import jinja2
import markdown2
from pyooc.parser import Repository, Module

REPO = None

def markdown_doc(member):
    return MARKDOWN.convert(member.doc, member)

def is_parent(member):
    return hasattr(member, 'members')

class MarkdownWithBenefits(markdown2.Markdown):
    def convert(self, text, member=None):
        self._member = member
        return markdown2.Markdown.convert(self, text)

    def _code_span_sub(self, match):
        """
            Actually make them links if possible.
        """
        contents = match.group(2)
        if self._member is not None:
            resolved = self._member.resolve_name(contents)
            if resolved:
                module = self._member.get_module()
                return '<a href="%s">%s</a>' % (REPO.get_link(resolved, module), '<code>%s</code>' % contents)
        return markdown2.Markdown._code_span_sub(self, match)

MARKDOWN = MarkdownWithBenefits()

class BrummiRepository(Repository):
    def __init__(self, ooc_path, jinja_path, out_path):
        Repository.__init__(self, ooc_path)
        self.out_path = out_path
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(jinja_path)
        )
        self.jinja_env.filters['markdown_doc'] = markdown_doc
        self.jinja_env.tests['parent'] = is_parent

    def get_link(self, member, start_module=None):
        path = ['.html']
        while not isinstance(member, Module):
            path.insert(0, member.name)
            member = member.parent
        if len(path) > 1:
            path.insert(0, '#')
        path.insert(0, member.path)
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
        output = template.render(module=module)
        with open(self.get_out_path(module), 'w') as f:
            f.write(output)

    def build_all_modules(self):
        for path, module in self.get_all_modules().iteritems():
            self.build_module(module)

def main(ooc_path, jinja_path, out_path):
    global REPO
    repo = REPO = BrummiRepository(ooc_path, jinja_path, out_path)
    repo.build_all_modules()
