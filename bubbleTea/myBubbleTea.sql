DROP DATABASE IF EXISTS myBubbleTea;
CREATE DATABASE IF NOT EXISTS myBubbleTea;
USE myBubbleTea;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


-------- USER ---------

CREATE TABLE user (
  id int(11) NOT NULL AUTO_INCREMENT,
  name varchar(79) NOT NULL,
  firstname varchar(79) NOT NULL,
  email varchar(79) NOT NULL,
  password varchar(128) NOT NULL,
  picture varchar(1000),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATE,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO user (id, name, firstname, email, password, picture, created_at, updated_at) VALUES
(1, 'Monster', 'Yeti', 'monster@yahoo.fr', '1234', NULL, '2024-04-15', NULL);




-------- ADMIN ---------

CREATE TABLE admin (
  id int(11) NOT NULL AUTO_INCREMENT,
  pseudo varchar(79) NOT NULL,
  email varchar(79) NOT NULL,
  password varchar(128) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATE,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO admin (id, pseudo, email, password, created_at, updated_at) VALUES
(1, 'Gladys', 'gladys@yahoo.fr', '1234', '2024-04-18', NULL);
(2, 'snd', 'snd@yahoo.fr', '1234', '2024-04-18', NULL);






-------- PRODUCT ---------

CREATE TABLE product (
  id int(11) NOT NULL AUTO_INCREMENT,
  identifier varchar(79) NOT NULL,
  description varchar(125) NOT NULL,
  price int(11) NOT NULL,
  picture varchar(1000) NOT NULL,
  stock int(11) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATE,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO product (id, identifier, description, price, picture, stock, created_at, updated_at) VALUES
(1, 'Matcha', 'Sublime parfum thé vert matcha.', 7, '/matcha.jpg', 200, '2024-04-15', NULL),
(2, 'Pinky', 'Sublime parfum thé noir.', 7, '/pinky.jpg', 200, '2024-04-15', NULL),
(3, 'Whity', 'Sublime parfum thé blanc.', 8, '/whity.jpg', 200, '2024-04-15', NULL);



-------- VARIETY ---------

CREATE TABLE variety (
  id int(11) NOT NULL AUTO_INCREMENT,
  bubble varchar(79) NOT NULL,
  description varchar(125) NOT NULL,
  sugar varchar(79) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATE,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO variety (id, bubble, description, sugar, created_at, updated_at) VALUES
(1, 'Tapioca', 'Billes de Tapioca.', 1, '2024-04-15', NULL),
(2, 'Tapioca', 'Billes de Tapioca.', 2, '2024-04-15', NULL),
(3, 'Tapioca', 'Billes de Tapioca.', 3, '2024-04-15', NULL),
(4, 'Mangue', 'Billes de Mangues.', 1, '2024-04-15', NULL),
(5, 'Mangue', 'Billes de Mangues.', 2, '2024-04-15', NULL),
(6, 'Mangue', 'Billes de Mangues.', 3, '2024-04-15', NULL);



-------- CART ---------

CREATE TABLE cart (
  id int(11) NOT NULL AUTO_INCREMENT,
  user_id int(11) NOT NULL,
  variety_id int(11) NOT NULL,
  quantity int(11) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATE,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id) REFERENCES user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO cart (id, user_id, variety_id, quantity, created_at, updated_at) VALUES
(1, 1, 1, 1, '2024-04-15', NULL);



-------- COMMAND ---------

CREATE TABLE command (
  id int(11) NOT NULL AUTO_INCREMENT,
  cart_id int(11) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATE,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO command (id, cart_id, created_at, updated_at) VALUES
(1, 1, '2024-04-15', NULL),
(2, 2, '2024-04-15', NULL);



-------- JONCTION - USER_PRODUCT ---------

CREATE TABLE user_product (
  user_id int(11) NOT NULL,
  product_id int(11) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (product_id) REFERENCES product(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO user_product (user_id, product_id) VALUES
(1, 3);



-------- JONCTION - VARIETY_PRODUCT ---------

CREATE TABLE variety_product (
  variety_id int(11) NOT NULL,
  product_id int(11) NOT NULL,
  FOREIGN KEY (variety_id) REFERENCES variety(id),
  FOREIGN KEY (product_id) REFERENCES product(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO variety_product (variety_id, product_id) VALUES
(4, 1);



-------- JONCTION - PRODUCT_CART ---------

CREATE TABLE product_cart (
  cart_id int(11) NOT NULL,  
  product_id int(11) NOT NULL,
  FOREIGN KEY (cart_id) REFERENCES cart(id),
  FOREIGN KEY (product_id) REFERENCES product(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO product_cart (cart_id, product_id) VALUES
(1, 2);