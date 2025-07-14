import bcrypt from 'bcrypt';

import userModel from '../models/user.js';
import * as jwt from '../ext/jwt.js';
import config from '../config.js';

const saltRounds = 10;

export default async function authenticate(username, password) {
    const user = await userModel.findOne({ username });
    if (user && await bcrypt.compare(password, user.password)) {
        return user;
    }
    return false;
}

export async function hashPassword(password) {
    return bcrypt.hash(password, saltRounds);
}

export async function isValidServiceToken(token) {
    const data = jwt.verify(token); 
    return data.account?.name === config.SERVICE_ACCOUNT_NAME;
}
