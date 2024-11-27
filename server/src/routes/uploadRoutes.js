const express = require("express");
const router = express.Router();
const formidable = require("formidable");
const { Worker } = require("worker_threads");

router.post("/", async (req, res, next) => {
    try {
        const form = new formidable.IncomingForm();
        form.parse(req, (err, fields, files) => {
            let file = files.image[0];
            const imagePath = file.filepath;

            const worker = new Worker("./controllers/uploadWorker.js", {
                workerData: imagePath,
            });

            worker.on("message", (result) => {
                res.json({ result });
            });

            worker.on("error", (error) => {
                res.status(500).send(error.message);
            });

            worker.on("exit", (code) => {
                if (code !== 0) {
                    res.status(500).send(
                        `Worker stopped with exit code ${code}`
                    );
                }
            });
        });
    } catch (err) {
        console.log("err: ", err);
        next(err);
    }
});

module.exports = router;
