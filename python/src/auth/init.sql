DROP USER 'auth_user'@'localhost';

DROP DATABASE auth;

CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'auth_user_passwd';

CREATE DATABASE auth;

GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';

USE auth;

CREATE TABLE users (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    username varchar(255) NOT NULL,
    password varchar(255) NOT NULL
);

INSERT INTO users (username, password) VALUES ('dummy@email.com', 'dummy_email_passwd');