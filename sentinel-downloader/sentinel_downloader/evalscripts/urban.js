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
    var not_vegetation = (sample.SCL === 5);

    if (not_vegetation) {
        return [1.0, 0, 1.0, 1];
    } else {
        return [sample.B04, sample.B03, sample.B02, 1];
    }
}