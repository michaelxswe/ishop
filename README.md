# Shopping Website Backend API

<http://3.15.183.9/docs>

This project provides a backend API for a shopping website, utilizing FastAPI and SQLAlchemy as the ORM to enable seamless CRUD operations with a PostgreSQL database. Implemented essential features, including user registration, secure sign-in with JWT integration, shopping cart management, order submission, and access to order history.


## Database Schemas

![ishop db](pics/ishop.png)

## Tech Stack
    1. FastAPI

    2. SQLAlchemy

    3. PostgreSQL

    4. Docker

    5. AWS Fargate

## Build
    1. clone this repo

    2. install docker desktop

    3. command to build the image: docker build -t ishop .

    4. command to run the container: docker-compose up

    5. go to -> localhost:8000/doc

## How to use

    1. First create a user
    2. Click the sign-in api
    3. Copy the token, click authorize icon, and paste it there
    4. Add items to cart and submit your order!