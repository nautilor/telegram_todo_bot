#!/usr/bin/env python3

import uuid
from .config import config

class todo_handler:
    def __init__(self):
      self.config = config();

    def generate_todo_key(self):
        return str(uuid.uuid1())[:8]

    def get_todos(self, user):
        return self.config.get_user(user)['todos']

    def complete_todo(self, user, key):
        todos = self.get_todos(user)
        todos[key]['done'] = 1
        self.config.update()

    def delete_todo(self, user, todo):
        todos = self.get_todos(user)
        todos.pop('key')
        self.config.update()
