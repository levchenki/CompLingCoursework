FROM node:lts-alpine AS builder
WORKDIR /app_build
COPY package.json .
RUN yarn install
COPY . .
RUN yarn run build

FROM nginx:stable-alpine
COPY --from=builder /app_build/dist /usr/share/nginx/html
#RUN rm /etc/nginx/conf.d/default.conf
#COPY deploy/nginx/nginx.conf /etc/nginx/conf.d
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
