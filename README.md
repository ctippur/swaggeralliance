## Steps for generating python-flask hello world
1. python3 -m venv target
2. source target/bin/activate
3. Generate initial code

  * Via CLI - On Macos
```
   * brew install swagger-codegen
      * For other platforms, refer to https://github.com/swagger-api/swagger-codegen for details
   * cd target
   * swagger-codegen generate -i ../swaggerglobal.yml -l python-flask -o src (Only first time)
```
  * Via Java
```
   * cd target
   * Follow instructions from https://github.com/swagger-api/swagger-codegen and generate code under src (Only first time)
```
  * Via UI
```
   * Go to http://editor.swagger.io/?_ga=2.191872618.1371276200.1503798690-1387572370.1503798690#/
   * Paste the swagger doc into the left hand side of the pane
   * Go to Generate Server on the top and generate python-flask code
   * Copy the zip file to target
   * unzip the file and move the contents of the unzipped contents to target folder
```
4. cd ```<project root>```; sh create_target.sh
You should be able to start the server as python swagger_server/app.py
You are now ready for zappa
5. zappa init
my zappa_settings.json looks like this:

```
{
    "dev": {
        "app_function": "swagger_server.app.app",
        "aws_region": "us-west-1",
        "profile_name": "test",
        "project_name": "petstore-test",
        "binary_support": true,
        "debug": true,
        "keep_warm": false,
        "s3_bucket": "redacted"
    }
}
```

6. zappa deploy

You should now be able to test 

curl -X GET "http://`<aws end point>`/v2/pet/findByStatus?status=available" -H "accept: application/json"
