from modules.user import user

# class print_user():
#     def __init__(self) -> None:
#         self = user()
#         print(self.login_url)
#         #return User
        
#     def print_name(self):
#         #User = self.User
#         print(self.username)
 
# # print_user()       
# # print_user.print_name()

# a = print_user()
# a.print_name()

# class Person():
#     def __init__(self, vor, nach) -> None:
#         self.vor = vor
#         self.nach = nach
        
#     def pr_per(self):
#         print("Vor:  %s, Nach:  %s" % (self.vor, self.nach)) 
        
# x = Person('ch', 'k')
# x.pr_per()

#### dependency injection
class testUser():
    def __init__(self, user_config) -> None:
        # vars() creates dict, items() select key, value pairs       
        for key, value in vars(user_config).items():
            setattr(self, key, value)
    
    def ptu(self):
        print(self.username)
            

testUser(user()).ptu()
#print_attributes(a)
#attributes = vars(a)
#print(attributes)
#testUser.ptu(a)
#print(a.username)