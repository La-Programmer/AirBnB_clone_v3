#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

first_state_id = list(storage.all(State).values())[0].id
print("First state: {}".format(storage.get(State, first_state_id)))

dict = {'name': "Texas"}

new_state = State(name="Texas")
print(f"New State: {new_state}")
print(f"New State type: {type(new_state)}")
id = new_state.id
# print(id)
new_state.save()
print("Getting new state: {}".format(storage.get(State, id)))
