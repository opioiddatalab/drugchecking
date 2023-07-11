import mongoose from 'mongoose';
import { CompoundClass, SubstanceCommonRole } from 'types';

const druglistSchema = new mongoose.Schema({
    chemicalName: {
        type: String,
        required: true,
    },
    pronunciation: {
        type: String,
    },
    compoundClass: {
        type: String,
        enum: CompoundClass
    },
    commonRole: {
        type: String,
        enum: SubstanceCommonRole,    
    },
    notes: {
        type: String,
        maxLength: 500,
    },
    synonyms: {
        type: [String],
    },
    vernacular: {
        type: String,
    },
    flag: {
        type: Boolean,
        default: false,
    },
}, {timestamps: true});

const DrugList = mongoose.model('DrugList', druglistSchema);

module.exports = DrugList;


