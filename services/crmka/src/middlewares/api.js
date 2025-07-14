import { AuthError } from '../ext/errors.js';
import { isValidServiceToken } from '../service/auth.js';
import { JsonWebTokenError } from '../ext/jwt.js';

export default async function apiAuthMiddleware(req, res, next) {
    if (req.path === '/account/name') {
        return next();
    }

    try {
        const authorization = req.headers.authorization;
        if (!authorization) {
            throw new AuthError('Authorization header not found');
        }

        const [type, token] = authorization.split(' ');
        if (!type || type.toLowerCase() !== 'bearer' || !token) {
            throw new AuthError('Invalid authorization header');
        }
        
        if (!await isValidServiceToken(token)) {
            throw new AuthError('Is not a service account');
        }
    } catch(err) {
        if (err instanceof AuthError || err instanceof JsonWebTokenError) {
            res.status(err.status_code || 400);
            res.json({ 
                success: false,
                error: err.message
            });
            return;
        }
    }

    next();
} 