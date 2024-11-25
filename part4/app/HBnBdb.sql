-- Database of hbnb
CREATE DATABASE IF NOT EXISTS HBnB;

USE HBnB;

CREATE TABLE User (
    id CHAR(36) PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    password VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE Place (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36),
    FOREIGN KEY (owner_id) REFERENCES User(id)
);

CREATE TABLE Amenity (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);

CREATE TABLE Review (
    id CHAR(36) PRIMARY KEY,
    text TEXT,
    rating INT,
    user_id CHAR(36),
    place_id CHAR(36),
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (place_id) REFERENCES Place(id),
    CONSTRAINT unique_review_for_place UNIQUE (user_id, place_id),
    CHECK (rating BETWEEN 1 AND 5)
);

CREATE TABLE Place_Amenity (
    place_id CHAR(36),               
    amenity_id CHAR(36),
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES Place(id),  
    FOREIGN KEY (amenity_id) REFERENCES Amenity(id)
);

INSERT INTO User (
    id,
    email,
    first_name,
    last_name,
    password,
    is_admin
)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'admin@hbnb.io',
    'Admin',
    'HBnB',
    '$2a$12$zWIDRqyRhjv4F8dsdmjFSu8w6qGflC9ZYpzIVbTnptta9Xc5LT.Ma',
    TRUE
);

INSERT INTO Amenity (id, name)
VALUES
    ('ea9bb6c7-5b20-4453-8f0b-77932aa70172', 'WiFi'),
    ('4798fff3-4a98-4420-a66c-0d08c5f67f5d', 'Swimming Pool'),
    ('00793c75-cffb-4282-a381-0cbc7a201ff9', 'Air Conditioning');
