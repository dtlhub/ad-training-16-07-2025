import createRouter from '../ext/router.js';
import authenticate from '../service/auth.js';

export default createRouter(r => {
    r.get('/login', (req, res) => {
        res.render('login');
    });

    r.post('/login', async (req, res) => {
        const user = await authenticate(req.body.username, req.body.password);
        if (user) {
            req.session.user = user;
            return res.redirect('/company');
        }
        res.render('login', {
            errors: 'Invalid username or password'
        });
    });

    r.get('/logout', (req, res) => {
        req.session.user = null;
        res.redirect('/login');
    });
});