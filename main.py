import os
import sys
import json
import time

json_path = "tasks.json"
tasks = []

args = sys.argv[1:]

def read_tasks():
  with open(json_path, "r") as file:
    return json.load(file)

def list_tasks():
  tasks = read_tasks()
  return "\n".join([f"{task['id']}. {task['task']} - {task['status']}" for task in tasks])

def create_id():
  no_of_tasks = len(read_tasks())
  return no_of_tasks + 1

def create_task(task, is_first_task=False):
  return {
    "id": 1 if is_first_task else create_id(),
    "task": task,
    "status": "todo",
    "createdAt": int(time.time())
  }


def write_to_json(task):
  with open(json_path, "r+") as file:
    if os.path.exists(json_path) and os.path.getsize(json_path) == 0:
      json.dump([create_task(task, True)], file)
    else:
      tasks = read_tasks()
      tasks.append(create_task(task))
      json.dump(tasks, file)

def update_task(task_id, new_task):
  tasks = read_tasks()
  for t in tasks:
    if t["id"] == task_id:
      t["task"] = new_task
      break
  with open(json_path, "w") as file:
    json.dump(tasks, file)



def take_input(arg):
  if arg[0] == "add":
    # check if task exists
    task = args[1]
    write_to_json(task)
  elif arg[0] == "list":
    print(list_tasks())
  elif arg[0] == "update":
    # check if task exists
    task = int(args[1])
    new_task = input("Please enter new task: ")
    update_task(task, new_task)

  # else:
  #   name = input("Please enter your task:")
  #   print(name[1])

take_input(args)
