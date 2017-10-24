# Swaggeralliance
## Purpose
This effort aims at integrating code generated via swagger codegen with other api gateway providers like AWS. 
Design principles:
   1. Keep it code agnostic - This means that we need to be able to use this methodology to accomodate different programming languages
   2. Cloud provider agnostic - We should be able to leverage different cloud offerings, like AWS, Google Cloud Platform
   3. Design first approach - Foster design first approach for api development.


### Advantages:
Ideally, this should significantly cut down the time it takes to develop API's and deploy it. The idea here is to leverage existing tools available to glue things together. As a first phase, we are looking at integrating swagger with AWS API gateway. 

## Flow
Based on design first approach (read [link](https://swaggerhub.com/blog/api-design/design-first-or-code-first-api-development/) for use cases that support design first approach), an ideal flow would be to:

1. Design the model and end points via Swagger
2. Validate with the team
3. Generate code stub via swagger codegen
4. Run a script/use UI to specify the provider. This changes/adds code necessary for a specific provider
5. Iterate on business logic and swagger configuration and checkin your code
6. Upload your code to the provider of choice (using zappa for AWS, find similar ones for other providers?) test and promote to production.

Any further changes to the endpoint or model should be reflected on swagger and code stub should be generated.

## Challenges/opportunities 
Just jotting down some challenges. I am sure there are a lot more.

1. After implementing business logic, how do we link with further changes to model or end point? This is relevant because swagger codegen recreates the stub.
2. Build A/B testing environment (For example use Wasabi)
3. Improve code gen to conform to specific use cases. Some things I can think of: 
   * Machine learning with pickle and otehr required libraries
   * Database connectivity (rds/otherwise)
   * Things needed for mobile/IOT applications
4. Abstracting other parameters in a ui or a command line so that we can truely make the experience agnostic to the provider.
5. Integrating with other providers like Azure, Google Cloud Platform. etc

## Steps for generating python-flask hello world
1. Generate initial code

  * Via CLI - On Macos
```
   * brew install swagger-codegen
      * For other platforms, refer to https://github.com/swagger-api/swagger-codegen for details
   * swagger-codegen generate -i swaggerglobal.yml -l python-flask -o src/python/flask (Only first time)
```
  * Via Java
```
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
