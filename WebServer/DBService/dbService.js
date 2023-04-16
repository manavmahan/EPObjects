import {readFile} from 'fs';

var standardQueries = null;
readFile('StandardQueries.json', 'utf8', (err, data) => {
    if (err) {
        console.error(err);
        return;
    }
    standardQueries = JSON.parse(data);
});


import express from 'express';
const app = express()
app.use(express.json({
    limit: '200mb',
    extended: true
}));

import cors from 'cors';
app.use(cors());

import axios from 'axios';
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

import { wrapper } from 'axios-cookiejar-support'
import { CookieJar }  from 'tough-cookie';

const port = 3001

const URL = "https://p-energyanalysis.de/"
// const URL = "http://127.0.0.1:8080"
const Id = "f76ba64860271dd9dd21867e387004d1"

const headers = {
    Id: Id,
    Referer: URL,
}

/*
curl -X POST localhost:3001 \
    -H 'Content-Type: application/json' \
    -d @./testProject.json
*/

let cookieJar = new CookieJar();

let client = wrapper(axios.create({
    jar: cookieJar,
    withCredentials: true,
    baseURL: URL,
    headers: headers,
}));

let config = await client.get('getcsrf/');//.then(({ config }) => {
let csrfToken = config.config.jar.toJSON()['cookies'].find(element => element['key'] == 'csrftoken')['value'];
    
client.defaults.headers['x-csrftoken'] = csrfToken;

const executeQuery = async (query, res) => {
    try{
        let result = await client.post('database/', query)
        res.send( result.data );
    }
    catch(error){
        console.log(error);
        res.send({'ERROR': error.response.status});
    }
};

app.post('/', (req, res) => {
    let queryType = req.body['TYPE'];

    if (!queryType || !standardQueries[queryType]){
        executeQuery(req.body, res);
        return;
    }

    let queryData = { ... standardQueries[queryType] };
    // console.log( standardQueries[0]);
    let queryStr = queryData['QUERY'];

    let missingKeys = []
    queryStr.split(' ').filter(word => word.includes('Q_')).forEach(element => {
        let key = element.substring(2)
        if (req.body[key]){
            queryStr = queryStr.replace(element, req.body[key]);
            // console.log(queryStr);
        }else{
            missingKeys.push[key];
        }
    });
    if (missingKeys.length > 0){
        res.send(`Incomplete Request: ${queryType} - ${queryStr} missing ${missingKeys}`);
    }else{
        queryData['QUERY'] = queryStr;
        executeQuery(queryData, res);
    }
});

app.listen(port, () => {
    console.log(`DB service listening on port ${port}`);
});