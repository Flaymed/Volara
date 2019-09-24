const express = require('express');
app = express();
const sqlite3 = require('sqlite3').verbose();

let db = new sqlite3.Database('./kingdombot/database/main.db');
require('events').EventEmitter.defaultMaxListeners = 0;

app.set('view engine', 'ejs')

app.get('/', function(req, res) {
  res.render('../public/index')
})

app.listen(8000);
console.log('Server is active on port 8000')
