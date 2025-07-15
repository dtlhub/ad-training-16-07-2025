import createRouter, { crud } from '../ext/router.js';
import authMiddleware from '../middlewares/auth.js';
import artist from '../models/artist.js';
import event from '../models/event.js';

export default createRouter(r => {
    r.use(authMiddleware);

    r.use(crud(artist));
    r.use(crud(event));

    r.get('/', async (req, res) => {
        const lables = [];
        const groups = [];

        const data = await artist.aggregate().sortByCount('group');
        data.forEach(item => {
            lables.push(item._id);
            groups.push(item.count);
        });

        res.render('company/dashboard', { lables, groups });
    });
});
