import express, { response } from 'express';
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

app.post('/', (req, res) => {
    let cookieJar = new CookieJar();

	let client = wrapper(axios.create({
		jar: cookieJar,
		withCredentials: true,
        baseURL: URL,
        headers: headers,
	}));

    client.get('getcsrf/').then(({ config }) => {
        let csrfToken = config.jar.toJSON()['cookies'].find(element => element['key'] == 'csrftoken')['value'];
        
        client.defaults.headers['x-csrftoken'] = csrfToken;
        
        client.post('database/', req.body)
        .then(r=>{res.send(r.data)})
        .catch(error=>{console.log(error); res.send('error'); })
    });
});

app.listen(port, () => {
    console.log(`DB service listening on port ${port}`);
});