from modules.user import user

# I tought this is the better approach because we can see 
# which variable is the attribute for the class.
class UnzipClass():
    """Get class object as attribute and unzip it in __init__ procedure.
    """
    def __init__(self, UserClass: 'modules.user.user') -> None:
        """Initialize Class with all attributes from `UserClass`
        Parameters
        ----------
        UserClass : class type
            User data initiated via `user()` function from user module            
        """
        # vars() creates dict 
        # items() iterate over key/value pairs       
        for key, value in vars(UserClass).items():
            setattr(self, key, value)

    def print_UnzipClass(self):
        print('UnzipClass: ' + self.username)

    def self_print(self):
        print('easy print')
        self.print_UnzipClass()

# With this we have to import a global variable and it's hardcoded in all classes.
# I don't know if there are better solutions for importing variables into classes. 
class ZipClass():
    """Import global variable and use it directly
    """
    global User
        
    def print_ZipClass(self):
        print('ZipClass: ' + User.username) 

##### run #####        
User = user()

UnzipClass(User).print_UnzipClass()
ZipClass().print_ZipClass()

# For further readability I was thinking about something like this 
# combined with a setup script. This works indipendently 
# of the way we import the user class anyway.

active_user = UnzipClass(User)
active_user.print_UnzipClass()
active_user.self_print()