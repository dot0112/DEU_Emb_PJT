const express = require("express");
const http = require("http");
const bodyParser = require("body-parser");
const app = express();

app.use(bodyParser.urlencoded({ extended: false }));

// for test
app.use(express.static("../public"));

const server = http.createServer(app);
const PORT = 3000;

const uploadRouter = require("./routes/uploadRoutes");

server.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});

app.use("/upload", uploadRouter);

app.get("/", (req, res) => {
    res.send("ok");
});
