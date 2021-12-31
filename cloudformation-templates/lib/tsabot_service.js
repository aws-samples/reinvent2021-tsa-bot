const core = require("@aws-cdk/core");
const lambda = require("@aws-cdk/aws-lambda");
const iam = require("@aws-cdk/aws-iam");
const dynamodb = require("@aws-cdk/aws-dynamodb");
//const cr = require("@aws-cdk/custom-resources");
const custom = require("@aws-cdk/custom-resources");



class tsaService extends core.Construct {
  constructor(scope, id) {
    super(scope, id);

    const generateItemBag = () => {
      return {
        id: { S: "Bag" },
        Allowed: { BOOL: false },
        labels: { SS: ["Coat","Sleeve","Sweater","Sweatshirt"] }
      };
    };
    
    var generateItemPhone = () => {
      return {
        id: { S: "Phone" },
        Allowed: { BOOL: false },
        labels: { "SS": ["Cell Phone","Iphone","Mobile Phone","Phone"] }
      };
    };
    
    var generateItemDrink = () => {
      return {
        id: { S: "Drink" },
        Allowed: { BOOL: false },
        labels: { "SS": ["Bottle","Can","Coffee","Cup"] }
      };
    };
    
    var generateItemHat = () => {
      return {
        id: { S: "Hat" },
        Allowed: { BOOL: false },
        labels: { "SS": ["Baseball Cap","Cap","Hat"] }
      };
    };
    
    var generateItemLaptop = () => {
      return {
        id: { S: "Laptop" },
        Allowed: { BOOL: false },
        labels: { "SS": ["Computer","Laptop"] }
      };
    };
    
    var generateItemJacket = () => {
      return {
        id: { S: "Jacket" },
        Allowed: { BOOL: false },
        labels: { "SS": ["Coat","Sleeve","Sweater","Sweatshirt"] }
      };
    };

    const table = new dynamodb.Table(this, 'tsaimagesddb', {
        partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
        timeToLiveAttribute: 'TTL',
        tableName: 'tsa-images2',
        removalPolicy: core.RemovalPolicy.DESTROY,
      });
  
      const ddbarn = new core.CfnOutput(this, "DDBTabletsaimagesARN",{
        value: table.tableArn,
        description: 'DynamoDB Table ARN',
        exportName: 'DDBTabletsaimagesARN'
      });

      const tableflights = new dynamodb.Table(this, 'Flightsddb', {
        partitionKey: { name: 'arr_iata', type: dynamodb.AttributeType.STRING },
        tableSortKey: { name: 'flight_number', type: dynamodb.AttributeType.STRING },
        timeToLiveAttribute: 'TTL',
        tableName: 'Flights2',
        removalPolicy: core.RemovalPolicy.DESTROY,
        stream: dynamodb.StreamViewType.KEYS_ONLY
      });
  
      const ddbflightsarn = new core.CfnOutput(this, "DDBTableFlightsARN",{
        value: tableflights.tableArn,
        description: 'DynamoDB Table ARN',
        exportName: 'DDBTableFlightsARN'
      });


    const handler = new lambda.Function(this, "FlightsDepartureLambda", {
      functionName: "update-flight-LasVegasdeparture2",
      runtime: lambda.Runtime.PYTHON_3_8, //
      code: lambda.Code.fromAsset("resources/Lambda/update-flight-LasVegasdeparture"),
      handler: "flight.handler_name",
      environment: {
        //BUCKET: bucket.bucketName
      },
      //layers: [lambdaxraylayer,lambdaalexasdklayer],
      timeout: core.Duration.seconds(10)
    });

      
    handler.addToRolePolicy(new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: [
        "dynamodb:BatchWriteItem"
        ],
        resources: ['arn:aws:dynamodb:*:*:table/Flights2']
      }));


    const myDDBProviderDrink = new custom.AwsCustomResource(this, 'MyProviderDrink', {
      onCreate: {
             service: 'DynamoDB',
            action: 'putItem',
            parameters: {
              TableName: 'tsa-images2',
              Item: generateItemDrink(),
            },
            physicalResourceId: 'initDBDataDrink',
          },
          policy: custom.AwsCustomResourcePolicy.fromSdkCalls({ resources: custom.AwsCustomResourcePolicy.ANY_RESOURCE }),
        });
    
      const myDDBProviderPhone = new custom.AwsCustomResource(this, 'initDBResourcePhone', {
        onCreate: {
          service: 'DynamoDB',
         action: 'putItem',
         parameters: {
           TableName: 'tsa-images2',
           Item: generateItemPhone(),
         },
         physicalResourceId: 'initDBDataPhone',
       },
       policy: custom.AwsCustomResourcePolicy.fromSdkCalls({ resources: custom.AwsCustomResourcePolicy.ANY_RESOURCE }),
     });

     const myDDBProviderHat = new custom.AwsCustomResource(this, 'initDBResourceHat', {
      onCreate: {
        service: 'DynamoDB',
       action: 'putItem',
       parameters: {
         TableName: 'tsa-images2',
         Item: generateItemHat(),
       },
       physicalResourceId: 'initDBDataHat',
     },
     policy: custom.AwsCustomResourcePolicy.fromSdkCalls({ resources: custom.AwsCustomResourcePolicy.ANY_RESOURCE }),
   });

   const myDDBProviderLaptop = new custom.AwsCustomResource(this, 'initDBResourceLaptop', {
    onCreate: {
      service: 'DynamoDB',
     action: 'putItem',
     parameters: {
       TableName: 'tsa-images2',
       Item: generateItemLaptop(),
     },
     physicalResourceId: 'initDBDataLaptop',
   },
   policy: custom.AwsCustomResourcePolicy.fromSdkCalls({ resources: custom.AwsCustomResourcePolicy.ANY_RESOURCE }),
 });

 const myDDBProviderJacket = new custom.AwsCustomResource(this, 'initDBResourceJacket', {
  onCreate: {
    service: 'DynamoDB',
   action: 'putItem',
   parameters: {
     TableName: 'tsa-images2',
     Item: generateItemJacket(),
   },
   physicalResourceId: 'initDBDataJacket',
 },
 policy: custom.AwsCustomResourcePolicy.fromSdkCalls({ resources: custom.AwsCustomResourcePolicy.ANY_RESOURCE }),
});

  }
}


module.exports = { tsaService }
