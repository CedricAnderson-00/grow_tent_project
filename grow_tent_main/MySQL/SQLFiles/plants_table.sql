CREATE TABLE plants (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    plant_name VARCHAR(255),
    exp_yield INT,
    blend VARCHAR(255),
    min_height INT,
    max_height INT,
    cbd_content VARCHAR(255),
    climate VARCHAR(255),
    medical_usage VARCHAR(255),
    genes VARCHAR(255),
    supplier VARCHAR(255),
    flowering_time_min INT,
    flowering_time_max INT,
    arrival_date DATE
);