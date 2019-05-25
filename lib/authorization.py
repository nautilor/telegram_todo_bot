#!/usr/bin/env python3

from .config import config

class authorization:
    def __init__(self):
        self.config = config()

    def is_authorized(self, user):
        self.config.load_config()
        return str(user) in self.config.users()

    def is_admin(self, user):
        self.config.load_config()
        return "ADMIN" in self.config.get_user(str(user))['capabilities']

    def has_access(self, user, capability):
        self.config.load_config()
        return capability in self.config.get_user_capabilities(str(user))

