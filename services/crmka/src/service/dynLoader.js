import { DynamicLoadError } from '../ext/errors.js';

const cache = {};

export async function load(path, isAllow) {
    if (isAllow && !isAllow(path)) {
        throw new DynamicLoadError(`Path "${path}" is no allowd`, { path });
    }
    if (!(path in cache)) {
        cache[path] = await import(path);
    }
    return cache[path];
}