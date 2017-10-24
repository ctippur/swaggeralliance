deactivate 2>/dev/null
python3 -m venv target
pwd=`pwd`
rm -f ${pwd}/swagger_server.zip
source target/bin/activate
cp src/python/flask/requirements.txt target
rm -rf temp
swagger-codegen generate -i swaggerglobal.yml -l python-flask -o temp
for files in `ls temp/swagger_server/models/*.py|egrep -v "__init__|binary.py"`; do 
  src=$files
  dest=`echo $files|sed 's/temp/src/g'`
  if [ ! -f $dest ]; then
     cp $src $dest
  fi
  cp temp/swagger_server/swagger/swagger.yaml src/python/flask/swagger_server/swagger/swagger.yaml
  cp temp/swagger_server/controllers/default_controller.py src/python/flask/swagger_server/controllers
done
cp -r src/python/flask/swagger_server target
python curate.py ## Generates controller code
cp /tmp/stage/* target/swagger_server/controllers
cd target
pip install -r requirements.txt
cd lib/python3.6/site-packages
zip -r9 ${pwd}/swagger_server.zip *
cd $pwd/target
zip -g -r ${pwd}/swagger_server.zip swagger_server
