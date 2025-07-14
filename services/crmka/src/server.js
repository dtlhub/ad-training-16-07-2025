import path from 'path';
import express from 'express';
import session from 'express-session';

import renderConfig from './ext/render.js';
import config from './config.js';
import { migration } from './db.js'; 
import errorMiddleware from './middlewares/error.js';
import indexRoutes from './routes/index.js';
import authRoutes from './routes/auth.js';
import companyRoutes from './routes/company.js';
import apiRoutes from './routes/api.js';

const app = express();

renderConfig(app);

app.set('view engine', 'ejs');
app.set('views', path.join(process.cwd(), 'views'));

app.use(express.static(path.join(process.cwd(), 'public')));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use(session({
    resave: false,
    secret: config.SESSION_SECRET,
    cookie: { secure: false },
    saveUninitialized: false
}));

app.use(indexRoutes);
app.use(authRoutes);
app.use('/company', companyRoutes);
app.use('/api', apiRoutes);
app.use(errorMiddleware);

await migration();

app.listen(config.PORT, () => {
    console.log(`Listen port ${config.PORT}`);
    console.log(`Printenv:`, config);
});
