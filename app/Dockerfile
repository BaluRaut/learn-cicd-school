# 🍱 The lunchbox recipe — the Docker school reads every line of a file like this.
FROM node:22-alpine
WORKDIR /app
COPY package.json server.js ./
ARG APP_VERSION=dev                 # CI passes the commit SHA here (lesson 07)
ENV APP_VERSION=$APP_VERSION
ENV PORT=3000
EXPOSE 3000
USER node
CMD ["node", "server.js"]
