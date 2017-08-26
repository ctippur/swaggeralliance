# Swaggeralliance
## Purpose
This effort aims at integrating code generated via swagger codegen with other api gateway providers like aws. 

### Advantages:
Ideally, this should significantly cut down the time it takes to develop API's and deploy it. The idea here is to leverage existing tools available to glue things together. As a first phase, we are looking at integrating swagger 

## Flow
Based on design first approach (read [link]: https://swaggerhub.com/blog/api-design/design-first-or-code-first-api-development/ for use cases that support design first approach), an ideal flow would be to:

1. Design the model and end points via Swagger
2. Validate with the team
3. Generate code stub via swagger codegen
4. Iterate on business logic and swagger configuration and checkin your code
5. Upload your code to the provider of choice (zappa for AWS, find similar ones for other providers?) test and promote to production.

Any further changes to the endpoint or model should be reflected on swagger and code stub should be generated.

## Challenges
Just jotting down some challenges. I am sure there are a lot more.

1. After implementing business logic, how do we link with further changes to model or end point? This is relevant because swagger codegen recreates the stub.
2. Integrting with other providers like Azure, Google Cloud Platform
3. Build A/B testing environment (For example use Wasabi)



