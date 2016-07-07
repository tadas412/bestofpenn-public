/* users */
INSERT INTO users VALUES (1, 'hsust@seas.upenn.edu', 'pass', '0', 1, '0', '0');
INSERT INTO users VALUES (2, 'channat@seas.upenn.edu', 'pass', '10', 1, '0', '0');
INSERT INTO users VALUES (3, 'phamb@seas.upenn.edu', 'pass', '10', 1, '0', '0');
INSERT INTO users VALUES (4, 'smaiman@seas.upenn.edu', 'pass', '10', 1, '0', '0');
INSERT INTO users VALUES (5, 'tadas@seas.upenn.edu', 'pass', '10', 1, '0', '0');

/* lists */
INSERT INTO lists VALUES (1, 2, 'Best BYO', 'Restaurants where you can "bring your own" drinks- a Philly favorite!', 1);
INSERT INTO lists VALUES (2, 3, 'Best Brunch Spot', 'Boozy or not, everyone at Penn loves brunch!', '0');
INSERT INTO lists VALUES (3, 2, 'Best Food Trucks', 'Students love being able to grab food on the go for a low price.', '0');
INSERT INTO lists VALUES (4, 2, 'Best Coffee Shop', 'Caffeine is a must for most students', '0');

/* entities */
INSERT INTO entities VALUES (1, 1, 4, 'Hubbub', 'For the trendy ones', '4.2', '0');
INSERT INTO entities VALUES (2, 2, 4, 'Capogriro', '', '3.9', '0');
INSERT INTO entities VALUES (3, 4, 4, 'Saxbys', '', '3.92', '0');
INSERT INTO entities VALUES (4, 3, 4, 'Starbucks', '', '4.1', '0');
INSERT INTO entities VALUES (5, 1, 4, 'United By Blue', 'For the hipsters', '3.6', '0');

INSERT INTO entities VALUES (6, 1, 3, 'Margic Carpet', '', '4.6', '0');
INSERT INTO entities VALUES (7, 2, 3, 'Lyns', '', '4.4', '0');
INSERT INTO entities VALUES (8, 1, 3, 'Don Memos', 'The best burrito on campus', '4.5', '0');
INSERT INTO entities VALUES (9, 4, 3, 'Noras', '', '3.9', '0');
INSERT INTO entities VALUES (10, 5, 3, 'Kims Food Truck', '', '4.01', '0');

INSERT INTO entities VALUES (11, 5, 1, 'Izichuatl', 'Its a shit hole', '3.9', '0');
INSERT INTO entities VALUES (12, 2, 1, 'Banana Leaf', 'Great place to bring freshman for their first BYO', '3.9', '0');
INSERT INTO entities VALUES (13, 3, 1, 'La Viola', '', '3.9', '0');
INSERT INTO entities VALUES (14, 1, 1, 'Dim Sum Garden', 'Really good dim sum and it can get pretty rowdy', '3.9', '0');
INSERT INTO entities VALUES (15, 1, 1, 'Beijing', 'Kinda shitty chinese food but itll do for its close location on campus', '3.9', '0');

INSERT INTO entities VALUES (16, 1, 2, 'Tap House', 'Best bloody mary on campus', '3.9', '0');
INSERT INTO entities VALUES (17, 1, 2, 'Renatas Kitchen', '', '3.9', '0');
INSERT INTO entities VALUES (18, 1, 2, 'Farmacy Rx', '', '3.9', '0');
INSERT INTO entities VALUES (19, 3, 2, 'Sabrinas', '', '3.9', '0');
INSERT INTO entities VALUES (20, 4, 2, 'White Dog', 'Have your parents bring you here', '3.9', '0');

INSERT INTO ratings VALUES (1, 1, 4.4);
INSERT INTO ratings VALUES (2, 1, 4.4);
INSERT INTO ratings VALUES (3, 1, 4.4);
INSERT INTO ratings VALUES (4, 1, 4.5);
INSERT INTO ratings VALUES (2, 2, 3.4);
INSERT INTO ratings VALUES (2, 3, 4.2);
INSERT INTO ratings VALUES (1, 2, 4.4);
