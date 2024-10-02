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
    var cloud = (sample.SCL === 3 || sample.SCL === 8 || sample.SCL === 9 || sample.SCL === 10);

    if (cloud) {
        return [1.0, 1.0, 1.0, 1];
    } else {
        return [sample.B04, sample.B03, sample.B02, 1];
    }
}