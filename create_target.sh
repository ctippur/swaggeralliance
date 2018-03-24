rm -rf stage temp
deactivate 2>/dev/null
pwd=`pwd`
src='src/python/flask/'
rm -f ${pwd}/swagger_server.zip

if [ ! -d "target" ]; then
  python3 -m venv --without-pip target
  source target/bin/activate
  curl https://bootstrap.pypa.io/get-pip.py | python
  deactivate
fi
source target/bin/activate

##
mkdir -p stage
cp ${src}/requirements.txt stage 2>/dev/null

# Generate new code under temp
swagger-codegen generate -i swaggerglobal.yml -l python-flask -o temp
mkdir -p ${src}/swagger_server/swagger
mkdir -p ${src}/swagger_server/controllers
cp temp/swagger_server/swagger/swagger.yaml ${src}/swagger_server/swagger/swagger.yaml
cp temp/swagger_server/controllers/*_controller.py ${src}/swagger_server/controllers

## Code to copy mopdel code if it does not exist
for files in `ls temp/swagger_server/models/*.py|egrep -v "__init__|binary.py|config.py"`; do
  modelsrc=$files
  dest="${src}/swagger_server/models/`basename $files`"
  echo "Copying $modelsrc $dest"
  #dest=`echo $files|sed "s|temp|${src}|g"`
  if [ ! -f $dest ]; then
     cp $modelsrc $dest
  fi
done

python curate.py ## Generates controller code under stage

cp stage/*_controller.py ${src}/swagger_server/controllers
#for files in `ls /tmp/stage/*_controller.py`; do
#  cp $files ${src}/swagger_server/controllers
#done
## Code to copy controller code if it does not exist
for files in `ls stage/*.py|egrep -v "__init__"`; do
  srccontroller=$files
  echo "Copying $srccontroller $dest"
  dest="${src}/swagger_server/controllers/`basename $files`"
  #echo $dest
  if [ ! -f $dest ]; then
     cp $srccontroller $dest
  fi
done
cp -r ${src}/swagger_server stage
#cp /tmp/stage/* stage/swagger_server/controllers
pip install -r ${pwd}/stage/requirements.txt
cp -r target/lib/python3.6/site-packages/* stage
cp ${src}/zappa_settings.json stage
exit

zip -r9 ${pwd}/swagger_server.zip * -x \*.pyc\*
cd $pwd/target
zip -g -r ${pwd}/swagger_server.zip swagger_server -x \*.pyc\*
