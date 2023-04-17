import * as THREE from "three";

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
  