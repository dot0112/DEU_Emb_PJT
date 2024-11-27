const { parentPort, workerData } = require("worker_threads");
const fs = require("fs");
const uploadController = require("../controllers/uploadController");

function processImage(imagePath) {
    return new Promise((resolve, reject) => {
        const readStream = fs.createReadStream(imagePath);
        let chunks = [];
        readStream.on("data", (chunk) => {
            chunks.push(chunk);
        });

        readStream.on("end", async () => {
            let imageBuffer = Buffer.concat(chunks);
            let result = await uploadController.predictImage(imageBuffer);
            resolve(result);
        });

        readStream.on("error", (err) => {
            reject(`Error reading file: ${err.message}`);
        });
    });
}

processImage(workerData)
    .then((result) => parentPort.postMessage(result))
    .catch((err) => parentPort.postMessage(err));
