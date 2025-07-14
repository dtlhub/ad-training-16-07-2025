import jwt_ from 'jsonwebtoken';
import config from '../config.js';

const key = config.JWT_PUBLIC_KEY;

export function verify(token) {
    return jwt_.verify(token, key, { algorithms: ['RS256'] });
}

export function sign(data) {
    return jwt_.sign(data, key);
}

export const JsonWebTokenError = jwt_.JsonWebTokenError;