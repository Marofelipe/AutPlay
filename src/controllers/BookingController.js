const Booking = require('../models/booking');

module.exports ={
    async Store(req,res){
        const {user_id} = req.headers;
        const {spot_id} = req.params;
        const {data} = req.body;
        
        const booking = await Booking.create({
            user: user_id,
            spot: spot_id,
            data,
            
        });
        return res.json(booking);
        

    }
};