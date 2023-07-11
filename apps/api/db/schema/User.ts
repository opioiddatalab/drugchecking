import mongoose from 'mongoose';
import isEmail from 'validator/lib/isEmail';
import  crypto from 'crypto';
import jwt from 'jsonwebtoken';
import secret from '../config.js';


const UserSchema = new mongoose.Schema({
    username: {
        type: String, 
        lowercase: true, 
        required: [true, "can't be blank"], 
        match: [/^[a-zA-Z0-9]+$/, 'is invalid'],
        index: true
    },
    email:{
        type:String,
        validate:{
              validator: isEmail,
              message: '{VALUE} is not a valid email',
              isAsync: false
            },
        index: true,
    },
  hash: String,
  salt: String
}, {timestamps: true});

UserSchema.methods.setPassword = function(password){
  this.salt = crypto.randomBytes(16).toString('hex');
  this.hash = crypto.pbkdf2Sync(password, this.salt, 10000, 512, 'sha512').toString('hex');
};

UserSchema.methods.validPassword = function(password) {
    var hash = crypto.pbkdf2Sync(password, this.salt, 10000, 512, 'sha512').toString('hex');
    return this.hash === hash;
};
// Create a method on the user model to generate a JWT
UserSchema.methods.generateJWT = function() {
    var today = new Date();
    var exp = new Date(today);
    exp.setDate(today.getDate() + 60); // 60 days from now
    // The first argument is the information we want to include in the token
    // The second argument is the secret key used to sign/signature the token
    // The third argument is the options object
    return jwt.sign({
        id: this._id,
        username: this.username,
        exp: exp.getTime() / 1000,
    }, secret);
};

// Create a method to get the JSON representation of a user for authentication
UserSchema.methods.toAuthJSON = function() {
    return {
        _id: this._id,
        username: this.username,
        email: this.email,
        token: this.generateJWT(),
    };
};


mongoose.model('User', UserSchema);