# Shopping App Backend

This project provides a complete backend API for a shopping app, featuring user registration, secure login via JWT, cart management, and order processing with historical tracking.

<http://18.119.129.40/docs>

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