export default function errorMiddleware(err, req, res, next) {
    res.status(err.status_code || 500);
    const obj = { 
        success:false, 
        error: err.message, 
        stack: err.stack
    };

    if (req.path.startsWith('/api')) {
        res.json(obj);
    } else {
        res.render('error', obj);
    }
} 