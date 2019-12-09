const express = require('express');

const app = express();

app.use(express.json());
app.use(express.urlencoded({extended:false}));

var apiRouter = require('./routes/api.js')
app.use('/api/', apiRouter);

app.listen(process.env.PORT || 8000);
