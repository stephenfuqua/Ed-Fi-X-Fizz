CREATE TABLE lms.[User] (
    Identifier INT NOT NULL IDENTITY,
    SourceSystemIdentifier VARCHAR(50) NOT NULL,
    SourceSystem VARCHAR(50) NOT NULL,
    UserRole VARCHAR(50) NOT NULL,
    LocalUserIdentifier VARCHAR(50),
    SISUserIdentifier VARCHAR(50),
    [Name] VARCHAR(250),
    EmailAddress VARCHAR(320),
    EntityStatus VARCHAR(50),
    CreateDate DATETIME2 NOT NULL CONSTRAINT DF_User_CreateDate DEFAULT (getdate()),
    LastModifiedDate DATETIME2 NOT NULL CONSTRAINT DF_User_LastModifiedDate DEFAULT (getdate()),
    DeletedAt DATETIME2,
    CONSTRAINT PK_User PRIMARY KEY CLUSTERED (
        Identifier ASC
    ) WITH(
        PAD_INDEX = OFF,
        STATISTICS_NORECOMPUTE = OFF,
        IGNORE_DUP_KEY = OFF,
        ALLOW_ROW_LOCKS = ON,
        ALLOW_PAGE_LOCKS = ON
    ) ON [PRIMARY],
    CONSTRAINT UK_SourceSystem UNIQUE (
        SourceSystemIdentifier,
        SourceSystem
    )
) ON [PRIMARY];

CREATE TABLE lms.[stg_User] (
    StagingId INT NOT NULL IDENTITY,
    SourceSystemIdentifier VARCHAR(50) NOT NULL,
    SourceSystem VARCHAR(50) NOT NULL,
    UserRole VARCHAR(50) NOT NULL,
    LocalUserIdentifier VARCHAR(50),
    SISUserIdentifier VARCHAR(50),
    [Name] VARCHAR(250),
    EmailAddress VARCHAR(320),
    EntityStatus VARCHAR(50),
    CreateDate DATETIME2,
    LastModifiedDate DATETIME2,
    CONSTRAINT PK_stg_User PRIMARY KEY CLUSTERED (
        StagingId ASC
    ) WITH(
        PAD_INDEX = OFF,
        STATISTICS_NORECOMPUTE = OFF,
        IGNORE_DUP_KEY = OFF,
        ALLOW_ROW_LOCKS = ON,
        ALLOW_PAGE_LOCKS = ON
    ) ON [PRIMARY],
) ON [PRIMARY];

CREATE INDEX IX_stg_User_Natural_Key ON lms.[stg_user] (SourceSystemIdentifier, SourceSystem, LastModifiedDate);
