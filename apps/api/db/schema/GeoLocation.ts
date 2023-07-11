import mongoose from 'mongoose';

const geoLocationSchema = new mongoose.Schema({
    name: String,
    location: {
        type: {type: String, enum: ['Point']},
        coordinates: {type: [Number], default: [0, 0]}
    }
},
{ timestamps: true}
);

const GeoLocation = mongoose.model('GeoLocation', geoLocationSchema);

module.exports = GeoLocation;
