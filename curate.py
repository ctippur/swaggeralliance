_author_ = 'ctippur'
import re
import os.path
import os
import sys
import glob

## this is where all generated controller files reside
folder='temp/swagger_server/controllers'

## This is the existing source folder
src='src/python/flask/'

## Temporaru staging area
folderstg='stage'

## Create a stage folder
try:
    os.mkdir(folderstg)
except:
    pass

default_folders=glob.glob(folder + '/*controller.py')
print (default_folders)
#sys.exit(0)
regexstr=['post','get' ]

## Import string
importStr="""\
import connexion
"""

## Post string
postStrFooter="""\
        body = Payload.from_dict(connexion.request.get_json())
    return 'do some magic!'
"""

## Footer string
getStrFooter="""\
"""

## Get string
resLogicGet="""\
    if res['result'] == 'failure':
        res['error_code']=400
        return res, 400
    else:
        return(res)
"""

## Post string
resLogicPost="""\
        if res['result'] == 'failure':
            res['error_code']=400
            return res, 400
        else:
            return(res)
"""

if not os.path.exists(src + "/swagger_server/models"):
    os.makedirs(src + "/swagger_server/models")

modelList=os.listdir(src + "/swagger_server/models")
for model in modelList:
    if model=='__init__.py' or model=='base_model_.py':
        pass
    else:
        modelname=re.sub('\.py$', '', model)
        fn=modelname.title()
        importStr+="\nfrom swagger_server.models." + modelname + " import " + fn


## controllerfile - self explanatory
## operation - _get / _post
## line - function (def)
def createStub(controllerfile,operation,line):
    #print (controllerfile, operation, line)
    if (re.match(operation, '_post')):
        print ("Writing line " + line + "to file " + controllerfile)

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
    #print (origfile)
    args=''
    retstr=''
    str=''
    for str in regexstr:
        #print (origfile, str)

        if re.search(str,origfile):
            retstr=origfile.split(str)[0].replace('def ','')
            if retstr =='':
                retstr=origfile.split('(')[0].replace('def ','')
                args=origfile.split('(')[1].split(')')[0]
    if retstr == '':
        retstr=origfile.split('(')[0].replace('def ','')
        args=origfile.split('(')[1].split(')')[0]
    return (retstr,str,args)

functionCall=None

## Start by copying all controller code to staging area
cmd='cp ' + folder + "/* "  + folderstg
os.system(cmd)

