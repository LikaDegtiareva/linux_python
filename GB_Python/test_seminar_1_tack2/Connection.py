import yaml

class Connection:
    def __init__(self, config_yaml):
        with open(config_yaml, 'r') as input:
            data = yaml.safe_load(input)
            self.host = data['connection']['host']
            self.password = data['connection']['password']
            self.username = data['connection']['username']