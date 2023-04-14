import axios from 'axios';

const URL = 'http://127.0.0.1:3001/'

// let data = {
//     "QueryType": "Search", 
//     "TABLE_NAME": "Projects", 
//     "COLUMN_NAMES": "Id,ProjectName,UserName", 
//     "CONDITIONS": "ProjectName='Tausendpfund'",
// }

let data = {
    "TYPE": "CREATE_TABLE", 
    "TABLE_NAME": "PROJECTS", 
}

const response = await axios.post(URL, data);

console.log(response.data);