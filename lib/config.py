#!/usr/bin/env python3 

import json

class config:
    def __init__(self):
        self.config_file = 'config/config.json'
        self.config = None
        self.load_config()

    def get_storage_path(self):
        return self.config['bot']['storage_path']

    def get_user(self, user):
        user = str(user)
        return self.users()[user]

    def get_user_capabilities(self, user):
        return self.get_user(user)['capabilities']

    def load_config(self):
        self.config = open(self.config_file, 'r')
        self.config = json.load(self.config)

    def users(self):
        return self.config['users']

    def get_bot_api(self):
        return self.config['bot']['api']

    def update(self):
        with open(self.config_file, 'w') as file:
            json.dump(self.config, file)
