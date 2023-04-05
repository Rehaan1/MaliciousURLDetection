FROM node:18-alpine

RUN apk update -y && apk add python3 -y
RUN apk add py3-pip -y && pip3 install -U setuptools -y && pip3 install pandas joblib -y && pip3 install -U scikit-learn==0.21.3 -y

ENV PORT=3000
WORKDIR /app
EXPOSE 3000

COPY ["package.json", "package-lock.json*", "./"]
RUN npm install

COPY . .
CMD [ "node", "app.js" ]
