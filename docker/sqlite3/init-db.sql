CREATE TABLE test_1(
	id INTEGER PRIMARY KEY,
	test_a TEXT,
	test_b INTEGER
);

INSERT INTO test_1
	(id, test_a, test_b)
VALUES
	(1, 'something', 22),
	(2, 'something else', 30),
	(3, 'other things', 50);

CREATE TABLE test_2(
	id INTEGER PRIMARY KEY,
	test_c INTEGER,
	test_d TEXT
);

INSERT INTO test_2
	(id, test_c, test_d)
VALUES 
	(1, 22, 'something'),
	(2, 30, 'something else'),
	(3, 50, 'other things');
