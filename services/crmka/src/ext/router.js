import express from 'express';

export default function createRouter(callback) {
    const router = express.Router();
    callback(router);
    return router;
}

export function crud(model) {
    const name = model.modelName.toLowerCase();
    const collection = `${name}s`;
    const indexURI = `/${collection}`;
    const isNew = (id) => id === 'new';

    return createRouter(r => {
        const schema = model.schema.obj;

        r.get(indexURI, async (req, res) => {
            res.render('crud/table', {
                name,
                schema,
                items: await model.find({}).sort({ _id: -1 })
            });
        });

        r.route(`${indexURI}/:id`)
            .get(async (req, res) => {
                const id = req.params.id;
                const entity = !isNew(id) ? await model.findById(id) : null;
                res.render('crud/form', { id, name, schema, entity });
            })
            .post(async (req, res) => {
                const id = req.params.id;
                if (isNew(id)) {
                    await model.create(req.body);
                } else {
                    await model.findByIdAndUpdate(id, req.body);                
                }
                res.redirect(`..${indexURI}`);
            });
    });
}