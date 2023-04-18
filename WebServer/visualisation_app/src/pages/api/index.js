import Image from 'next/image'
import Script from 'next/script'
import * as ReactDOM from 'react-dom/client';

import { Inter } from 'next/font/google'

import { useState, useEffect, useReducer } from 'react';
import { useRouter } from 'next/router';

import GenerateBuildingElements from './plotly_visualisation';

import axios from 'axios';

const URL = 'http://127.0.0.1:3001/'

const inter = Inter({ subsets: ['latin'] })

async function _getGeometry(setGeometry, project_name, user_name){
  let query = {
    "TYPE": "SEARCH", 
    "TABLE_NAME": "PROJECTS", 
    "COLUMN_NAMES": "GEOMETRY", 
    "CONDITIONS": `PROJECT_NAME='${project_name}' AND USER_NAME='${user_name}'`,
  }

  console.log(query);
  
  axios.post(URL, query)
  .then(({data})=>{
    if (data.ERROR)
      console.log(data.ERROR, data.QUERY)
    setGeometry(data.RESULT[0][0]);
  })
  .catch((err)=> {
    console.log(err);
  });
}

// http://localhost:3000/?user_name=MANAV&project_name=TAUSENDPFUND
// http://localhost:3000/?user_name=RANDOM&project_name=SHAPE_100_000155
function PlotlyPlot(elementId, project_name='TAUSENDPFUND', user_name='MANAV'){
  const [geom, setGeom] = useState(null);
  const [root, setRoot] = useState(null);

  _getGeometry(setGeom, project_name, user_name);
  useEffect(()=>{
    if (document && (!root)) {
      console.log(root);
      setRoot(ReactDOM.createRoot(document.getElementById(elementId)));
    }
    
    if((geom!==null) && (root!==null)){
      let elements = JSON.parse(geom);
      let buildingElements = elements.filter(obj => /^(Building|Fenestration)Surface:Detailed/.test(obj['__IDFName__']));
      root.render(GenerateBuildingElements(buildingElements));
    }
  }, [geom, root, elementId]);
}


function DivElement({ id }) {
  return <div id={id}> </div>;
}

function Home() {
  const router = useRouter();

  const { project_name, user_name } = router.query;
  console.log(router.query);
  console.log(project_name, user_name);

  PlotlyPlot('plot_div',project_name, user_name);
  return (
    <>
    <DivElement id='plot_div' />
    <form action="/update" method="post">
      <label htmlFor="project_name">Project Name: </label>
      <input type="text" id="project_name" name="project_name" required />
      <label htmlFor="user_name"> User Name: </label>
      <input type="text" id="user_name" name="user_name" required />
      <button type="submit">  Update</button>
    </form>
  </>
  )
}

export default Home;