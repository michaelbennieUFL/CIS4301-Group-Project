CREATE TABLE Accident (
    ID VARCHAR2(50) NOT NULL,
    Source VARCHAR2(255),
    Severity NUMBER(1)
        CONSTRAINT chk_Severity CHECK (Severity BETWEEN 1 AND 4) NOT NULL,
    DistanceAffected NUMBER(5,2) NOT NULL,
    --Description VARCHAR2(500), this is too much data we cant store it
    LocStartLatitude NUMBER(12,5)
        CONSTRAINT chk_LocStartLatitude CHECK (LocStartLatitude BETWEEN -180 AND 180),
    LocStartLongitude NUMBER(12,5)
        CONSTRAINT chk_LocStartLongitude CHECK (LocStartLongitude BETWEEN -180 AND 180),
    PRIMARY KEY (ID)
);


CREATE TABLE Time (
    StartTime TIMESTAMP NOT NULL,
    EndTime TIMESTAMP NOT NULL,
    AccidentID VARCHAR2(50) NOT NULL,
    TimeZone VARCHAR2(25),
    TimePeriod VARCHAR2(255),
    CONSTRAINT pk_Time PRIMARY KEY (StartTime, EndTime),
    CONSTRAINT fk_Time_Accident FOREIGN KEY (AccidentID) REFERENCES Accident(ID)
);


CREATE TABLE Weather (
    Temperature NUMBER(5,2)
        CONSTRAINT chk_Temperature CHECK (Temperature BETWEEN -90 AND 150),
    WindSpeed NUMBER(5,2) NOT NULL,
    WeatherCondition VARCHAR2(100),
    Visibility NUMBER(3,1)
        CONSTRAINT chk_Visibility CHECK (Visibility BETWEEN 0 AND 500),
    WindDirection VARCHAR2(10),
    Humidity NUMBER(5,2)
        CONSTRAINT chk_Humidity CHECK (Humidity BETWEEN 1 AND 100),
    Pressure NUMBER(5,2)
        CONSTRAINT chk_Pressure CHECK (Pressure BETWEEN 0 AND 80),
    WindChill NUMBER(5,2)
        CONSTRAINT chk_WindChill CHECK (WindChill BETWEEN -110 AND 110),
    Precipitation NUMBER(5,2)
        CONSTRAINT chk_Precipitation CHECK (Precipitation BETWEEN 0 AND 50),
    AccidentID VARCHAR2(50) NOT NULL,
    PRIMARY KEY (AccidentID)
);


CREATE TABLE RoadCondition (
    AccidentID VARCHAR2(50) NOT NULL,
    Bump NUMBER(1)
        CONSTRAINT chk_RoadCondition_Bump CHECK (Bump IN (0, 1)),
    Amenity NUMBER(1)
        CONSTRAINT chk_RoadCondition_Amenity CHECK (Amenity IN (0, 1)),
    NoExit NUMBER(1)
        CONSTRAINT chk_RoadCondition_NoExit CHECK (NoExit IN (0, 1)),
    TrafficSignal NUMBER(1)
        CONSTRAINT chk_RoadCondition_TrafficSignal CHECK (TrafficSignal IN (0, 1)),
    Railway NUMBER(1)
        CONSTRAINT chk_RoadCondition_Railway CHECK (Railway IN (0, 1)),
    TrafficCalming NUMBER(1)
        CONSTRAINT chk_RoadCondition_TrafficCalming CHECK (TrafficCalming IN (0, 1)),
    GiveWay NUMBER(1)
        CONSTRAINT chk_RoadCondition_GiveWay CHECK (GiveWay IN (0, 1)),
    TurningLoop NUMBER(1)
        CONSTRAINT chk_RoadCondition_TurningLoop CHECK (TurningLoop IN (0, 1)),
    Roundabout NUMBER(1)
        CONSTRAINT chk_RoadCondition_Roundabout CHECK (Roundabout IN (0, 1)),
    Crossing NUMBER(1)
        CONSTRAINT chk_RoadCondition_Crossing CHECK (Crossing IN (0, 1)),
    Station NUMBER(1)
        CONSTRAINT chk_RoadCondition_Station CHECK (Station IN (0, 1)),
    Stop NUMBER(1)
        CONSTRAINT chk_RoadCondition_Stop CHECK (Stop IN (0, 1)),
    Junction NUMBER(1)
        CONSTRAINT chk_RoadCondition_Junction CHECK (Junction IN (0, 1)),
    LocStartLatitude NUMBER(12,5)
        CONSTRAINT chk_RoadCondition_LocStartLatitude CHECK (LocStartLatitude BETWEEN -180 AND 180) NOT NULL,
    LocStartLongitude NUMBER(12,5)
        CONSTRAINT chk_RoadCondition_LocStartLongitude CHECK (LocStartLongitude BETWEEN -180 AND 180) NOT NULL,
    PRIMARY KEY (LocStartLatitude, LocStartLongitude),
    FOREIGN KEY (AccidentID) REFERENCES Accident(ID)
);



