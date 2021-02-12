import os

print("\n\n********** Installing Requirements *********")
os.system('pip3 install virtualenv')
os.chdir(os.getcwd()+'/ccs')
os.system('virtualenv venv')
os.system('venv\\Scripts\\pip3 install -r requirements.txt')
print("\n\n********** Initializing *********")
os.system('heroku login -i')
os.system('venv\\Scripts\\python Host.py')
