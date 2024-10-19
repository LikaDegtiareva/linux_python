import yaml


class Post:
    def __init__(self, config_yaml):
        with open(config_yaml, 'r') as input:
            data = yaml.safe_load(input)
            self.title = data['post']['title']
            self.description = data['post']['description']
            self.content = data['post']['content']

    #def json(self):
    #    return json.dumps(self.__dict__)

    def payload(self):
        return {'title': self.title, 'description': self.description, 'content': self.content}