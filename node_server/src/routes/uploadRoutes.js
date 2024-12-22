const express = require("express");
const router = express.Router();
const formidable = require("formidable");
const { Worker } = require("worker_threads");

router.post("/", async (req, res, next) => {
  try {
    const form = new formidable.IncomingForm({
      multiples: true,
      keepExtensions: true,
    });
    form.parse(req, (err, fields, files) => {
      if (err) {
        console.error(err);
        return res.status(500).send("파일 파싱 중 오류가 발생했습니다.");
      }

      if (!files.images) {
        return res.status(400).send("이미지 파일이 없습니다.");
      }

      let file = Array.isArray(files.images) ? files.images[0] : files.images;
      const imagePath = file.filepath;

      const worker = new Worker("./src/controllers/uploadWorker.js", {
        workerData: imagePath,
      });

      worker.on("message", (result) => {
        return res.status(200).send("asdf");
      });

      worker.on("error", (error) => {
        console.error(error);
        return res.status(500).send(error.message);
      });
    });
  } catch (err) {
    console.log("err: ", err);
    return res.status(400).send(error);
  }
});

module.exports = router;
