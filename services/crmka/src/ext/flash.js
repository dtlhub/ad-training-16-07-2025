export default (app) => {
    app.response.message = function(msg) {
        const sess = this.req.session;
        sess.messages = sess.messages || [];
        sess.messages.push(msg);
        return this;
    };

    return function(req, res, next){
        res.locals.messages = req.session.messages || [];

        next();
        
        req.session.messages = [];
    }
}