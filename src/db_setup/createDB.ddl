CREATE TABLE users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(40) NOT NULL,
  passw TEXT NOT NULL,
  credit_total INTEGER DEFAULT 0,
  quality_weight DOUBLE DEFAULT 1.0,
  flag_count INTEGER DEFAULT 0,
  admin_val INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE lists (
  list_id INT AUTO_INCREMENT PRIMARY KEY,
  creator_id INT NOT NULL,
  list_name VARCHAR(40) NOT NULL,
  description VARCHAR(200),
  flag_count INTEGER DEFAULT 0,
  FOREIGN KEY (creator_id) REFERENCES users(user_id)
);

CREATE TABLE entities (
  entity_id INT AUTO_INCREMENT PRIMARY KEY,
  creator_id INT NOT NULL,
  list_id INT NOT NULL,
  entity_name VARCHAR(20) NOT NULL,
  entity_desc VARCHAR(200),
  avg_rating DOUBLE DEFAULT 0.0,
  flag_count INTEGER DEFAULT 0,
  FOREIGN KEY (creator_id) REFERENCES users(user_id),
  FOREIGN KEY (list_id) REFERENCES lists(list_id)
);

CREATE TABLE ratings (
  user_id INT NOT NULL,
  entity_id INT NOT NULL,
  rating INTEGER DEFAULT 3,
  PRIMARY KEY (user_id, entity_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (entity_id) REFERENCES entities(entity_id)
);

CREATE TABLE list_flags (
  user_id INT NOT NULL,
  list_id INT NOT NULL,
  PRIMARY KEY (user_id, list_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (list_id) REFERENCES lists(list_id)
);

CREATE TABLE entity_flags (
  user_id INT NOT NULL,
  entity_id INT NOT NULL,
  PRIMARY KEY (user_id, entity_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (entity_id) REFERENCES entities(entity_id)
);
