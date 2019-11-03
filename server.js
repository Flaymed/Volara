const express = require('express');
app = express();
const sqlite3 = require('sqlite3').verbose();

let db = new sqlite3.Database('./kingdombot/database/main.db');
require('events').EventEmitter.defaultMaxListeners = 0;

app.get('/', function(req, res) {
  res.sendFile(__dirname + '/public/index.html');
})

app.get('/images/Tower.png', function(req, res) {
  res.sendFile(__dirname + '/public/images/Tower.png')
})

app.get('/js/homepage.js', function(req, res) {
  res.sendFile(__dirname + '/public/js/homepage.js')
})

app.listen(8000);
console.log('Server is active on port 8000')
