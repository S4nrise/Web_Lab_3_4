CREATE TABLE user (
	user_id INTEGER NOT NULL PRIMARY KEY,
	user_name TEXT NOT NULL,
	user_email TEXT NOT NULL,
	user_pass BLOB NOT NULL
);
CREATE INDEX user_id_IDX ON user (user_id);

CREATE TABLE todo (
	todo_id INTEGER NOT NULL PRIMARY KEY,
	todo_title TEXT NOT NULL,
	todo_description TEXT,
	todo_is_done INTEGER,
	todo_user_id INTEGER,
	CONSTRAINT todo_FK FOREIGN KEY (todo_user_id) REFERENCES "user"(user_id)
);
CREATE INDEX todo_id_IDX ON todo (todo_id);


