/*
 * NOTE: the tables below have been modified from the output generated by
 * MetaEd: the primary key columns have been set to IDENTITY.
 */

-- Table [lms].[Assignment] --
CREATE TABLE [lms].[Assignment] (
    [AssignmentIdentifier] [INT] IDENTITY,
    [SourceSystemIdentifier] [NVARCHAR](255) NOT NULL,
    [SourceSystem] [NVARCHAR](255) NOT NULL,
    [LMSSectionIdentifier] [INT] NOT NULL,
    [Title] [NVARCHAR](255) NOT NULL,
    [AssignmentCategory] [NVARCHAR](60) NOT NULL,
    [AssignmentDescription] [NVARCHAR](1024) NULL,
    [StartDateTime] [DATETIME2](7) NULL,
    [EndDateTime] [DATETIME2](7) NULL,
    [DueDateTime] [DATETIME2](7) NULL,
    [MaxPoints] [INT] NULL,
    [SourceCreateDate] [DATETIME2](7) NULL,
    [SourceLastModifiedDate] [DATETIME2](7) NULL,
    [Discriminator] [NVARCHAR](128) NULL,
    [CreateDate] [DATETIME2] NOT NULL,
    [LastModifiedDate] [DATETIME2] NOT NULL,
    [Id] [UNIQUEIDENTIFIER] NOT NULL,
    CONSTRAINT [Assignment_PK] PRIMARY KEY CLUSTERED (
        [AssignmentIdentifier] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [lms].[Assignment] ADD CONSTRAINT [Assignment_DF_CreateDate] DEFAULT (getdate()) FOR [CreateDate]
GO
ALTER TABLE [lms].[Assignment] ADD CONSTRAINT [Assignment_DF_Id] DEFAULT (newid()) FOR [Id]
GO
ALTER TABLE [lms].[Assignment] ADD CONSTRAINT [Assignment_DF_LastModifiedDate] DEFAULT (getdate()) FOR [LastModifiedDate]
GO

-- Table [lms].[AssignmentSubmission] --
CREATE TABLE [lms].[AssignmentSubmission] (
    [LMSGradeIdentifier] [INT] IDENTITY,
    [SourceSystemIdentifier] [NVARCHAR](255) NOT NULL,
    [SourceSystem] [NVARCHAR](255) NOT NULL,
    [LMSUserIdentifier] [INT] NOT NULL,
    [AssignmentIdentifier] [INT] NOT NULL,
    [Status] [NVARCHAR](60) NOT NULL,
    [SubmissionDateTime] [DATETIME2](7) NOT NULL,
    [EarnedPoints] [INT] NULL,
    [Grade] [NVARCHAR](20) NULL,
    [SourceCreateDate] [DATETIME2](7) NULL,
    [SourceLastModifiedDate] [DATETIME2](7) NULL,
    [Discriminator] [NVARCHAR](128) NULL,
    [CreateDate] [DATETIME2] NOT NULL,
    [LastModifiedDate] [DATETIME2] NOT NULL,
    [Id] [UNIQUEIDENTIFIER] NOT NULL,
    CONSTRAINT [AssignmentSubmission_PK] PRIMARY KEY CLUSTERED (
        [LMSGradeIdentifier] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [lms].[AssignmentSubmission] ADD CONSTRAINT [AssignmentSubmission_DF_CreateDate] DEFAULT (getdate()) FOR [CreateDate]
GO
ALTER TABLE [lms].[AssignmentSubmission] ADD CONSTRAINT [AssignmentSubmission_DF_Id] DEFAULT (newid()) FOR [Id]
GO
ALTER TABLE [lms].[AssignmentSubmission] ADD CONSTRAINT [AssignmentSubmission_DF_LastModifiedDate] DEFAULT (getdate()) FOR [LastModifiedDate]
GO

-- Table [lms].[AssignmentSubmissionType] --
CREATE TABLE [lms].[AssignmentSubmissionType] (
    [AssignmentIdentifier] [INT] NOT NULL,
    [SubmissionType] [NVARCHAR](60) NOT NULL,
    [CreateDate] [DATETIME2] NOT NULL,
    CONSTRAINT [AssignmentSubmissionType_PK] PRIMARY KEY CLUSTERED (
        [AssignmentIdentifier] ASC,
        [SubmissionType] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [lms].[AssignmentSubmissionType] ADD CONSTRAINT [AssignmentSubmissionType_DF_CreateDate] DEFAULT (getdate()) FOR [CreateDate]
GO

-- Table [lms].[LMSGrade] --
CREATE TABLE [lms].[LMSGrade] (
    [LMSGradeIdentifier] [INT] IDENTITY,
    [SourceSystemIdentifier] [NVARCHAR](255) NOT NULL,
    [SourceSystem] [NVARCHAR](255) NOT NULL,
    [LMSUserIdentifier] [INT] NOT NULL,
    [LMSSectionIdentifier] [INT] NOT NULL,
    [LMSUserLMSSectionAssociationIdentifier] [INT] NOT NULL,
    [Grade] [NVARCHAR](20) NOT NULL,
    [GradeType] [NVARCHAR](60) NULL,
    [SourceCreateDate] [DATETIME2](7) NULL,
    [SourceLastModifiedDate] [DATETIME2](7) NULL,
    [Discriminator] [NVARCHAR](128) NULL,
    [CreateDate] [DATETIME2] NOT NULL,
    [LastModifiedDate] [DATETIME2] NOT NULL,
    [Id] [UNIQUEIDENTIFIER] NOT NULL,
    CONSTRAINT [LMSGrade_PK] PRIMARY KEY CLUSTERED (
        [LMSGradeIdentifier] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [lms].[LMSGrade] ADD CONSTRAINT [LMSGrade_DF_CreateDate] DEFAULT (getdate()) FOR [CreateDate]
GO
ALTER TABLE [lms].[LMSGrade] ADD CONSTRAINT [LMSGrade_DF_Id] DEFAULT (newid()) FOR [Id]
GO
ALTER TABLE [lms].[LMSGrade] ADD CONSTRAINT [LMSGrade_DF_LastModifiedDate] DEFAULT (getdate()) FOR [LastModifiedDate]
GO

-- Table [lms].[LMSSection] --
CREATE TABLE [lms].[LMSSection] (
    [LMSSectionIdentifier] [INT] IDENTITY,
    [SourceSystemIdentifier] [NVARCHAR](255) NOT NULL,
    [SourceSystem] [NVARCHAR](255) NOT NULL,
    [SISSectionIdentifier] [NVARCHAR](255) NULL,
    [Title] [NVARCHAR](255) NOT NULL,
    [SectionDescription] [NVARCHAR](1024) NULL,
    [Term] [NVARCHAR](60) NULL,
    [LMSSectionStatus] [NVARCHAR](60) NULL,
    [SourceCreateDate] [DATETIME2](7) NULL,
    [SourceLastModifiedDate] [DATETIME2](7) NULL,
    [Discriminator] [NVARCHAR](128) NULL,
    [CreateDate] [DATETIME2] NOT NULL,
    [LastModifiedDate] [DATETIME2] NOT NULL,
    [Id] [UNIQUEIDENTIFIER] NOT NULL,
    CONSTRAINT [LMSSection_PK] PRIMARY KEY CLUSTERED (
        [LMSSectionIdentifier] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [lms].[LMSSection] ADD CONSTRAINT [LMSSection_DF_CreateDate] DEFAULT (getdate()) FOR [CreateDate]
GO
ALTER TABLE [lms].[LMSSection] ADD CONSTRAINT [LMSSection_DF_Id] DEFAULT (newid()) FOR [Id]
GO
ALTER TABLE [lms].[LMSSection] ADD CONSTRAINT [LMSSection_DF_LastModifiedDate] DEFAULT (getdate()) FOR [LastModifiedDate]
GO

-- Table [lms].[LMSSectionActivity] --
CREATE TABLE [lms].[LMSSectionActivity] (
    [LMSSectionActivityIdentifier] [INT] IDENTITY,
    [SourceSystemIdentifier] [NVARCHAR](255) NOT NULL,
    [SourceSystem] [NVARCHAR](255) NOT NULL,
    [LMSUserIdentifier] [INT] NOT NULL,
    [LMSSectionIdentifier] [INT] NOT NULL,
    [ActivityType] [NVARCHAR](60) NOT NULL,
    [ActivityDateTime] [DATETIME2](7) NOT NULL,
    [ActivityStatus] [NVARCHAR](60) NOT NULL,
    [ParentSourceSystemIdentifier] [NVARCHAR](255) NULL,
    [ActivityTimeInMinutes] [INT] NULL,
    [SourceCreateDate] [DATETIME2](7) NULL,
    [SourceLastModifiedDate] [DATETIME2](7) NULL,
    [Discriminator] [NVARCHAR](128) NULL,
    [CreateDate] [DATETIME2] NOT NULL,
    [LastModifiedDate] [DATETIME2] NOT NULL,
    [Id] [UNIQUEIDENTIFIER] NOT NULL,
    CONSTRAINT [LMSSectionActivity_PK] PRIMARY KEY CLUSTERED (
        [LMSSectionActivityIdentifier] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [lms].[LMSSectionActivity] ADD CONSTRAINT [LMSSectionActivity_DF_CreateDate] DEFAULT (getdate()) FOR [CreateDate]
GO
ALTER TABLE [lms].[LMSSectionActivity] ADD CONSTRAINT [LMSSectionActivity_DF_Id] DEFAULT (newid()) FOR [Id]
GO
ALTER TABLE [lms].[LMSSectionActivity] ADD CONSTRAINT [LMSSectionActivity_DF_LastModifiedDate] DEFAULT (getdate()) FOR [LastModifiedDate]
GO

-- Table [lms].[LMSSystemActivity] --
CREATE TABLE [lms].[LMSSystemActivity] (
    [LMSSystemActivityIdentifier] [INT] IDENTITY,
    [SourceSystemIdentifier] [NVARCHAR](255) NOT NULL,
    [SourceSystem] [NVARCHAR](255) NOT NULL,
    [LMSUserIdentifier] [INT] NOT NULL,
    [ActivityType] [NVARCHAR](60) NOT NULL,
    [ActivityDateTime] [DATETIME2](7) NOT NULL,
    [ActivityStatus] [NVARCHAR](60) NOT NULL,
    [ParentSourceSystemIdentifier] [NVARCHAR](255) NULL,
    [ActivityTimeInMinutes] [INT] NULL,
    [SourceCreateDate] [DATETIME2](7) NULL,
    [SourceLastModifiedDate] [DATETIME2](7) NULL,
    [Discriminator] [NVARCHAR](128) NULL,
    [CreateDate] [DATETIME2] NOT NULL,
    [LastModifiedDate] [DATETIME2] NOT NULL,
    [Id] [UNIQUEIDENTIFIER] NOT NULL,
    CONSTRAINT [LMSSystemActivity_PK] PRIMARY KEY CLUSTERED (
        [LMSSystemActivityIdentifier] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [lms].[LMSSystemActivity] ADD CONSTRAINT [LMSSystemActivity_DF_CreateDate] DEFAULT (getdate()) FOR [CreateDate]
GO
ALTER TABLE [lms].[LMSSystemActivity] ADD CONSTRAINT [LMSSystemActivity_DF_Id] DEFAULT (newid()) FOR [Id]
GO
ALTER TABLE [lms].[LMSSystemActivity] ADD CONSTRAINT [LMSSystemActivity_DF_LastModifiedDate] DEFAULT (getdate()) FOR [LastModifiedDate]
GO

-- Table [lms].[LMSUser] --
CREATE TABLE [lms].[LMSUser] (
    [LMSUserIdentifier] [INT] IDENTITY,
    [SourceSystemIdentifier] [NVARCHAR](255) NOT NULL,
    [SourceSystem] [NVARCHAR](255) NOT NULL,
    [UserRole] [NVARCHAR](60) NOT NULL,
    [SISUserIdentifier] [NVARCHAR](255) NULL,
    [LocalUserIdentifier] [NVARCHAR](255) NULL,
    [Name] [NVARCHAR](255) NOT NULL,
    [EmailAddress] [NVARCHAR](255) NOT NULL,
    [SourceCreateDate] [DATETIME2](7) NULL,
    [SourceLastModifiedDate] [DATETIME2](7) NULL,
    [Discriminator] [NVARCHAR](128) NULL,
    [CreateDate] [DATETIME2] NOT NULL,
    [LastModifiedDate] [DATETIME2] NOT NULL,
    [Id] [UNIQUEIDENTIFIER] NOT NULL,
    CONSTRAINT [LMSUser_PK] PRIMARY KEY CLUSTERED (
        [LMSUserIdentifier] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [lms].[LMSUser] ADD CONSTRAINT [LMSUser_DF_CreateDate] DEFAULT (getdate()) FOR [CreateDate]
GO
ALTER TABLE [lms].[LMSUser] ADD CONSTRAINT [LMSUser_DF_Id] DEFAULT (newid()) FOR [Id]
GO
ALTER TABLE [lms].[LMSUser] ADD CONSTRAINT [LMSUser_DF_LastModifiedDate] DEFAULT (getdate()) FOR [LastModifiedDate]
GO

-- Table [lms].[LMSUserAttendanceEvent] --
CREATE TABLE [lms].[LMSUserAttendanceEvent] (
    [LMSUserAttendanceEventIdentifier] [INT] IDENTITY,
    [SourceSystemIdentifier] [NVARCHAR](255) NOT NULL,
    [SourceSystem] [NVARCHAR](255) NOT NULL,
    [LMSUserIdentifier] [INT] NOT NULL,
    [LMSSectionIdentifier] [INT] NULL,
    [LMSUserLMSSectionAssociationIdentifier] [INT] NULL,
    [EventDate] [DATE] NOT NULL,
    [Status] [NVARCHAR](60) NOT NULL,
    [SourceCreateDate] [DATETIME2](7) NULL,
    [SourceLastModifiedDate] [DATETIME2](7) NULL,
    [Discriminator] [NVARCHAR](128) NULL,
    [CreateDate] [DATETIME2] NOT NULL,
    [LastModifiedDate] [DATETIME2] NOT NULL,
    [Id] [UNIQUEIDENTIFIER] NOT NULL,
    CONSTRAINT [LMSUserAttendanceEvent_PK] PRIMARY KEY CLUSTERED (
        [LMSUserAttendanceEventIdentifier] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [lms].[LMSUserAttendanceEvent] ADD CONSTRAINT [LMSUserAttendanceEvent_DF_CreateDate] DEFAULT (getdate()) FOR [CreateDate]
GO
ALTER TABLE [lms].[LMSUserAttendanceEvent] ADD CONSTRAINT [LMSUserAttendanceEvent_DF_Id] DEFAULT (newid()) FOR [Id]
GO
ALTER TABLE [lms].[LMSUserAttendanceEvent] ADD CONSTRAINT [LMSUserAttendanceEvent_DF_LastModifiedDate] DEFAULT (getdate()) FOR [LastModifiedDate]
GO

-- Table [lms].[LMSUserLMSSectionAssociation] --
CREATE TABLE [lms].[LMSUserLMSSectionAssociation] (
    [LMSSectionIdentifier] [INT] NOT NULL,
    [LMSUserIdentifier] [INT] NOT NULL,
    [LMSUserLMSSectionAssociationIdentifier] [INT] IDENTITY,
    [SourceSystemIdentifier] [NVARCHAR](255) NOT NULL,
    [SourceSystem] [NVARCHAR](255) NOT NULL,
    [EnrollmentStatus] [NVARCHAR](60) NOT NULL,
    [StartDate] [DATE] NOT NULL,
    [EndDate] [DATE] NOT NULL,
    [SourceCreateDate] [DATETIME2](7) NULL,
    [SourceLastModifiedDate] [DATETIME2](7) NULL,
    [Discriminator] [NVARCHAR](128) NULL,
    [CreateDate] [DATETIME2] NOT NULL,
    [LastModifiedDate] [DATETIME2] NOT NULL,
    [Id] [UNIQUEIDENTIFIER] NOT NULL,
    CONSTRAINT [LMSUserLMSSectionAssociation_PK] PRIMARY KEY CLUSTERED (
        [LMSSectionIdentifier] ASC,
        [LMSUserIdentifier] ASC,
        [LMSUserLMSSectionAssociationIdentifier] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [lms].[LMSUserLMSSectionAssociation] ADD CONSTRAINT [LMSUserLMSSectionAssociation_DF_CreateDate] DEFAULT (getdate()) FOR [CreateDate]
GO
ALTER TABLE [lms].[LMSUserLMSSectionAssociation] ADD CONSTRAINT [LMSUserLMSSectionAssociation_DF_Id] DEFAULT (newid()) FOR [Id]
GO
ALTER TABLE [lms].[LMSUserLMSSectionAssociation] ADD CONSTRAINT [LMSUserLMSSectionAssociation_DF_LastModifiedDate] DEFAULT (getdate()) FOR [LastModifiedDate]
GO

