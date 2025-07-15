export default function config(app) {
    app.locals.getFieldTemplate = (prefix, field) => {
        let fieldType;
        
        switch (field.tpl) {
            case 'select':
            case 'textarea':
                fieldType = field.tpl;
                break;
            default:
                fieldType = 'input';
        }

        return `${prefix}/field/${fieldType}`;
    };

    app.locals.prepareFieldValue = (value, field, isInput = false) => {
        if (field.type.name === 'Date') {
            value = value || new Date();
            return isInput ? value.toISOString().substr(0, 10) : value.toLocaleDateString('ru');
        }
        return value;
    }
    
    app.locals.ucFirst = (str) => {
        if (!str) {
            return str;
        }
        return str.charAt(0).toUpperCase() + str.slice(1);
    }
}