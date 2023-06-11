const fs = require('fs');
const express = require('express');

const app = express();
const port = process.env.PORT || 3000;

const canudb_db = "CanuDB/";

function canudbWrite(table, data) {
    console.log("[CanuDB] write > data " + data + " to table > " + table);
    fs.writeFileSync(canudb_db + table + ".canu", data);
}

function canudbRead(table, callback) {
    const recvData = fs.readFileSync(canudb_db + table + ".canu", "utf8");
    console.log("[CanuDB] read > data " + recvData + " from table > " + table);
    callback(recvData);
}

app.use(express.json());

// Endpoint to fetch the key
app.post('/key', (req, res) => {
    const key = req.query.key;
    console.log("query " + req.query)
    console.log("params " + req.params.dictionary)
    console.log("body " + req.body)
    console.log(key)
    canudbWrite("chei", key);
    res.send("Key received and written to the database.");
});

app.get('/key-rec', (req, res) => {
    canudbRead("chei", function (key) {
        console.log("Key received and read from the database. " + key);
        res.send({ key: key });
    });
});

// Serve the index.html file
app.use(express.static(__dirname));

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port} sau http://192.168.56.1:${port}`);
});
