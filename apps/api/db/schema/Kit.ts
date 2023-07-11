// create basic mongoose schema for druglist
import mongoose from 'mongoose';
import { AbundanceLevels, AnalysisMethod, KitStatus } from 'types';

const kitSchema = new mongoose.Schema({
   sampleId: {
        type: String,
        required: true,
    },
    kitStatus: { // where is the bag?
        type: String,
        enum: KitStatus
    },
    dateReturned: {
        type: Date,
    },
    analysisComplete: {
        type: Boolean,
        default: false,
    },
    invoiceDate: {
        type: Date,
        required: false,
    },
    substance: {
        type: String,
        required: true,
    },
    abundance: {
        type: String,
        enum: AbundanceLevels,
    },
    method: {
        type: String,
        enum: AnalysisMethod
    }, 
    labNotes: {
        type: String,
    },
    spectraUploaded: {
        type: Boolean,
    },
}, {timestamps: true});

const Kit = mongoose.model('Kit', kitSchema);

module.exports = Kit;


