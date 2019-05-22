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

    def add_todo(self, user, todo):
        try:
            key = self.generate_todo_key()
            todos = self.get_todos(user)
            todos[todo] = {'description': todo, 'done': 0}
            self.config.update()
        except Exception:
            return

    def complete_todo(self, user, key):
        try:
            todos = self.get_todos(user)
            todos[key]['done'] = 1
            self.config.update()
        except Exception:
            return

    def delete_todo(self, user, todo):
        try:
            todos = self.get_todos(user)
            todos.pop(todo)
            self.config.update()
        except Exception:
            return
