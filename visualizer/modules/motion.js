////////////////////////////////////////////////////////////
// Keyframe and Motion classes (adapted from CPSC 314 A3)
////////////////////////////////////////////////////////////

class Keyframe {
    constructor(name,time,avars) {
        this.name = name;
        this.time = time;
        this.avars = avars;
    }
}

class Motion {
    constructor(setMatricesFunc) {
        this.keyFrameArray = [];          // list of keyframes
        this.maxTime = 0.0;               // time of last keyframe
        this.currTime = 0.0;              // current playback time
        this.updateMatrices = setMatricesFunc;    // function to call to update transformation matrices
    };
    reset() {                     // go back to first keyframe
        this.currTime = 0.0;
    };
    addKeyFrame(keyframe) {               // add a new keyframe at end of list
        this.keyFrameArray.push(keyframe);
        if (keyframe.time > this.maxTime)
            this.maxTime = keyframe.time;
    };
    timestep(dt) {                //  take a time-step;  loop to beginning if at end
        this.currTime += dt;
        if (this.currTime > this.maxTime) {
            this.currTime = 0;
            return 1; // alert finished (reset)
        }
        let avars = this.getAvars();
        this.updateMatrices(avars);
        return 0; // alert stepped
    };
    getAvars() {                  //  compute interpolated values for the current time
        let i = 1;
        while (this.currTime > this.keyFrameArray[i].time)       // find the right pair of keyframes
            i++;
        let avars = [];
        for (let n=0; n<this.keyFrameArray[i-1].avars.length; n++) {   // interpolate the values
            let y0 = this.keyFrameArray[i-1].avars[n];
            let y1 = this.keyFrameArray[i].avars[n];
            let x0 = this.keyFrameArray[i-1].time;
            let x1 = this.keyFrameArray[i].time;
            let x = this.currTime;
            let y = y0 + (y1-y0)*(x-x0)/(x1-x0);    // linearly interpolate
            avars.push(y);
        }
        return avars;         // return list of interpolated avars
    };
}

export { Keyframe, Motion };
