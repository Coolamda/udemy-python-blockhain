import json
import pickle

ask_user_for_input = True
user_input_list = []


while ask_user_for_input:
    print("1) Write to file.")
    print("2) Print out file.")
    print("q) Exit.")
    user_choice = input("Your Choice: ")
    if user_choice == "1":
        user_input = input("Enter some text: ")
        with open("module_7_tasks.p", mode="wb") as f:
            user_input_list.append(user_input)
            f.write(pickle.dumps(user_input_list))
    elif user_choice == "2":
        with open("module_7_tasks.p", mode="rb") as f:
            file_content = pickle.loads(f.readline())
            for line in file_content:
                print(line)
    elif user_choice == "q":
        ask_user_for_input = False
