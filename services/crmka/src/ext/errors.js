export class HttpError extends Error {
    constructor(message, options) {
        super(message, options);
        this.stauts_code = options?.stauts_code || 500;
    }

    getStatusCode() {
        return this.stauts_code;
    }   
}

export class AuthError extends HttpError {
    constructor(message, options) {
        super(message, {...options, stauts_code: 401});
    }
}

export class DynamicLoadError extends Error {
    constructor(message, options) {
        super(message, options);
        this.path = options.path;
    }

    getPath() {
        return this.path;
    }  
}