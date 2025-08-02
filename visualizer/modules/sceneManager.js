export let scene = new THREE.Scene();
let camera, renderer, controls;

// only needs to be called once
export function initCanvas() {
  // SETUP RENDERER & SCENE
  let canvas = document.getElementById('canvas');
  renderer = new THREE.WebGLRenderer();
  renderer.setClearColor(0x30322F); // set background colour
  canvas.appendChild(renderer.domElement);

  // SETUP CAMERA
  camera = new THREE.PerspectiveCamera(30,1,0.1,1000); // view angle, aspect ratio, near, far
  camera.position.set(15,10,10);
  camera.lookAt(0,0,0);
  scene.add(camera);

  // SETUP ORBIT CONTROLS OF THE CAMERA
  controls = new THREE.OrbitControls(camera);
  controls.damping = 0.2;
  controls.autoRotate = false;
  
  // EVENT LISTENER RESIZE
  window.addEventListener('resize',resize);
  resize();

  // SCROLLBAR FUNCTION DISABLE
  window.onscroll = function () {
      window.scrollTo(0,0);
  }

  // ADD LIGHTS
  const light = new THREE.PointLight(0xffffff);
  light.position.set(0,4,2);
  scene.add(light);
  const ambientLight = new THREE.AmbientLight(0x606060);
  scene.add(ambientLight);

  const axesHelper = new THREE.AxesHelper( 4 );
  scene.add( axesHelper );
}

// ADAPT TO WINDOW RESIZE
function resize() {
  renderer.setSize(window.innerWidth,window.innerHeight);
  camera.aspect = window.innerWidth/window.innerHeight;
  camera.updateProjectionMatrix();
}

export function render() {
  renderer.render(scene, camera);
}