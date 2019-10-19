const express = require('express');
const routes = require('./routes');
const mongoose = require('mongoose');


const app = express();
mongoose.connect('mongodb+srv://Marcos_tsz:Marofelipe323536@aulaguipo-ikkxy.mongodb.net/Semana09?retryWrites=true&w=majority',{
    useNewUrlParser:true,
    useUnifiedTopology:true,
});
app.use(express.json());
app.use(routes);    
app.listen(3000);