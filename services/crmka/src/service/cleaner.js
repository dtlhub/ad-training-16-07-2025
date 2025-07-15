import { scheduleJob } from 'node-schedule';
import artist from '../models/artist.js';

export default function startCleaner(min) {
    scheduleJob(`*/${min} * * * *`, async function() {
        console.log('run cleaner job');
        const date = new Date();
        date.setMinutes(date.getMinutes() - min);
        await artist.deleteMany({ createdAt: { $lte: date } });
    });
}