import os

print("\n\n********** Installing Requirements *********")
os.system('pip3 install -r requirements.txt')
os.chdir(os.getcwd()+'/CCS')
print("\n\n********** Initializing *********")
os.system('heroku login -i')
os.system('python Host.py')
