import json


class Config(object):
    def __init__(self):
        self.config_path = '../config.json'

        self.base = 'App.vue'

        self.source_path = ''
        self.out_path = ''
        self.scss_path = ''
        self.pages_path = ''
        self.components_path = ''

    def load(self):
        with open(self.config_path, 'r') as cnf:
            __config = json.loads(cnf.read())

        self.source_path = __config.get('ENTRY')
        self.out_path = __config.get('OUTPUT')
        self.pages_path = self.source_path + __config.get('PAGES')
        self.components_path = self.source_path + __config.get('COMPONENTS')
        self.scss_path = self.source_path + __config.get('SCSS')
