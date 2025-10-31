CREATE DATABASE Pizzahut;


CREATE TABLE orders (
order_id INT NOT NULL,
order_date DATE NOT NULL,
ORDER_TIME TIME NOT NULL,
PRIMARY KEY (order_id)
);


CREATE TABLE orders_details (
order_details_id int not null,
order_id INT NOT NULL,
pizza_id text not null,
quntity int not null,
PRIMARY KEY (order_details_id)
);