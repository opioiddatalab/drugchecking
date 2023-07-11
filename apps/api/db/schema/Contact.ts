import mongoose from 'mongoose';
import { isEmail, isMobilePhone } from 'validator';


const contactSchema = new mongoose.Schema({
    name: {
        type: String,
    },
    email:{
        type:String,
        validate:{
              validator: isEmail,
              message: '{VALUE} is not a valid email',
              isAsync: false
            }
    },
    phone: {
        type: String,
        validate: {
            validator: isMobilePhone,
            message: `{VALUE} is not a valid phone number`,
            isAsync: false,
        },
    },
    mailingAddress: {
        city: {
            type: String,
          },
          state: {
            type: String,
          }, 
          address1: {
            type: String,
            required: true,
          }, 
          address2: {
            type: String,
          }, 
          geo: {
            type: Geolocation,
          }
    }
},
{ timestamps: true}
);

const Contact = mongoose.model('Contact', contactSchema);

module.exports = Contact;
