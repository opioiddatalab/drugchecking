import mongoose from 'mongoose';

const programSchema = new mongoose.Schema({
  name: {
    type: String,
  },
  fullName: {
    type: String,
    required: true,
  },
  contacts: {
    type: [mongoose.Schema.Types.ObjectId],
  },
  version: {
    type: String,
  },
  description: {
    type: String,
    maxlength: 500,
  },
  location: {
      city: {
        type: String,
      },
      county: {
        type: String,
      },
      state: {
        type: String,
      }, 
      country: {
        type: String,
        default: 'US',
      }, 
      geo: {
        type: Geolocation,
      }
  },
  type: {
    enum: ['HR', 'Confirmatory', 'Health Department', 'User Union', 'Research', 'HR/Confirmatory', 'Other'],
  },
  dateJoined: {
    type: Date,
    default: Date.now,
  },
  code: {
    type: String, 
  }, 
  communityLiaison: {
    type: User,
  }
},
{ timestamps: true}
);

const Program = mongoose.model('Program', programSchema);

module.exports = Program;
