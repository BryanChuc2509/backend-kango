# service.py
from flask import jsonify

class UserService:
    def __init__(self):
        self.users = [
            {"id": 1, "name": "Juan", "age": 25},
            {"id": 2, "name": "Ana", "age": 30},
            {"id": 3, "name": "Carlos", "age": 35},
        ]

    def get_users(self):
        return jsonify(self.users)

    def get_user(self, user_id):
        for user in self.users:
            if user["id"] == user_id:
                return jsonify(user)
        return jsonify({"error": "Usuario no encontrado"}), 404

    def add_user(self, name, age):
        for user in self.users:
            if user["name"] == name and user["age"] == age:
                return jsonify({"error": "Usuario ya registrado"}), 400
        new_user = {"id": len(self.users) + 1, "name": name, "age": age}
        self.users.append(new_user)
        return jsonify(new_user), 201