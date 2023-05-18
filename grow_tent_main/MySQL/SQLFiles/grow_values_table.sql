CREATE TABLE grow_values (
    id INT PRIMARY KEY AUTO_INCREMENT,
    temp_f DECIMAL(5, 2),
    temp_c DECIMAL(5, 2),
    humidity INT,
    water_amount DECIMAL(5, 2),
    light_on DECIMAL(5, 2),
    light_off DECIMAL(5, 2),
    program_time INT,
    timestamp DATETIME,
    plant_id INT,
    FOREIGN KEY(plant_id) REFERENCES plants(id)
);