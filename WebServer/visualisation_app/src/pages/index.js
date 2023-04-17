import Image from 'next/image'
import Script from 'next/script'
import * as ReactDOM from 'react-dom/client';

import { Inter } from 'next/font/google'

import { useState, useEffect, useReducer } from 'react';

import GenerateBuildingElements from './plotly_visualisation';

import axios from 'axios';

const URL = 'http://127.0.0.1:3001/'

const inter = Inter({ subsets: ['latin'] })

async function _getGeometry(setGeometry,){
  let query = {
    "TYPE": "SEARCH", 
    "TABLE_NAME": "PROJECTS", 
    "COLUMN_NAMES": "GEOMETRY", 
    "CONDITIONS": "PROJECT_NAME='SHAPE_100_000100' AND USER_NAME='RANDOM'",
  }
  
  axios.post(URL, query)
  .then(({data})=>{
    setGeometry(data.RESULT[0][0]);
  })
  .catch((err)=> {
    console.log(err);
  });
}

function PlotlyPlot(elementId){
  const [geom, setGeom] = useState(null);
  const [root, setRoot] = useState(null);

  _getGeometry(setGeom);
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
  PlotlyPlot('plot_div');
  return (
    <DivElement id='plot_div' />
  )
}

export default Home;