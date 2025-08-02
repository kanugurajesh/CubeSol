import { rotateXFace, rotateYFace, rotateZFace } from "./rubik.js";
import { Keyframe, Motion } from "./motion.js"


export const Faces = Object.freeze({
    RIGHT: "right",
    LEFT: "left",
    MID: "mid",
    UP: "up",
    DOWN: "down",
    FRONT: "front",
    BACK: "back",
});

const face_animation_status = {
    [Faces.RIGHT]: false,
    [Faces.LEFT]: false,
    [Faces.MID]: false,
    [Faces.UP]: false,
    [Faces.DOWN]: false,
    [Faces.FRONT]: false,
    [Faces.BACK]: false,
};

// functions to call to update transformation matrices
// avars=[xpos (x world coordinate for cubelets on the face), theta (rad amount to rotate by)]
function rotateRFace(avars) {
    rotateXFace(avars[0], avars[1]);
}
function rotateLFace(avars) {
    rotateXFace(avars[0], avars[1]);
}
function rotateMFace(avars) {
    rotateXFace(avars[0], avars[1]);
}
function rotateUFace(avars) {
    rotateYFace(avars[0], avars[1]);
}
function rotateDFace(avars) {
    rotateYFace(avars[0], avars[1]);
}
function rotateFFace(avars) {
    rotateZFace(avars[0], avars[1]);
}
function rotateBFace(avars) {
    rotateZFace(avars[0], avars[1]);
}

///////////////////////////////////////////////////////////////////////////////////////
// KEYFRAME ANIMATIONS FOR EACH FACE ROTATION
///////////////////////////////////////////////////////////////////////////////////////

// Motion-related variables
const motions = {
    right: null,
    left: null,
    mid: null,
    up: null,
    down: null,
    front: null,
    back: null
};

// in seconds
const keyFrameDt = 0.2;
export const duration = 3 * keyFrameDt;

export function initMotions(clockwise=true) {
  let theta = Math.PI / 8;
  if (!clockwise) theta = -theta;
  motions.right = new Motion(rotateRFace);
  motions.left = new Motion(rotateLFace);
  motions.mid = new Motion(rotateMFace);
  motions.up = new Motion(rotateUFace);
  motions.down = new Motion(rotateDFace);
  motions.front = new Motion(rotateFFace);
  motions.back = new Motion(rotateBFace);
  // keyframes for motion: name, time, avars=[xpos, theta (rad)]
  motions.right.addKeyFrame(new Keyframe('beg', 0.0, [1.1, 0]));
  motions.right.addKeyFrame(new Keyframe('beg', keyFrameDt, [1.1, -theta]));
  motions.right.addKeyFrame(new Keyframe('mid', keyFrameDt * 2, [1.1, -theta]));
  motions.right.addKeyFrame(new Keyframe('end', duration, [1.1, 0]));

  motions.left.addKeyFrame(new Keyframe('beg', 0.0, [-1.1, 0]));
  motions.left.addKeyFrame(new Keyframe('beg', keyFrameDt, [-1.1, theta]));
  motions.left.addKeyFrame(new Keyframe('mid', keyFrameDt * 2, [-1.1, theta]));
  motions.left.addKeyFrame(new Keyframe('end', duration, [-1.1, 0]));

  motions.mid.addKeyFrame(new Keyframe('beg', 0.0, [0, 0]));
  motions.mid.addKeyFrame(new Keyframe('beg', keyFrameDt, [0, -theta]));
  motions.mid.addKeyFrame(new Keyframe('mid', keyFrameDt * 2, [0, -theta]));
  motions.mid.addKeyFrame(new Keyframe('end', duration, [0, 0]));

  motions.up.addKeyFrame(new Keyframe('beg', 0.0, [1.1, 0]));
  motions.up.addKeyFrame(new Keyframe('beg', keyFrameDt, [1.1, -theta]));
  motions.up.addKeyFrame(new Keyframe('mid', keyFrameDt * 2, [1.1, -theta]));
  motions.up.addKeyFrame(new Keyframe('end', duration, [1.1, 0]));

  motions.down.addKeyFrame(new Keyframe('beg', 0.0, [-1.1, 0]));
  motions.down.addKeyFrame(new Keyframe('beg', keyFrameDt, [-1.1, theta]));
  motions.down.addKeyFrame(new Keyframe('mid', keyFrameDt * 2, [-1.1, theta]));
  motions.down.addKeyFrame(new Keyframe('end', duration, [-1.1, 0]));

  motions.front.addKeyFrame(new Keyframe('beg', 0.0, [1.1, 0]));
  motions.front.addKeyFrame(new Keyframe('beg', keyFrameDt, [1.1, -theta]));
  motions.front.addKeyFrame(new Keyframe('mid', keyFrameDt * 2, [1.1, -theta]));
  motions.front.addKeyFrame(new Keyframe('end', duration, [1.1, 0]));

  motions.back.addKeyFrame(new Keyframe('beg', 0.0, [-1.1, 0]));
  motions.back.addKeyFrame(new Keyframe('beg', keyFrameDt, [-1.1, theta]));
  motions.back.addKeyFrame(new Keyframe('mid', keyFrameDt * 2, [-1.1, theta]));
  motions.back.addKeyFrame(new Keyframe('end', duration, [-1.1, 0]));
}


function stopAnimation(face) {
    face_animation_status[face] = false;
}

export function animate(face) {
    face_animation_status[face] = true;
    return new Promise(resolve => setTimeout(resolve, 700));
}

export function updateAnimations(dt=0.1) {
    for (const face of Object.values(Faces)) {
        if (face_animation_status[face]) {
            let finished = motions[face].timestep(dt);
            if (finished) stopAnimation(face);
            break;
        }
    }
}