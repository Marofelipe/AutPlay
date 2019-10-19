const mongoose = require('mongoose');

const UserSchema = new mongoose.Schema({
    email: String,
    nome: String,
    NivelAdm: String,
    Aluno: Array,       
})
module.exports = mongoose.model('User',UserSchema);