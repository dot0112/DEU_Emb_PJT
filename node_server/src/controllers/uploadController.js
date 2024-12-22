const tf = require("@tensorflow/tfjs");
const jpeg = require("jpeg-js");
const yolov5_weight = "http://localhost:3000/yolov5/model.json";

let detector;

async function createDetector() {
  if (!detector) {
    // 모델이 아직 로드되지 않았다면
    detector = await tf.loadGraphModel(yolov5_weight);
  }
  return detector; // 이미 로드된 모델 반환
}

async function predictImage(imageRawData) {
  const detector = await createDetector();
  const [modelWidth, modelHeight] = detector.inputs[0].shape.slice(1, 3);

  const imageData = jpeg.decode(imageRawData); // { width, height, data }

  const input = tf.tidy(() => {
    return tf.image
      .resizeBilinear(tf.browser.fromPixels(imageData), [
        modelWidth,
        modelHeight,
      ])
      .div(255.0) // Normalize the image data to [0, 1]
      .expandDims(0); // Add batch dimension
  });

  let detect_res = await detector.executeAsync(input);

  const [boxes, scores, classes, valid_detections] = detect_res;
  const boxes_data = boxes.dataSync();
  const valid_detections_data = valid_detections.dataSync()[0];
  tf.dispose(detect_res);

  let result = [];
  for (let i = 0; i < valid_detections_data; ++i) {
    result.push(boxes_data.slice(i * 4, (i + 1) * 4));
  }

  return result;
}

module.exports = { predictImage };
