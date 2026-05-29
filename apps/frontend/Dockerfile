# Build stage
FROM node:22-alpine AS builder
WORKDIR /build
COPY package.json package-lock.json* ./
RUN npm ci --no-audit
COPY . .
RUN npm run build

# Runtime stage
FROM node:22-alpine
WORKDIR /app
RUN addgroup -S -g 1001 app && \
    adduser -S -u 1001 -G app app
COPY --from=builder /build/.output ./.output
COPY --from=builder /build/node_modules ./node_modules
COPY --from=builder /build/package.json ./package.json
USER app
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000',r=>process.exit(r.statusCode===200?0:1)).on('error',()=>process.exit(1))"
CMD ["npx", "nuxi", "preview", "--port", "3000"]