for default_controller in default_folders:
    #default_controller=folder + '/default_controller.py'
    print ("Default controller " + default_controller)
    default_controller_file=default_controller.split('/')[-1]
    # /tmp/stage/temp/swagger_server/controllers/store_controller.py
    print ("Writing to " + folderstg + '/' + default_controller_file)
    fStgDefaultController = open(folderstg + '/' + default_controller_file, 'w')

    ## Read default controller that was generated
    with open(default_controller) as infile:
        defn=0
        post=0
        defline=''
        ## Read each line
        for line in infile:

            ## See if it matches operationid
            if (re.match(r'operationId', line)):
                l=re.findall(r"(\w)(get|post|put)\(", line)[0]
                if l[0] != '_':
                    # Introduce a _ before get
                    line=re.sub(r'((get|post|put|delete))', r'_\1', line)
            ## Match the start of a function
            if (re.match(r'^def', line)):
                defn=1
                defline=line
                #print (ret_filename(line))
                # Each line beginning def is a
                ## Different types of function definitions
                # 1. binary_branch_get(branch)
                # 2. binary_branch_post(body, branch)
                # 3. clinic_city_city_get(city):
                # 4. clinic_get():

                ## This is to handle mangled def with get|post. Example, idget instead of id_get
                l=[]
                try:
                    l=re.findall(r"(\w)(get|post|put)\(", line)[0]
                    if l[0] != '_':
                        # Introduce a _ before get
                        line=re.sub(r'((get|post|put))', r'_\1', line)
                except:
                    l=[]
                #print ("Line is " + line)
                try:
                    newfile,operation,args=ret_filename(line)
                    #print (line,newfile,operation,args)
                except:
                    print (sys.exc_info())
                    continue
                #print ("Operation is " + operation)

                ## Get Arguments to the function
                result=line.partition('(')[-1].rpartition(')')[0]
                ## Get the function name
                impFn=line.split('(')[0].replace('def ', '')

                ## Construct calling new function
                ##from swagger_server.controllers.users import user_users_post
                if operation == '_post':
                    importlocal="    from swagger_server.controllers." + newfile + " import " + impFn + "\n"
                    #functionCall="        return(" + impFn + "(" + result + "))\n"
                    functionCall="    res=" + impFn + "(" + result + ")\n" +  resLogicPost
                else:
                    operation = '_get'
                    importlocal="from swagger_server.controllers." + newfile + " import " + impFn + "\n"
                    #functionCall="    return(" + impFn + "(" + result + "))\n"
                    functionCall="res=" + impFn + "(" + result + ")\n" + resLogicGet

                ## New logic
                ## if connexion.request.is_json

                #importlocal="        from swagger_server.controllers." + newfile + " import " + impFn + "\n"
                #functionCall="        " + impFn + "(" + result + ")\n"

                ## Controller file
                controllerfile=folderstg + '/' + newfile + '.py'
                """
                ## Check if new file exists
                if os.path.exists(controllerfile):
                    ## Check if operation exists
                    if line in open(controllerfile).read():
                        print("controller file Here " + controllerfile + " exists and no changes for " + line)
                    else:
                        print ("Writing line " + line + "to file " + controllerfile)
                        ## Create stub
                        createStub(controllerfile,operation, line)
                else:
                    ## Create file and stub
                    createStub(controllerfile,operation, line)
                """
                fStgDefaultController.write(line)

            #elif (re.match(r'return \'do some magic!\'',line)):
            ## new Only POST has request.is_json in it
            elif ('if connexion.request.is_json' in line):
                post=1
                ## THis means it is post
                importlocal="        from swagger_server.controllers." + newfile + " import " + impFn + "\n"
                #functionCall="        return(" + impFn + "(" + result + "))\n"
                functionCall="        res=" + impFn + "(" + result + ")\n" +  resLogicPost
                controllerfile=folderstg + '/' + newfile + '.py'
                operation="_post"
                newline=defline + '\n' + line
                ## Check if new file exists
                if os.path.exists(controllerfile):
                    ## Check if operation exists
                    if line in open(controllerfile).read():
                        print("controller file " + controllerfile + " exists and no changes for " + line)

                    else:
                        ## Create stub
                        createStub(controllerfile,operation, newline)
                else:
                    ## Create file and stub
                    createStub(controllerfile,operation, newline)
                fStgDefaultController.write(line)

            elif ('return \'do some magic!\'' in line):
                if post == 0:
                    importlocal="    from swagger_server.controllers." + newfile + " import " + impFn + "\n"
                    #functionCall="    return(" + impFn + "(" + result + "))\n"
                    functionCall="    res=" + impFn + "(" + result + ")\n" + resLogicGet
                    ## Controller file
                    controllerfile=folderstg + '/' + newfile + '.py'
                    operation='_get'

                    newline=defline + '\n' + line

                    ## Check if new file exists
                    if os.path.exists(controllerfile):
                        ## Check if operation exists

                        if line in open(controllerfile).read():
                            print("controller file here1 " + controllerfile + " exists and no changes for " + newline)
                        else:
                            print ("post " + str(post), " def " + str(defn), "defline " + newline)

                            ## Create stub
                            createStub(controllerfile,operation, newline)
                    else:
                        ## Create file and stub
                        print ("Writing line " + line + "to file " + controllerfile)
                        createStub(controllerfile,operation, newline)
                    fStgDefaultController.write(line)

                try:
                    fStgDefaultController.write(importlocal)
                    fStgDefaultController.write(functionCall)
                except:
                    fStgDefaultController.write(line)
                defn=0
                post=0
            else:
                fStgDefaultController.write(line)
                #defn=0
                #post=0
fStgDefaultController.close()
