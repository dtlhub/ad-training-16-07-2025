import { connect } from 'mongoose';

import userModel from './models/user.js';
import config from './config.js';
import { hashPassword } from './service/auth.js';

async function initAdminUser() {
    await userModel.updateOne(
        { username: 'admin' }, 
        { 
            username: 'admin', 
            password: await hashPassword(config.ADMIN_PASSWORD),
            is_admin: true 
        }, 
        { upsert: true }
    );
}

connect(config.DB_URL);

export async function migration() {
    await initAdminUser();
}