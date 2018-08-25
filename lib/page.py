from component import Component
import re


class Page(Component):
    def __init__(self, page_name, engine):
        super().__init__(page_name, engine)
        self.base_html = engine.base_html
        self.engine = engine
        self.title_reg = re.compile('<title>([\s\S]+?)</title>')
        self.import_reg = re.compile('@import[\s\S]+?scss";')
        self.title = self.name.rsplit('.', 1)[0]
        self.css_link = ''

    def make(self):

        print(f'making {self.title}')
        self.make_html()
        self.make_style()
        self.write()

    def make_html(self):
        self.output_html = self.base_html.replace('<div id="app"></div>',
                                                  self.engine.base_component.template)
        self.resolve()

        self.css_link = f'<link href="./statics/css/{self.title}.css" rel="stylesheet"/>'

        self.output_html = re.sub(self.title_reg,
                                  lambda x: f'''<title>{self.title}</title>
                                  {self.css_link}
                                  ''',
                                  self.output_html)
        self.output_html = self.output_html.replace('<router-view/>', self.template)

    def make_style(self):
        self.output_style += self.engine.base_component.style

        for each in self.engine.base_component.style_set:
            self.output_style += self.engine.components[each].style

        self.output_style += self.style
        scss_imports = re.findall(self.import_reg, self.output_style)
        scss_imports = list(set(scss_imports))
        for each in scss_imports:
            self.output_style = re.sub(each, '', self.output_style)
        self.output_style = '\n'.join(scss_imports) + self.output_style

    def write(self):
        html_file_name = self.engine.config.out_path + self.title
        scss_file_name = self.engine.config.out_path + '/statics/scss/' + self.title

        with open(html_file_name + '.html', 'w') as html:
            html.write(self.output_html)

        with open(scss_file_name + '.scss', 'w') as scss:
            scss.write(self.output_style)
