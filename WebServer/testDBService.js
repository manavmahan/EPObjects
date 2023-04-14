import axios from 'axios';

const URL = 'http://127.0.0.1:3001/'

var data = {
    "TYPE": "SEARCH", 
    "TABLE_NAME": "PROJECTS", 
    "COLUMN_NAMES": "ID,PROJECT_NAME,USER_NAME", 
    "CONDITIONS": "PROJECT_NAME='TAUSENDPFUND' AND USER_NAME='MANAV'",
}

// data = {
//     "TYPE": "CREATE_TABLE", 
//     "TABLE_NAME": "PROJECTS", 
// }

data = {
    "TYPE": "ADD_COLUMN", 
    "TABLE_NAME": "PROJECTS",
    "COLUMN_NAME": "PARAMETERS",
    "COLUMN_TYPE": "BLOB"
}

// data = {
//     "TYPE": "INSERT_ITEM", 
//     "TABLE_NAME": "PROJECTS",
//     "COLUMN_NAMES": "(PROJECT_NAME,USER_NAME)",
//     "COLUMN_VALUES": "('TAUSENDPFUND','MANAV')"
// }

// data = {
//     QUERY: `CREATE TRIGGER INSERT_TRIGGER BEFORE INSERT ON PROJECTS FOR EACH ROW SET new.NAME = CONCAT(new.USER_NAME, '-', new.PROJECT_NAME);`
// }

// data = {
//     QUERY: `CREATE TRIGGER UPDATE_TRIGGER BEFORE UPDATE ON PROJECTS FOR EACH ROW SET new.NAME = CONCAT(new.USER_NAME, '-', new.PROJECT_NAME);`
// }

// data = {
//     QUERY: 'ALTER TABLE PROJECTS ADD CONSTRAINT USERPROJECT UNIQUE (USER_NAME,PROJECT_NAME);'
// }

// data = {
//     "TYPE": "UPDATE_ITEM", 
//     "TABLE_NAME": "PROJECTS",
//     "SET_VALUES": "PROJECT_NAME='TAUSENDPFUND'",
//     "CONDITIONS": "PROJECT_NAME='TAUSENDPFUND' AND USER_NAME='MANAV'"
// }

const response = await axios.post(URL, data);

console.log(response.data);