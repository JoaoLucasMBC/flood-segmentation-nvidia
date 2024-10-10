//VERSION=3

function setup() {
    return {
        input: [{
            bands: ["B02", "B03", "B04", "SCL"]
        }],
        output: {
            bands: 4 
        }
    };
}

function evaluatePixel(sample) {
    var water = (sample.SCL === 6);

    if (water) {
        return [0, 0, 1.0, 1];
    } else {
        return [sample.B04, sample.B03, sample.B02, 1];
    }
}