CREATE TABLE Location (
	AirportCode VARCHAR2(255),
	Street VARCHAR2(255),
	City VARCHAR2(255),
	Zipcode VARCHAR2(255),
	County VARCHAR2(255),
	State VARCHAR2(255),
	Country VARCHAR2(255),
	StartLatitude NUMBER(12,5)
	    CONSTRAINT chk_StartLatitude CHECK (StartLatitude BETWEEN -180 AND 180),
	EndLatitude NUMBER(12,5)
	    CONSTRAINT chk_EndLatitude CHECK (EndLatitude BETWEEN -180 AND 180),
	StartLongitude NUMBER(12,5)
	    CONSTRAINT chk_StartLongitude CHECK (StartLongitude BETWEEN -180 AND 180),
	EndLongitude NUMBER(12,5)
	    CONSTRAINT chk_EndLongitude CHECK (EndLongitude BETWEEN -180 AND 180),
	AirportICAOCode VARCHAR2(4),
	PRIMARY KEY (StartLatitude, StartLongitude, EndLatitude, EndLongitude)
);




-- allow other users to interacct with these tables


-- 對weather表的權限
GRANT SELECT, INSERT, UPDATE, DELETE ON WEATHER TO MICHAELBENNIE;
GRANT SELECT, INSERT, UPDATE, DELETE ON WEATHER TO "P.KEEFE";
GRANT SELECT, INSERT, UPDATE, DELETE ON WEATHER TO "LOGAN.FERNANDEZ";
GRANT SELECT, INSERT, UPDATE, DELETE ON WEATHER TO "H.ZENG";
GRANT SELECT, INSERT, UPDATE, DELETE ON WEATHER TO "JOSEPH.FLEMING";


-- 對accident表的權限

GRANT SELECT,INSERT,UPDATE,DELETE ON ACCIDENT TO MICHAELBENNIE;
GRANT SELECT,INSERT,UPDATE,DELETE ON ACCIDENT TO "P.KEEFE";
GRANT SELECT,INSERT,UPDATE,DELETE ON ACCIDENT TO "LOGAN.FERNANDEZ";
GRANT SELECT,INSERT,UPDATE,DELETE ON ACCIDENT TO "H.ZENG";
GRANT SELECT,INSERT,UPDATE,DELETE ON ACCIDENT TO "JOSEPH.FLEMING";


-- 對time表的權限
GRANT SELECT, INSERT, UPDATE, DELETE ON Time TO MICHAELBENNIE;
GRANT SELECT, INSERT, UPDATE, DELETE ON Time TO "P.KEEFE";
GRANT SELECT, INSERT, UPDATE, DELETE ON Time TO "LOGAN.FERNANDEZ";
GRANT SELECT, INSERT, UPDATE, DELETE ON Time TO "H.ZENG";
GRANT SELECT, INSERT, UPDATE, DELETE ON Time TO "JOSEPH.FLEMING";


-- 對RoadCondition表的權限
GRANT SELECT, INSERT, UPDATE, DELETE ON RoadCondition TO MICHAELBENNIE;
GRANT SELECT, INSERT, UPDATE, DELETE ON RoadCondition TO "P.KEEFE";
GRANT SELECT, INSERT, UPDATE, DELETE ON RoadCondition TO "LOGAN.FERNANDEZ";
GRANT SELECT, INSERT, UPDATE, DELETE ON RoadCondition TO "H.ZENG";
GRANT SELECT, INSERT, UPDATE, DELETE ON RoadCondition TO "JOSEPH.FLEMING";

-- 對location表的權限
GRANT SELECT, INSERT, UPDATE, DELETE ON Location TO MICHAELBENNIE;
GRANT SELECT, INSERT, UPDATE, DELETE ON Location TO "P.KEEFE";
GRANT SELECT, INSERT, UPDATE, DELETE ON Location TO "LOGAN.FERNANDEZ";
GRANT SELECT, INSERT, UPDATE, DELETE ON Location TO "H.ZENG";
GRANT SELECT, INSERT, UPDATE, DELETE ON Location TO "JOSEPH.FLEMING";


CREATE TABLE Airport (
    AirportID NUMBER GENERATED BY DEFAULT ON NULL AS IDENTITY,
    Name VARCHAR2(255),
    Latitude NUMBER(12,5)
        CONSTRAINT chk_Latitude CHECK (Latitude BETWEEN -180 AND 180),
    Longitude NUMBER(12,5)
        CONSTRAINT chk_Longitude CHECK (Longitude BETWEEN -180 AND 180),
    IATACode VARCHAR2(5) NOT NULL,
    ICAOCode VARCHAR2(4), -- 允许为空
    RegionCode VARCHAR2(50),
    CONSTRAINT pk_Airport PRIMARY KEY (AirportID)
);

-- 對airport表的權限
GRANT SELECT,INSERT,UPDATE,DELETE ON AIRPORT TO MICHAELBENNIE;
GRANT SELECT,INSERT,UPDATE,DELETE ON AIRPORT TO "P.KEEFE";
GRANT SELECT,INSERT,UPDATE,DELETE ON AIRPORT TO "LOGAN.FERNANDEZ";
GRANT SELECT,INSERT,UPDATE,DELETE ON AIRPORT TO "H.ZENG";
GRANT SELECT,INSERT,UPDATE,DELETE ON AIRPORT TO "JOSEPH.FLEMING";
