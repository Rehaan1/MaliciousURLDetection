FROM node:18
RUN apt-get update || : && apt-get install python3 -y

RUN apt install python3-pip -y
RUN pip3 install pandas -y
RUN pip3 install joblib -y
RUN pip3 install -U scikit-learn==0.21.3 -y

ENV PORT=3000
WORKDIR /app
EXPOSE 3000

COPY ["package.json", "package-lock.json*", "./"]
RUN npm install

COPY . .
CMD [ "node", "app.js" ]