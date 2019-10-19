const express = require('express');
const multer = require('multer');
const BookingController = require('./controllers/BookingController');
const UploadConfig = require('../src/config/upload');

const ProfileController = require('./controllers/ProfileController');
const SessionController = require('./controllers/SessionController');
const SpotController = require('./controllers/SpotController');

const routes = express.Router();
const upload = multer(UploadConfig);



routes.post('/Session' , SessionController.store);
routes.get('/Profileindex' , ProfileController.show);
routes.get('/Spotindex' , SpotController.index);
routes.post('/Spot' , upload.single('thumbnail'), SpotController.store);
routes.post('/spots/:spot_id/bookings',BookingController.Store)
module.exports = routes;