import yaml

class Config:

    def __init__(self, config_yaml):
        with open(config_yaml) as f:
            data = yaml.safe_load(f)
            self.host = data["host"]
            self.port = data["port"]
            self.user = data["user"]
            self.password = str(data["password"])

            self.user_home = data["user_home"]
            self.working_folder = data["working_folder"]

            self.folder_in = str(data["folder_in"])\
                .replace("${user_home}", self.user_home)\
                .replace("${working_folder}", self.working_folder)

            self.archive = data["archive"]
            self.archive_error = data["archive_error"]
            self.folder_ext = str(data["folder_ext"]).replace("${user_home}", self.user_home)
            self.folder_ext2 = str(data["folder_ext2"]).replace("${user_home}", self.user_home)
            self.count = data["count"]
            self.bs = data["bs"]
            self.type = data["type"]