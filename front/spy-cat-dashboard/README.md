

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev

```
if you have problems with libs-dependecies use "npm install " and after that use "npm run dev"
Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.


This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

To deploy backend , firstly decoment in main.py line 23 to create tables in the database, and actually you need
to create the DATABASE with name catapi, or you can change config in "env" File if you are using in postgres another password or login
Please, in the root of backend directory use "poetry install" command to install all needed dependencies
After that just run main.py and you may go to http://localhost:8080/docs to see the API endpoints

I could make this task much better but unfortunately i dont have time, 6 hours is to much , 

I completed this task in two and a half hours, and most importantly,
the main principles of writing backend logic have been adhered to.


The backend was written in an asynchronous context, and I implemented validation,
but since I unfortunately cannot dedicate more than two and a half hours to the task,
the responses may not always be clear to the client.