--add constraints for time
ALTER TABLE MICHAELBENNIE.Time ADD CONSTRAINT pk_Time PRIMARY KEY (AccidentID);
ALTER TABLE MICHAELBENNIE.Time ADD CONSTRAINT fk_Time_Accident FOREIGN KEY (AccidentID) REFERENCES Accident(ID);

--add constraints for location
ALTER TABLE MICHAELBENNIE.LOCATION ADD CONSTRAINT pk_Location PRIMARY KEY (StartLatitude, StartLongitude);

--add constraints for RoadCondition
ALTER TABLE "H.ZENG".ROADCONDITION ADD CONSTRAINT pk_RoadCondition PRIMARY KEY (LocStartLatitude, LocStartLongitude);
CREATE INDEX idx_LocStartLatitude ON "H.ZENG".ROADCONDITION (LocStartLatitude);
CREATE INDEX idx_LocStartLongitude ON "H.ZENG".ROADCONDITION (LocStartLongitude);

--add constraint for Weather
ALTER TABLE "H.ZENG".WEATHER ADD CONSTRAINT pk_Weather PRIMARY KEY (AccidentID);
DELETE FROM "H.ZENG".Weather
WHERE Temperature < -90 OR Temperature > 150;
ALTER TABLE "H.ZENG".Weather ADD CONSTRAINT chk_Temperature CHECK (Temperature BETWEEN -90 AND 150);
DELETE FROM "H.ZENG".Weather
WHERE WindSpeed < 0 OR WindSpeed > 400;
ALTER TABLE "H.ZENG".Weather ADD CONSTRAINT chk_WindSpeed CHECK (WindSpeed BETWEEN 0 AND 400);
ALTER TABLE "H.ZENG".Weather ADD CONSTRAINT chk_Visibility CHECK (Visibility BETWEEN 0 AND 100);
ALTER TABLE "H.ZENG".Weather ADD CONSTRAINT chk_Humidity CHECK (Humidity BETWEEN 1 AND 100);
DELETE FROM "H.ZENG".Weather
WHERE Pressure < 20 OR Pressure > 50;
ALTER TABLE "H.ZENG".Weather ADD CONSTRAINT chk_Pressure CHECK (Pressure BETWEEN 20 AND 50);
DELETE FROM "H.ZENG".Weather
WHERE WindChill < -110 OR WindChill > 110;
ALTER TABLE "H.ZENG".Weather ADD CONSTRAINT chk_WindChill CHECK (WindChill BETWEEN -110 AND 110);
ALTER TABLE "H.ZENG".Weather ADD CONSTRAINT chk_Precipitation CHECK (Precipitation BETWEEN 0 AND 50);

--add constraints for US Cities
ALTER TABLE "P.KEEFE".USCITIES ADD CONSTRAINT chk_Latitude CHECK (Latitude BETWEEN -90 AND 90);
ALTER TABLE "P.KEEFE".USCITIES ADD CONSTRAINT chk_Longitude CHECK (Longitude BETWEEN -90 AND 90);
ALTER TABLE "P.KEEFE".USCITIES ADD CONSTRAINT pk_ID PRIMARY KEY (ID);

-- add foreign key constraint for US Cities
-- ALTER TABLE "P.KEEFE".USCITIES ADD CONSTRAINT fk_City FOREIGN KEY (City) REFERENCES MICHAELBENNIE.Location(City);

--Add Indices for faster lookup
CREATE INDEX idx_Accident_LocStartLatitude ON MICHAELBENNIE.ACCIDENT (LocStartLatitude);
CREATE INDEX idx_Accident_LocStartLongitude ON MICHAELBENNIE.ACCIDENT (LocStartLongitude);

-Wait! Me too!
CREATE INDEX idx_USCities_City ON "P.KEEFE".USCities (City);
CREATE INDEX idx_USCities_StateID ON "P.KEEFE".USCities (StateID);

