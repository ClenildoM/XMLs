import pyodbc

conexao = pyodbc.connect( 
            r"DRIVER={ODBC Driver 17 for SQL Server};"
            r"SERVER=10.100.2.2\eris;"
            r"DATABASE=ERIS_ESCARIZ;"
            r"UID=api_transferencia;"
            r"PWD=1q2w!Q@W;"
            r"Trusted_Connection=no;"
)