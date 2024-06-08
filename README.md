# RAKT Food Trucks

RAKT Food Trucks is a Django project that allows you to easily find nearby food trucks around San Francisco. 🚚🍔🌮

# 🌐 Live Demo

Web App - https://rakt-web.vercel.app/


API - https://rakt-food-trucks-production-7cb4.up.railway.app/api/foodtrucks/?long=-122.4&lat=37.7&searchRadius=5000


## Installation and Configuration

To get started with FoodTruck in a Dockerized environment, follow these steps:

1. Clone this repository to your local machine.
2. Make sure you have Docker and docker-compose installed on your machine.
3. Change the `.env.example` to `.env` file in the root directory of the project.
4. Build and run the Docker image using docker-compose (this might take a few mins):
    ```
    docker-compose up -d --build
    ```
    ```
    docker-compose up
    ```
    then open new terminal 
    ```
    docker-compose exec web python manage.py makemigrations
    ```
    ```
    docker-compose exec web python manage.py migrate
    ```
  
  
    This command will build the Docker image based on the Dockerfile and start the containers defined in the docker-compose.yaml file.
7. Access the FoodTruck application by navigating to `http://localhost:8000` in your web browser.

## Approach

My approach to solve this problem is to build an API that allows users to retrieve nearby food trucks based on their location, search radius, and other filters. However, if the result is less than 5, we will ignore the radius parameter and retrieve the 5 closest food trucks based on the location and other parameters.

To achieve this, we will utilize a combination of geospatial data and filtering techniques. By storing the food truck locations in a PostgreSQL database with the PostGIS extension, we can perform spatial queries and calculate distances between points. This will enable us to efficiently retrieve the nearby food trucks based on the user's provided location.


## Usage
## Endpoints/API Documentation

### Search FoodTrucks

Description: Retrieve nearby food trucks based on provided location coordinates.

URL: /api/foodtruck

Method: GET

Query Parameters:

- `lat` (required): Latitude coordinate of the center point for the search (default: 0).
- `long` (required): Longitude coordinate of the center point for the search (default: 0).
- `searchRadius` (optional): Search radius in meters (default: 1000).
- `status` (optional): food truck status.
- `facilityType` (optional): food truck type.

Returns: JSON response containing count and data of nearby food trucks.
...

## 🗄️ Database

I am using PostgreSQL with PostGIS extension for handling location-based data in our project. PostgreSQL is a powerful open-source relational database management system, and PostGIS is an extension that adds support for geographic objects, allowing us to store and query spatial data efficiently.

By using PostgreSQL with PostGIS, we can store and manipulate location coordinates, perform spatial queries, and calculate distances between points. This enables us to implement features like finding nearby food trucks based on user-provided location coordinates.

If you are not familiar with PostgreSQL or PostGIS, you can refer to their official documentation for more information:

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [PostGIS Documentation](https://postgis.net/documentation/)

## 🧪 Testing

To test the Django project, run the following command:

    docker-compose run web python manage.py test

## 🚀 What I Would Like Improve

    Here are some ideas for improvements in our project:

    - Implement a feature to find food trucks based on the type of food they serve.
    - use more attributes of food truck to enhance the project more 
    - Enhance the project with more other features to make it more feature-rich.

## 📚 Learning

During this project, I had the opportunity to learn about PostGIS, which is an extension of PostgreSQL. PostGIS allows us to work with geographic objects and perform spatial operations. It has been a valuable addition to the project and has expanded my knowledge in working with location-based data.

