//index , show , store , update , destroy
const User = require('../models/User');
module.exports = {
    async store(req,res){
        const {nome} = req.body;
        const {email} = req.body;
        const {NivelAdm} = req.body;
        const {Aluno} = req.body;
        
        let user = await User.findOne({ 
            email,
            nome,
            NivelAdm

         });
        if(!user){
            user = await User.create({
                NivelAdm,
                email,
                nome,
                Aluno : Aluno.split(',').map( Aluno => Aluno.trim()),
            })

        }
        return res.json(user);
    }
};