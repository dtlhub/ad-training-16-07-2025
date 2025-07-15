import createRouter from '../ext/router.js';

export default createRouter(r => {
    r.get('/', (req, res) => {
        const path = req.session.user ? '/company' : '/login';   
        res.redirect(path);
    });
});
