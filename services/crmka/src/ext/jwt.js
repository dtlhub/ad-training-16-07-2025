import jwt_ from 'jsonwebtoken';
import config from '../config.js';

export function verify(token) {
    return jwt_.verify(token, config.JWT_PUBLIC_KEY, { algorithms: ['RS256'] });
}

export const JsonWebTokenError = jwt_.JsonWebTokenError;