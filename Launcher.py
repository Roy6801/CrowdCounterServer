import os

print("\n\n********** Installing Requirements *********")
os.system('pip3 install virtualenv')
os.chdir(os.getcwd()+'/ccs')
os.system('virtualenv --system-site-packages venv_gpu')
os.system('venv_gpu\\Scripts\\pip3 install -r requirements.txt')
print("\n\n********** Initializing *********")
os.system('heroku login -i')
os.system('venv_gpu\\Scripts\\python Host.py')
