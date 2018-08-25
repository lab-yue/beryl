import os
from component import Component
from page import Page
from config import Config


class Engine(object):
    def __init__(self):

        self.base_html = ''
        self.base_component = None
        self.config = Config()
        self.components = {}
        self.pages = {}

    def run(self):
        self.config.load()

        print('config loaded')

        with open(self.config.source_path + 'index.html', 'r') as base:
            self.base_html = base.read()

        self.base_component = Component(self.config.source_path + 'App.vue', self)

        self.register_components()
        print('components registered')
        self.resolve_nested_components()
        self.base_component.resolve()
        self.make_dirs()

        self.make_pages()

        print('pages made')
        self.compile_sass()
        print('sass compiled')
        print('done')

    def make_dirs(self):
        if not os.path.isdir('../build'):
            os.mkdir('../build')
            os.mkdir('../build/statics')
            os.mkdir('../build/statics/img')
            os.mkdir('../build/statics/js')
            os.mkdir('../build/statics/css')
            os.system(f'cp -r {self.config.scss_path} ../build/statics/scss')

    def test(self):
        self.run()
        # print(self.components['<PageFooter/>'].style)
        # print(self.pages['About'].style)

    def compile_sass(self):
        os.chdir(self.config.out_path + 'statics')
        os.system('sass --update scss:css --style compressed')

    def register_components(self):
        components = [file for file in os.listdir(self.config.components_path)
                      if file.endswith('.vue')]
        [self.register_component(component) for component in components]

    def register_component(self, filename):
        name = filename.rsplit('.')[0]
        self.components[f"<{name}/>"] = Component(self.config.components_path + filename, self)

    def resolve_nested_components(self):
        for component in self.components:
            self.components[component].resolve()

    def make_pages(self):
        pages = [file for file in os.listdir(self.config.pages_path)
                 if file.endswith('.vue')]
        for page in pages:
            name = page.rsplit('.')[0]
            self.pages[name] = Page(self.config.pages_path + page, self)

        for page in self.pages:
            self.pages[page].make()


if __name__ == '__main__':
    engine = Engine()
    engine.test()
