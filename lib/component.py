import re
import os


class Component(object):
    def __init__(self, filename, engine):
        with open(filename, 'r') as f:
            self.file = f.read()

        self.name = filename.split('/')[-1]

        self.__template_reg = re.compile('<template>([\s\S]+?)</template>')
        self.__style_reg = re.compile('<style[\s\S]+?>([\s\S]+?)</style>')
        self.__classname_reg = re.compile('(class="[\s\S]+?")/>')

        self.template = re.findall(self.__template_reg, self.file)[0]  # .group()
        self.style = re.findall(self.__style_reg, self.file)[0]  # .group()
        self.engine = engine
        self.output_html = ''
        self.output_style = ''
        self.style_set = []

    def resolve(self):
        for nested_name in self.engine.components:

            ori_reg = nested_name.replace('/>', '[\s\S]*?/>')

            nested = re.findall(ori_reg, self.template)

            if nested:
                print(nested_name, ' in ', self.name)
                self.update(nested[0],
                            self.engine.components[nested_name].template)

                if nested_name not in self.style_set:
                    # self.style = self.style + self.engine.components[nested_name].style
                    # self.style_set.append(nested_name)
                    self.style_set.extend(self.engine.components[nested_name].style_set)
                    self.style_set.append(nested_name)

        self.style_set = list(set(self.style_set))

    def update(self, origin, inside):

        classes = re.findall(self.__classname_reg, origin)

        # print(classes)

        inner_html = self.make_div(classes, inside)

        self.template = self.template.replace(origin, inner_html)

    @staticmethod
    def make_div(classes, inside):
        # print(el)
        # inner_html
        if not classes:
            classes = ''
        else:
            classes = classes[0]
        inner_html = f"<div {classes}> {inside}</div>"
        # print(inner_html)

        return inner_html


class Page(Component):
    def __init__(self, page_name, engine):
        super().__init__(page_name, engine)
        self.base_html = engine.base_html
        self.engine = engine
        self.title_reg = re.compile('<title>([\s\S]+?)</title>')
        self.import_reg = re.compile('@import[\s\S]+?scss";')
        self.title = self.name.rsplit('.', 1)[0].lower()
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

        self.css_link = f'<link href="../statics/css/{self.title}.css" rel="stylesheet"/>'

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

        os.mkdir(html_file_name)

        with open(html_file_name + '/index.html', 'w') as html:
            html.write(self.output_html)

        with open(scss_file_name + '.scss', 'w') as scss:
            scss.write(self.output_style)
