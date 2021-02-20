import os

print("\n\n********** Installing Requirements *********")
os.system('pip3 install virtualenv')
os.chdir(os.getcwd()+'/ccs')
os.system('virtualenv venv_local')
os.system('venv_local\\Scripts\\pip3 install -r requirements.txt')
print("\n\n********** Initializing *********")
os.system('venv_local\\Scripts\\python Host.py')
