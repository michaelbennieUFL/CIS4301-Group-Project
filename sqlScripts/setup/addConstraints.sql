--add constraints for time
ALTER TABLE MICHAELBENNIE.Time ADD CONSTRAINT pk_Time PRIMARY KEY (AccidentID);
ALTER TABLE MICHAELBENNIE.Time ADD CONSTRAINT fk_Time_Accident FOREIGN KEY (AccidentID) REFERENCES Accident(ID);

--add constraints for location
ALTER TABLE MICHAELBENNIE.LOCATION ADD CONSTRAINT pk_Location PRIMARY KEY (StartLatitude, StartLongitude);
