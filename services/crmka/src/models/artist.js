import { Schema, model } from 'mongoose';

const groups = ['solo', 'duet', 'troupe'];
const spectialization = ['clown'];

export default model('Artist', new Schema({
    name: { type: String, unique: true, required: true },
    contact: { type: String, required: true },
    group: { type: String, enum: groups, required: true, tpl: 'select' },
    spectialization: { type: String, enum: spectialization, required: true, tpl: 'select' },
    fee: { type: Number, required: true, tpl: 'number' }
}));