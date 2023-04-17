import Image from 'next/image'
import Script from 'next/script'
import * as ReactDOM from 'react-dom/client';

import { Inter } from 'next/font/google'

import * as THREE from "three";
import { useState, useEffect, useReducer } from 'react';

// import Plotly from 'plotly';
import React from 'react';
import dynamic from "next/dynamic";
const Plot = dynamic(() => import("react-plotly.js"), { ssr: false, });

import GenerateBuildingElements from './plotly_visualisation';

import axios from 'axios';

const URL = 'http://127.0.0.1:3001/'

const inter = Inter({ subsets: ['latin'] })

async function _getGeometry(setGeometry,){
  let query = {
    "TYPE": "SEARCH", 
    "TABLE_NAME": "PROJECTS", 
    "COLUMN_NAMES": "GEOMETRY", 
    "CONDITIONS": "PROJECT_NAME='TAUSENDPFUND' AND USER_NAME='MANAV'",
  }
  
  axios.post(URL, query)
  .then(({data})=>{
    setGeometry(data.RESULT[0][0]);
  })
  .catch((err)=> {
    console.log(err);
  });
}

function LoadPlotly(buildingElements) {
  console.log(buildingElements)
  const data = GenerateBuildingElements(buildingElements);
  return (
    <Plot data={data.PlotData} layout={data.Layout} config={data.Config}/>
  )
}

function reducer(state, action) {
  if (action.type === 'incremented_age') {
    return {
      age: state.age + 1
    };
  }
  throw Error('Unknown action.');
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
      root.render(LoadPlotly(buildingElements));
    }
  }, [geom, root, elementId]);
}

function ThreeScene(){
  const [geom, setGeom] = useState(null);
  _getGeometry(setGeom);
  useEffect(()=>{
    let element = document.getElementById('scene');
    if(geom!==null){
      let geoms = Create3DObjects(geom);
      // === THREE.JS CODE START ===
      var scene = new THREE.Scene();
      var camera = new THREE.PerspectiveCamera( 75, window.innerWidth/window.innerHeight, 0.1, 1000 );
      var renderer = new THREE.WebGLRenderer();
      renderer.setSize( window.innerWidth, window.innerHeight );
      element.replaceChildren( renderer.domElement );
      var geometry = new THREE.BoxGeometry( 1, 1, 1 );
      var color = (geom===null) ? 0xbbbbbb : 0xff0000;
      var material = new THREE.MeshBasicMaterial( { color: color} );
      var cube = new THREE.Mesh( geometry, material );
      scene.add( ...geoms );
      camera.position.z = 5;
      var animate = function () {
        requestAnimationFrame( animate );
        camera.rotation.x += 0.01;
        camera.rotation.y += 0.01;
        renderer.render( scene, camera );
      };
      animate();
    }else{
      element.replaceChildren( 'loading...' );
    }
    // === THREE.JS EXAMPLE CODE END ===
  }, [geom]);
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

export function HomeOld() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm lg:flex">
        <p className="fixed left-0 top-0 flex w-full justify-center border-b border-gray-300 bg-gradient-to-b from-zinc-200 pb-6 pt-8 backdrop-blur-2xl dark:border-neutral-800 dark:bg-zinc-800/30 dark:from-inherit lg:static lg:w-auto  lg:rounded-xl lg:border lg:bg-gray-200 lg:p-4 lg:dark:bg-zinc-800/30">
          Get started by editing&nbsp;
          <code className="font-mono font-bold">src/pages/index.js</code>
        </p>
        <div className="fixed bottom-0 left-0 flex h-48 w-full items-end justify-center bg-gradient-to-t from-white via-white dark:from-black dark:via-black lg:static lg:h-auto lg:w-auto lg:bg-none">
          <a
            className="pointer-events-none flex place-items-center gap-2 p-8 lg:pointer-events-auto lg:p-0"
            href="https://vercel.com?utm_source=create-next-app&utm_medium=default-template-tw&utm_campaign=create-next-app"
            target="_blank"
            rel="noopener noreferrer"
          >
            By{' '}
            <Image
              src="/vercel.svg"
              alt="Vercel Logo"
              className="dark:invert"
              width={100}
              height={24}
              priority
            />
          </a>
        </div>
      </div>

      <div className="relative flex place-items-center before:absolute before:h-[300px] before:w-[480px] before:-translate-x-1/2 before:rounded-full before:bg-gradient-radial before:from-white before:to-transparent before:blur-2xl before:content-[''] after:absolute after:-z-20 after:h-[180px] after:w-[240px] after:translate-x-1/3 after:bg-gradient-conic after:from-sky-200 after:via-blue-200 after:blur-2xl after:content-[''] before:dark:bg-gradient-to-br before:dark:from-transparent before:dark:to-blue-700/10 after:dark:from-sky-900 after:dark:via-[#0141ff]/40 before:lg:h-[360px]">
        <Image
          className="relative dark:drop-shadow-[0_0_0.3rem_#ffffff70] dark:invert"
          src="/next.svg"
          alt="Next.js Logo"
          width={180}
          height={37}
          priority
        />
      </div>

      <div className="mb-32 grid text-center lg:mb-0 lg:grid-cols-4 lg:text-left">
        <a
          href="https://nextjs.org/docs?utm_source=create-next-app&utm_medium=default-template-tw&utm_campaign=create-next-app"
          className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
          target="_blank"
          rel="noopener noreferrer"
        >
          <h2 className={`${inter.className} mb-3 text-2xl font-semibold`}>
            Docs{' '}
            <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
              -&gt;
            </span>
          </h2>
          <p
            className={`${inter.className} m-0 max-w-[30ch] text-sm opacity-50`}
          >
            Find in-depth information about Next.js features and API.
          </p>
        </a>

        <a
          href="https://nextjs.org/learn?utm_source=create-next-app&utm_medium=default-template-tw&utm_campaign=create-next-app"
          className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
          target="_blank"
          rel="noopener noreferrer"
        >
          <h2 className={`${inter.className} mb-3 text-2xl font-semibold`}>
            Learn{' '}
            <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
              -&gt;
            </span>
          </h2>
          <p
            className={`${inter.className} m-0 max-w-[30ch] text-sm opacity-50`}
          >
            Learn about Next.js in an interactive course with&nbsp;quizzes!
          </p>
        </a>

        <a
          href="https://vercel.com/templates?framework=next.js&utm_source=create-next-app&utm_medium=default-template-tw&utm_campaign=create-next-app"
          className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
          target="_blank"
          rel="noopener noreferrer"
        >
          <h2 className={`${inter.className} mb-3 text-2xl font-semibold`}>
            Templates{' '}
            <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
              -&gt;
            </span>
          </h2>
          <p
            className={`${inter.className} m-0 max-w-[30ch] text-sm opacity-50`}
          >
            Discover and deploy boilerplate example Next.js&nbsp;projects.
          </p>
        </a>

        <a
          href="https://vercel.com/new?utm_source=create-next-app&utm_medium=default-template-tw&utm_campaign=create-next-app"
          className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
          target="_blank"
          rel="noopener noreferrer"
        >
          <h2 className={`${inter.className} mb-3 text-2xl font-semibold`}>
            Deploy{' '}
            <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
              -&gt;
            </span>
          </h2>
          <p
            className={`${inter.className} m-0 max-w-[30ch] text-sm opacity-50`}
          >
            Instantly deploy your Next.js site to a shareable URL with Vercel.
          </p>
        </a>
      </div>
    </main>
  )
}