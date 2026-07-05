import pyodbc

conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=hfapi;UID=sa;PWD=Fashion@01;"
sql = """
-- Drop tables if they exist
IF OBJECT_ID('token_blacklist_blacklistedtoken', 'U') IS NOT NULL
    DROP TABLE token_blacklist_blacklistedtoken;
IF OBJECT_ID('token_blacklist_outstandingtoken', 'U') IS NOT NULL
    DROP TABLE token_blacklist_outstandingtoken;

-- Create outstandingtoken table with bigint columns
CREATE TABLE [token_blacklist_outstandingtoken] (
    [id] bigint IDENTITY(1,1) NOT NULL,
    [token] nvarchar(max) NOT NULL,
    [created_at] datetime2(7) NULL,
    [expires_at] datetime2(7) NOT NULL,
    [user_id] bigint NULL,
    [jti] nvarchar(255) NOT NULL,
    CONSTRAINT [token_blacklist_outstandingtoken_id_69982597_pk] PRIMARY KEY ([id]),
    CONSTRAINT [token_blacklist_outstandingtoken_jti_key] UNIQUE ([jti])
);

CREATE INDEX [token_blacklist_outstandingtoken_user_id_83bc629a] ON [token_blacklist_outstandingtoken] ([user_id]);
ALTER TABLE [token_blacklist_outstandingtoken] ADD CONSTRAINT [token_blacklist_outstandingtoken_user_id_fk_herofashion_user_id] FOREIGN KEY ([user_id]) REFERENCES [herofashion_user] ([id]);

-- Create blacklistedtoken table with bigint columns
CREATE TABLE [token_blacklist_blacklistedtoken] (
    [id] bigint IDENTITY(1,1) NOT NULL,
    [blacklisted_at] datetime2(7) NOT NULL,
    [token_id] bigint NOT NULL,
    CONSTRAINT [token_blacklist_blacklistedtoken_id_e1c86975_pk] PRIMARY KEY ([id]),
    CONSTRAINT [token_blacklist_blacklistedtoken_token_id_key] UNIQUE ([token_id])
);

CREATE INDEX [token_blacklist_blacklistedtoken_token_id_3cc7fe56] ON [token_blacklist_blacklistedtoken] ([token_id]);
ALTER TABLE [token_blacklist_blacklistedtoken] ADD CONSTRAINT [token_blacklist_blacklistedtoken_token_id_3cc7fe56_fk_token_blacklist_outstandingtoken_id] FOREIGN KEY ([token_id]) REFERENCES [token_blacklist_outstandingtoken] ([id]);
"""

try:
    print("Connecting to database...")
    conn = pyodbc.connect(conn_str)
    conn.autocommit = True
    cursor = conn.cursor()
    print("Executing table recreation...")
    cursor.execute(sql)
    print("SUCCESS! Tables created successfully.")
    conn.close()
except Exception as e:
    print(f"FAILED: {e}")
