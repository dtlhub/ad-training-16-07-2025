import createRouter, { crud } from '../ext/router.js';
import authMiddleware from '../middlewares/auth.js';
import artist from '../models/artist.js';
import event from '../models/event.js';

export default createRouter(r => {
    r.use(authMiddleware);

    r.use(crud(artist));
    r.use(crud(event));

    r.get('/', (req, res) => {
        res.render('company/dashboard');
    });
});
