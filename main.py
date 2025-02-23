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


def list_tasks(tasks=None):
    tasks_list = read_tasks() if tasks is None else tasks
    return "\n".join(
        [f"{task['id']}. {task['task']} - {task['status']}" for task in tasks_list]
    )


def create_id():
    no_of_tasks = len(read_tasks())
    return no_of_tasks + 1


def create_task(task, is_first_task=False):
    return {
        "id": 1 if is_first_task else create_id(),
        "task": task,
        "status": "todo",
        "createdAt": int(time.time()),
    }


def write_to_json(task):
    with open(json_path, "r+") as file:
        if os.path.exists(json_path) and os.path.getsize(json_path) == 0:
            json.dump([create_task(task, True)], file)
        else:
            tasks = read_tasks()
            tasks.append(create_task(task))
            json.dump(tasks, file)


def write_tasks_to_json(tasks):
    with open(json_path, "w") as file:
        json.dump(tasks, file)


def update_task(task_id):
    tasks = read_tasks()
    if task_id not in range(1, len(tasks) + 1):
        print("Task number doesn't exist.")
    else:
        new_task = input("Please enter new task: ")
        for t in tasks:
            if t["id"] == task_id:
                t["task"] = new_task
                break
        write_tasks_to_json(tasks)
        print(list_tasks(tasks))


def delete_task(task_id):
    tasks = read_tasks()
    if task_id not in range(1, len(tasks) + 1):
        print("Task number doesn't exist.")
    else:
        while True:
            confirm = input("Are you sure? (yes/no): ").strip().lower()
            if confirm in ("yes", "y"):
                new_tasks = [task for task in tasks if task["id"] != task_id]
                for index, task in enumerate(new_tasks, start=1):
                    task["id"] = index
                write_tasks_to_json(new_tasks)
                print(list_tasks(new_tasks))
                break
            elif confirm in ("no", "n"):
                print("Cancelled!")
                break
            else:
                print("Please enter 'yes' or 'no'.")


def get_int_arg(args, index):
    try:
        return int(args[index])
    except (IndexError, ValueError):
        return None  # Return None or a default value


def take_input(arg):
    if arg[0] == "add":
        # check if task exists
        task = args[1]
        write_to_json(task)

    elif arg[0] == "list":
        print(list_tasks())

    elif arg[0] == "update":
        # check if task exists
        if len(args) != 2:
            print("Please try again with a valid id. eg- update 1")
        else:
            task = get_int_arg(args, 1)
            if task is None:
                print("Invalid task number!")
            else:
                update_task(task)

    elif arg[0] == "delete":
        # check if task exists
        if len(args) != 2:
            print("Please try again with a valid id. eg- update 1")
        else:
            task = get_int_arg(args, 1)
            if task is None:
                print("Invalid task number!")
            else:
                delete_task(task)

    # else:
    #   name = input("Please enter your task:")
    #   print(name[1])


take_input(args)
