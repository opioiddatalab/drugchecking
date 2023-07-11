import mongoose from 'mongoose';

const inventorySchema = new mongoose.Schema({
  invoiceNumber: {
    type: String,
    required: true,
  },
  agency: {
    // this should refer to the partner schema _id
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Partner',
    required: true,
  },
  date: {
    type: Date,
    default: Date.now,
  },
  serviceType: {
    enum: ['confirmatory', 'research', 'harm reduction', 'other'],
    type: String,
    required: true,
  },
  subServiceType: {
    enum: ['kit purchase', 'startup-kit purchase', 'sample analysis', 'purchase'],
    type: String,
  },
  amountDue: {
    type: Number,
    required: true,
  }, 
  datePaid: {
    type: Date,
  },
  amountPaid: {
    type: Number,
  },
  accountType: {
    enum: ['income', 'other'],
    type: String,
  }  
}, {timestamps: true}
);

const Inventory = mongoose.model('Inventory', inventorySchema);

module.exports = Inventory;
