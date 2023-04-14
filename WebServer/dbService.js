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
app.use(express.json());

import axios from 'axios';
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

import { wrapper } from 'axios-cookiejar-support'
import { CookieJar }  from 'tough-cookie';

const port = 3001

const URL = "https://p-energyanalysis.de/"
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

const executeQuery = async (query, res) => {
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
    
    let result = await client.post('database/', query)
    res.send( result.data );
};

app.post('/', (req, res) => {
    let queryType = req.body['QueryType'];

    if (!queryType || !standardQueries[queryType]){
        executeQuery(req.body, res);
        return;
    }

    // let queryData = { ... standardQueries[queryType] };
    // // console.log( standardQueries[0]);
    // let queryStr = queryData['Query'];

    // queryStr.split(' ').filter(word => word.includes('Q_')).forEach(element => {
    //     let key = element.substring(2)
    //     if (! req.body[key]){
    //         res.send(`Incomplete Request: ${queryType} - ${queryStr} missing ${key}`);
    //         return;
    //     }
    //     queryStr.replace(key, req.body[key])
    // });
    // executeQuery(queryData, res);
});

app.listen(port, () => {
    console.log(`DB service listening on port ${port}`);
});