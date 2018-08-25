import re


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
