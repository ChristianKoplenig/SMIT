from modules.user import user

#### dependency injection
class testUser():
    def __init__(self, UserClass: user) -> None:
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
    
    def ptu(self):
        print(self.login_url)
            
    def __repr__(self) -> dict:
        print(vars(self))
        return self.username

#testUser(user()).ptu()

a = user()
#testUser(a).ptu()

print(type(a))

#print(testUser(a))
#print_attributes(a)
#attributes = vars(a)
#print(attributes)
#testUser.ptu(a)
#print(a.username)