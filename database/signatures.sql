DROP TABLE IF EXISTS Signatures;
CREATE TABLE Signatures(
    [code] TEXT,
    [url] TEXT,
    [signature] TEXT,
    [epoch] FLOAT
);

DROP TABLE IF EXISTS Logs;
CREATE TABLE Logs(
    [moment] TEXT,
    [epoch] FLOAT,
    [data] TEXT,
    [isError] BIT
);

DROP TABLE IF EXISTS ConfiguredSignatures;
CREATE TABLE ConfiguredSignatures(
    [url] TEXT,
    [updateIntervalSeconds] FLOAT,
    [nextUpdateEpoch] FLOAT,
    [tags] TEXT
);
INSERT INTO ConfiguredSignatures VALUES ('https://listindiario.com/', 3600, 0, '[]');