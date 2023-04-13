// const AWS = require('@aws-sdk/config-resolver');
import { DynamoDB } from "@aws-sdk/client-dynamodb";


// AWS.config.loadFromPath('./config.json');
const client = new DynamoDB({ region: "eu-west-1" });

var params = {
    AttributeDefinitions: [
        {
            AttributeName: "UserName", 
            AttributeType: "S"
        },
    ], 
    KeySchema: [
        {
            AttributeName: "UserName", 
            KeyType: "HASH"
        },
    ], 
    ProvisionedThroughput: {
        ReadCapacityUnits: 5, 
        WriteCapacityUnits: 5
    }, 
    TableName: "Users"
};

var params = {
    AttributeDefinitions: [
        {
            AttributeName: "UserName", 
            AttributeType: "S",
            AttributeName: "ProjectName", 
            AttributeType: "S",
            AttributeName: "ProjectData", 
            AttributeType: "S",
        },
    ], 
    KeySchema: [
        {
            AttributeName: "UserName", 
            KeyType: "HASH",
            AttributeName: "ProjectName", 
            KeyType: "HASH",
            AttributeName: "ProjectData", 
            KeyType: "RANGE",
        },
    ],
    ProvisionedThroughput: {
        ReadCapacityUnits: 1, 
        WriteCapacityUnits: 1,
    }, 
    TableName: "Projects"
};

client.createTable(params, function(err, data) {
    if (err) console.log(err, err.stack);
    else console.log(data);
});


// var params = {
//     TableName: "Users"
// };

// client.deleteTable(params, function(err, data) {
//     if (err) console.log(err, err.stack);
//     else console.log(data);
// });