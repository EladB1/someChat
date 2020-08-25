CREATE TABLE Users (
  UserID SERIAL PRIMARY KEY,
  Username TEXT UNIQUE NOT NULL,
  Email TEXT UNIQUE NOT NULL,
  Password TEXT NOT NULL,
  role TEXT NOT NULL,
  time_zone TEXT NOT NULL,
  status TEXT,
  profile_photo TEXT
);

CREATE INDEX indx_uname ON Users(Username);

/*CREATE TABLE UserSettings (

);


CREATE TABLE settings (
  
);*/

CREATE TABLE messages (
  msgID SERIAL PRIMARY KEY,
  msg_content TEXT NOT NULL,
  time_sent timestamp NOT NULL,
  recipient INT NOT NULL
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
