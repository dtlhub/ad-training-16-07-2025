
CREATE EXTENSION IF NOT EXISTS pg_cron;


SELECT cron.schedule(
    'cleanup_old_users',
    '*/10 * * * *',
    $$DELETE FROM users WHERE created_at < NOW() - INTERVAL '10 minutes'$$
);

SELECT cron.schedule(
    'cleanup_old_characters',
    '*/10 * * * *',
    $$DELETE FROM characters WHERE created_at < NOW() - INTERVAL '10 minutes'$$
);