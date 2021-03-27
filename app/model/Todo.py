class Todo:
    def __init__(self, todo_id, name, description, is_done, user_id):
        self.todo_id = todo_id
        self.name = name
        self.description = description
        self.user_id = user_id
        self.is_done = is_done is not None and is_done > 0
