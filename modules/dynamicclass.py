'''
Dynamically creates an instance of class 'User' based on variables from user_data file
Input:
    - path to user data file
    - name for the class
    
code generated by chatgpt
'''
class DynamicClass:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

def create_class_from_file(file_path, class_name):
    variables = {}
    with open(file_path, "r") as file:
        code = compile(file.read(), file_path, "exec")
        exec(code, variables)
    
    CustomClass = type(class_name, (DynamicClass,), variables)
    return CustomClass()

def create_user():
    return create_class_from_file('/media/data/coding/strom/user_data.py', 'User')
