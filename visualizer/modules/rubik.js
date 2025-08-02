// Import the scene here to facilitate cube creation and modification
// Directly modifying the scene during cube creation improves performance
import { scene } from "./sceneManager.js";

///////////////////////////////////////////////////////////////////////////////////////////
//  MATERIALS
///////////////////////////////////////////////////////////////////////////////////////////

let blackMaterial = new THREE.MeshBasicMaterial({ color: 0x000000 });
let blueMaterial = new THREE.MeshBasicMaterial( { color: 0x003DA5 } );
let greenMaterial = new THREE.MeshBasicMaterial( { color: 0x009A44 } );
let whiteMaterial = new THREE.MeshBasicMaterial( { color: 0xFFFFFF } );
let yellowMaterial = new THREE.MeshBasicMaterial( { color: 0xFFD700 } );
let redMaterial = new THREE.MeshBasicMaterial( { color: 0xBA0C2F } );
let orangeMaterial = new THREE.MeshBasicMaterial( { color: 0xFE5000 } );

///////////////////////////////////////////////////////////////////////////////////////////
//  OBJECTS
///////////////////////////////////////////////////////////////////////////////////////////

function createCubelet(x, y, z) {
  let cubeGeometry = new THREE.BoxGeometry(1, 1, 1);
  let cubeMaterial = generateMaterial(x, y, z);
  let cubelet = new THREE.Mesh(cubeGeometry, cubeMaterial);
  cubelet.position.set(x, y, z);
  return cubelet;
}

function generateMaterial(x, y, z) {
  if (x == 0 && y == 0 && z == 0) {return blackMaterial;} // hidden piece
  let cubeMaterialArray = [];   // order to add materials: x+,x-,y+,y-,z+,z-
  
  if (x == 0 || x == -1.1) {cubeMaterialArray[0] = blackMaterial;} // right face black
  else cubeMaterialArray.push( blueMaterial );
  if (x == 0 || x == 1.1) {cubeMaterialArray[1] = blackMaterial;} // left face black
  else cubeMaterialArray.push( greenMaterial );
  if (y == 0 || y == -1.1) {cubeMaterialArray[2] = blackMaterial;} // top face black
  else cubeMaterialArray.push( whiteMaterial );
  if (y == 0 || y == 1.1) {cubeMaterialArray[3] = blackMaterial;} // bottom face black
  else cubeMaterialArray.push( yellowMaterial );
  if (z == 0 || z == -1.1) {cubeMaterialArray[4] = blackMaterial;} // front face black
  else cubeMaterialArray.push( redMaterial );
  if (z == 0 || z == 1.1) {cubeMaterialArray[5] = blackMaterial;} // back face black
  else cubeMaterialArray.push( orangeMaterial );
  
  return cubeMaterialArray;
}

export let cubesArray3D = [];
export function createCube() {
  cubesArray3D = [];
  for (let x = -1.1; x <= 1.1; x += 1.1) {
    let why = [];
    for (let y = -1.1; y <= 1.1; y += 1.1) {
      let zed = [];
      for (let z = -1.1; z <= 1.1; z += 1.1) {
        const c = createCubelet(x, y, z);
        zed.push(c);
        scene.add(c);
      }
      why.push(zed);
    }
    cubesArray3D.push(why);
  }
}

export function resetCubeObject() {
  cubesArray3D.forEach(layer => {
    layer.forEach(row => {
      row.forEach(cube => {
        scene.remove(cube);
      });
    });
  });
  createCube();
}

///////////////////////////////////////////////////////////////////////////////////////
// FACE ROTATION HELPER FUNCTIONS (shared rotation behaviour for each axis)
///////////////////////////////////////////////////////////////////////////////////////

// special rounding helper function, rounds value to -1.1, 0, 1.1
function round(v) {
  var distToZero = Math.abs(v);
  var distToPos = Math.abs(1.1-v);
  var distToNeg = Math.abs(-1.1-v);
  if (distToZero < distToNeg && distToZero < distToPos) {
    return 0;
  }
  if (distToNeg < distToZero && distToNeg < distToPos) {
    return -1.1;
  } 
  return 1.1; // closer to 1.1 case
}

// rotate x faces (R,L,M)
export function rotateXFace(xpos, rad) {
  let M = new THREE.Matrix4();
  M.makeRotationX(rad);
  let cubePos = new THREE.Vector3();
  // perform rotation
  for (let x = 0; x < 3; x++) {
      for (let y = 0; y < 3; y++) {
          for (let z = 0; z < 3; z++) {
              if (round(cubesArray3D[x][y][z].getWorldPosition(cubePos).x) == xpos) {
                  cubesArray3D[x][y][z].matrixAutoUpdate = false;
                  cubesArray3D[x][y][z].matrix.premultiply(M);
                  cubesArray3D[x][y][z].updateMatrixWorld();
              }
          }
      }
  }
}
// rotate y faces (U, D)
export function rotateYFace(ypos, rad) {
  let M = new THREE.Matrix4();
  M.makeRotationY(rad);
  let cubePos = new THREE.Vector3();
  // perform rotation
  for (let x = 0; x < 3; x++) {
      for (let y = 0; y < 3; y++) {
          for (let z = 0; z < 3; z++) {
              if (round(cubesArray3D[x][y][z].getWorldPosition(cubePos).y) == ypos) {
                  cubesArray3D[x][y][z].matrixAutoUpdate = false;
                  cubesArray3D[x][y][z].matrix.premultiply(M);
                  cubesArray3D[x][y][z].updateMatrixWorld();
              }
          }
      }
  }
}
// rotate z faces (F, B)
export function rotateZFace(zpos, rad) {
  let M = new THREE.Matrix4();
  M.makeRotationZ(rad);
  let cubePos = new THREE.Vector3();
  // perform rotation
  for (let x = 0; x < 3; x++) {
      for (let y = 0; y < 3; y++) {
          for (let z = 0; z < 3; z++) {
              if (round(cubesArray3D[x][y][z].getWorldPosition(cubePos).z) == zpos) {
                  cubesArray3D[x][y][z].matrixAutoUpdate = false;
                  cubesArray3D[x][y][z].matrix.premultiply(M);
                  cubesArray3D[x][y][z].updateMatrixWorld();
              }
          }
      }
  }
}