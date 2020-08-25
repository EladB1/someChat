CREATE TABLE Users (
  UserID SERIAL PRIMARY KEY,
  Username TEXT UNIQUE NOT NULL,
  Email TEXT UNIQUE NOT NULL,
  Password TEXT NOT NULL,
  status TEXT,
  profile_photo TEXT
);

CREATE INDEX indx_uname ON Users(Username);

CREATE TABLE messages (
  msgID SERIAL PRIMARY KEY,
  msg_content TEXT NOT NULL,
  time_sent timestamp NOT NULL,
  senderID INT NOT NULL,
  recipientID INT NOT NULL,
  CONSTRAINT fk_senderID FOREIGN KEY(senderID) REFERENCES Users(UserID) ON DELETE CASCADE,
  CONSTRAINT fk_recipientID FOREIGN KEY(recipientID) REFERENCES Users(UserID) ON DELETE CASCADE
);

CREATE INDEX indx_contents ON messages(msg_content);


CREATE TABLE rooms (
  roomID SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT
);

CREATE TABLE room_membership (
  roomID INT,
  UserID INT,
  memberID SERIAL PRIMARY KEY,
  CONSTRAINT fk_roomID FOREIGN KEY(roomID) REFERENCES rooms(roomID) ON DELETE CASCADE,
  CONSTRAINT fk_UserID FOREIGN KEY(UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

/*
Possible future use

CREATE TABLE roles (
  roleID SERIAL PRIMARY KEY,
  role_name TEXT NOT NULL
);

INSERT INTO roles(role_name) VALUES('admin');
INSERT INTO roles(role_name) VALUES('room_admin');
INSERT INTO roles(role_name) VALUES('user');

CREATE TABLE UserSettings (

);


CREATE TABLE settings (
  
);
*/
