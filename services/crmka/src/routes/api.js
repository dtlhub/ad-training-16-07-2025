import config from '../config.js';
import createRouter from '../ext/router.js';
import apiAuthMiddleware from '../middlewares/api.js';
import { load } from '../service/dynLoader.js';

const isAllow = (moduleName) => {
    return /^.+\/models\/[a-z]+\.js$/.test(moduleName) && moduleName?.indexOf('user') === -1;
}

export default createRouter(r => {
    r.use(apiAuthMiddleware);

    r.get('/account/name', (req, res) => {
        res.json({account_name: config.SERVICE_ACCOUNT_NAME});
    });

    r.get('/entity/:id', async (req, res) => {
        const { default: model } = await load(req.query.path, isAllow);
        const entity = await model.findById(req.params.id);
        if (!entity) {
            return res.status(404).json({ success: false });
        }
        res.json({ success: true, entity });
    });

    r.post('/entity/add', async (req, res) => {
        const { default: model } = await load(req.query.path, isAllow);
        const entity = await model.create(req.body);
        res.json({ success: true, entity: entity._doc });
    });
})