import { Schema, model } from 'mongoose';

export default model('Event', new Schema({
    name: { type: String, unique: true, required: true },
    date: { type: Date, required: true, tpl: 'date' },
    description: { type: String, unique: true, required: true, tpl: 'textarea' },
    raiting: { type: Number, required: true, tpl: 'number' }
}, { timestamps: true }));