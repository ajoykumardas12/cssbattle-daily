import os
import subprocess
from datetime import datetime
import pyperclip
import time

solutions_folder = r'C:\Users\ajoyk\Desktop\projects\cssbattle-solutions\solutions'
# source_code_file_path = r'C:\Users\ajoyk\Documents\cssb.txt'
today_date = datetime.today().strftime('%Y-%m-%d')
new_folder_path = os.path.join(solutions_folder, today_date)
index_file_path = os.path.join(new_folder_path, 'index.html')
current_git_branch = ''

def confirmUpdate():
    updateConfirmation = input(f"Today's code has been created already. Do you want to update? (y/n): ").lower()
    if updateConfirmation != 'y':
        print("❎ Task aborted.\nExiting...")
        time.sleep(2)
        exit()
        
def optionallyMakeDir():
    new_folder_exists = os.path.exists(new_folder_path)
    
    if os.path.exists(solutions_folder):
        if new_folder_exists:
            confirmUpdate()
        else:
            os.makedirs(new_folder_path)
    else:
        print("❔ Project folder doesn't exist.\nExiting...")
        time.sleep(2)
        exit()
        
def checkCode(code):
    required_string = 'style'
    if required_string not in code:
        confirmation = input(f"Looks like correct code isn't copied in clipboard.\nDo you still want to proceed? (y/n): ").lower()
        if confirmation != 'y':
            print("❎ Task aborted.\nExiting...")
            time.sleep(2)
            exit()
            
def copyCodeToFile(file_path, code):
    with open(file_path, 'w') as index_file:
        index_file.write(code)
        
def isGitBranchMain():
    global current_git_branch
    git_branch_check = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    current_git_branch = git_branch_check.stdout.strip()
    return current_git_branch == 'main'

def printSuccessfulPushMessage():
    print(f"Remote file: " + "https://github.com/ajoykumardas12/cssbattle-solutions/tree/main/solutions/" + today_date + "/index.html")
    
def runGitProcess():
    subprocess.run(['git', 'checkout', 'main'])
    
    isBranchMain = isGitBranchMain()
    
    if isBranchMain:
        subprocess.run(['git', 'add', f'{today_date}/index.html'])
        commit_message = f'cssb:{today_date}'
        subprocess.run(['git', 'commit', '-m', commit_message])
        subprocess.run(['git', 'push', 'origin', 'main'])
        printSuccessfulPushMessage()
    else:
        print(f"⚠ Current branch is {current_git_branch}, not 'main'.")

def executeTask():
    optionallyMakeDir()
    
    # ------ Copy from file ------
    # with open(source_code_file_path, 'r') as source_code_file:
    #     code_to_paste = source_code_file.read()
    
    # ------ Or, Copy from clipboard ------
    code_to_paste = pyperclip.paste()
    
    checkCode(code_to_paste)
    copyCodeToFile(index_file_path, code_to_paste)
    
    os.chdir(solutions_folder)
    runGitProcess()

try:
    executeTask()
    print(f"✅ Task completed successfully!!")
except Exception as e:
    print(f"\u274c Error: {e}")
    
input("Press Enter to exit...")
