-- db
CREATE DATABASE test;
USE test;

-- create tables
CREATE TABLE IF NOT EXISTS test_1 (
    id INT PRIMARY KEY,
    test_a TEXT,
    test_b INTEGER
);

CREATE TABLE IF NOT EXISTS test_2 (
    id INT PRIMARY KEY,
    test_c INTEGER,
    test_d TEXT
);

-- inserts
INSERT INTO test_1 
    (id, test_a, test_b) 
VALUES 
    (1, 'stuff', 29),
    (2, 'things', 33),
    (3, 'others', 92);

INSERT INTO test_2 
    (id, test_c, test_d) 
VALUES 
    (1, 29, 'stuff'),
    (2, 33, 'things'),
    (3, 92, 'others');
