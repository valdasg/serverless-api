# API call recording app for S3

This app records API calls and records it to Dynamo Db.
App is created using Serverless Framework on AWS platfrom.

## Usage
Send request to API endpoint and item will be added, uodated, deleted or all items will be listed.

### Deployment
Third-party dependencies are used in app, so you will need to use a plugin `serverless-python-requirements`. You can set it up by running the following command:

```bash
serverless plugin install -n serverless-python-requirements
```
In order to deploy app you need to clone and run the following command from parrent folder:
```
$ serverless deploy
```
Framework creates lambda functions, iam role and api service.

### Clean up
After playing with app run:
```
sls remove
```