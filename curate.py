_author_ = 'ctippur'
import re
import os.path
import os

folder='src/swagger_server/controllers'
folderstg='/tmp/stage'

## Create a stage folder
try:
    os.mkdir(folderstg)
except:
    pass

default_controller=folder + '/default_controller.py'
regexstr=['_post','_get']

fStgDefaultController = open(folderstg + '/default_controller.py', 'w')

importStr="""\
import connexion
"""
modelList=os.listdir("src/swagger_server/models")
for model in modelList:
    if model=='__init__.py' or model=='base_model_.py':
        pass
    else:
        fn=model.title()
        importStr+="\nfrom swagger_server.models." + model + " import " + fn


postStrFooter="""\
    if connexion.request.is_json:
        body = Payload.from_dict(connexion.request.get_json())
    return 'do some magic!'
"""

getStrFooter="""\
    return 'do some magic!'
"""

## controllerfile - self explanatory
## operation - _get / _post
## line - function (def)
def createStub(controllerfile,operation,line):
    print (controllerfile, operation, line)
    if (re.match(operation, '_post')):
        if os.path.exists(controllerfile):
            with open(controllerfile, "a") as w:
                w.write('\n')
                w.write(line)
                w.write(postStrFooter)
        else:
            with open(controllerfile, "w") as w:
                w.write(importStr)
                w.write('\n')
                w.write(line)
                w.write(postStrFooter)
    elif (re.match(operation, '_get')):
        if os.path.exists(controllerfile):
            with open(controllerfile, "a") as w:
                w.write('\n')
                w.write(line)
                w.write(getStrFooter)
        else:
            with open(controllerfile, "w") as w:
                w.write(importStr)
                w.write('\n')
                w.write(line)
                w.write(getStrFooter)


def ret_filename(origfile):
    for str in regexstr:
        if re.search(str,origfile):
            retstr=origfile.split(str)[0].replace('def ','')
            return (retstr,str)

functionCall=None

## Start by copying all controller code to staging area
cmd='cp ' + folder + "/* "  + folderstg
os.system(cmd)

with open(default_controller) as infile:
    for line in infile:
        if (re.match(r'^def', line)):
            #print (ret_filename(line))
            # Each line beginning def is a
            ## Different types of function definitions
            # 1. binary_branch_get(branch)
            # 2. binary_branch_post(body, branch)
            # 3. clinic_city_city_get(city):
            # 4. clinic_get():
            newfile,operation=ret_filename(line)
            print ("Operation is " + operation)

            ## Get Arguments to the function
            result=line.partition('(')[-1].rpartition(')')[0]
            ## Get the function name
            impFn=line.split('(')[0].replace('def ', '')

            ## Construct calling new function
            ##from swagger_server.controllers.users import user_users_post

            if operation == '_post':
                importlocal="        from swagger_server.controllers." + newfile + " import " + impFn + "\n"
                functionCall="        " + impFn + "(" + result + ")\n"
            elif operation == '_get':
                importlocal="    from swagger_server.controllers." + newfile + " import " + impFn + "\n"
                functionCall="    " + impFn + "(" + result + ")\n"

            #importlocal="        from swagger_server.controllers." + newfile + " import " + impFn + "\n"
            #functionCall="        " + impFn + "(" + result + ")\n"

            ## Controller file
            controllerfile=folderstg + '/' + newfile + '.py'

            ## Check if new file exists
            if os.path.exists(controllerfile):
                ## Check if operation exists
                if line in open(controllerfile).read():
                    print("controller file " + controllerfile + " exists and no changes for " + line)
                else:
                    ## Create stub
                    createStub(controllerfile,operation, line)
            else:
                ## Create file and stub
                createStub(controllerfile,operation, line)
            fStgDefaultController.write(line)
        #elif (re.match(r'return \'do some magic!\'',line)):
        elif ('return \'do some magic!\'' in line):
            fStgDefaultController.write(importlocal)
            fStgDefaultController.write(functionCall)
        else:
            fStgDefaultController.write(line)
fStgDefaultController.close()
