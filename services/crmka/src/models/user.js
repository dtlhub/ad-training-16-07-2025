import { Schema, model } from 'mongoose';

export default model('User', new Schema({
    username: { type: String, unique: true, required: true },
    password: { type: String, required: true },
}));