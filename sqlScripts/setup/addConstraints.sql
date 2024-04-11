--add constraints for time
ALTER TABLE MICHAELBENNIE.Time ADD CONSTRAINT pk_Time PRIMARY KEY (AccidentID);
ALTER TABLE MICHAELBENNIE.Time ADD CONSTRAINT fk_Time_Accident FOREIGN KEY (AccidentID) REFERENCES Accident(ID);

--add constraints for location
ALTER TABLE MICHAELBENNIE.LOCATION ADD CONSTRAINT pk_Location PRIMARY KEY (StartLatitude, StartLongitude);

--add constraints for RoadCondition
ALTER TABLE MICHAELBENNIE.ROADCONDITION ADD CONSTRAINT pk_RoadCondition PRIMARY KEY (LocStartLatitude, LocStartLongitude);


--add constraint for Weather
ALTER TABLE MICHAELBENNIE.WEATHER ADD CONSTRAINT pk_Weather PRIMARY KEY (AccidentID);


--Add Indices for faster lookup
CREATE unique INDEX idx_Time_AccidentID ON Time (AccidentID);
