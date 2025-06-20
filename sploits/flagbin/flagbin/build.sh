docker run --rm -v $(pwd):/host -w /host alpine:3.22.0 sh -c "apk add --no-cache gcc make musl-dev && make build"
