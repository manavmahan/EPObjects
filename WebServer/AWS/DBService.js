import { DynamoDB } from "@aws-sdk/client-dynamodb";
import express from 'express';
import pkg from 'body-parser';
const { json, urlencoded } = pkg;
// const json = require('JSON')

import { UpdateProject } from './ProjectTransactions.js';

const client = new DynamoDB({ region: "eu-west-1" });

const UsersListTableName = 'Users'

const app = express()
const port = 3001

app.use( json() );       // to support JSON-encoded bodies
app.use(urlencoded({     // to support URL-encoded bodies
    extended: true
}));

const IsUserExists = (username, actionTrue, actionFalse) => {
    let params = {
        TableName: UsersListTableName,
        Key: {
            'UserName' : {S: `${username}`},
        }
    };

    client.getItem(params, function(err, data){
        if (err){
            console.log(err);
            return false;
        };

        if (data['Item']){ 
            actionTrue(data);
            return true;
        } else{
            actionFalse (data);
            return false;
        };
    });
    
};

/*
curl -X POST localhost:3001/createuser \
    -H 'Content-Type: application/json' \
    -d '{"UserName": "manav"}' 
*/
app.post('/createuser/', (req, res) => {
    let username = req.body.UserName;
    if (!username) {
        res.send(`Error: missing username from request!}`);
        return;
    };

    IsUserExists(username,
        actionTrue = (data) => {res.send(`User exists: ${username}`); },
        actionFalse = null);

    console.log(`Requested Create User: ${username}`)
    var params = {
        TableName: 'Users',
        Item: {
            'UserName' : {S: `${username}`},
        }
    };

    client.putItem(params, function(err, data) {
        if (err) {
            res.send(`Error: ${JSON.stringify(err)}`);
        } else {
            res.send(`Success: ${JSON.stringify(data)}`);
        }
    });
});

/*
curl -X POST localhost:3001/updateproject \
    -H 'Content-Type: application/json' \
    -d @./testProject.json
*/
app.post('/updateproject/', (req, res) => {
    let userName = req.body.UserName;
    let projectName = req.body.ProjectName;
    if (!userName || !projectName) {
        res.send(`Error: missing user and/or project name from request!}`);
        return;
    };

    UpdateProject(req.body.UserName, req.body.ProjectName, req.body.ProjectData, 
        actionSuccess = () => {
            res.send(`Updated/created project: ${projectName}`);
    });
});

app.listen(port, () => {
  console.log(`DB service listening on port ${port}`)
});