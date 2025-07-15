import process from 'process';
import dotenv from 'dotenv';

const config = {};

const result = dotenv.config({
    processEnv: config,
    path: process.cwd() + '/.env'
});

if (result.error) {
    throw result.error;
}

export default config;