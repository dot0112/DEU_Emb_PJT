const tf = require("@tensorflow/tfjs");

// 데이터 준비
const 온도 = [20, 21, 22, 23]; // 독립변수
const 판매량 = [40, 42, 44, 46]; // 종속변수

const 원인 = tf.tensor(온도);
const 결과 = tf.tensor(판매량);

// 모델 생성
const model = tf.sequential();
model.add(tf.layers.dense({ units: 1, inputShape: [1] }));

// 모델 컴파일
model.compile({ optimizer: "sgd", loss: "meanSquaredError" });

// 모델 훈련
model.fit(원인, 결과, { epochs: 100 }).then(() => {
    // 예측하기
    const 새로운온도 = tf.tensor([24]);
    const 예측판매량 = model.predict(새로운온도);
    예측판매량.print(); // 예측된 판매량 출력
});
