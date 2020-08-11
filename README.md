# gRPC-timeseries-microservice


Detailed development notes are captured in 'developer_notes' here: https://github.com/jongillespie/gRPC-timeseries-microservice/blob/master/developer_notes

## In Brief

This MVP was developed as a challenge provided by Spectral to test backend developemnt skills. The purpose of the contained - is to ingest raw CSV data consisting of time and meterusage metrics, store this data in a timeseries DB and expose it with a gRPC server. Additionally, this server can be queried for all of the data (timestamp : float) via a Django frontend that then displays it in JSON format in a simple UI.

The timescale_helper connects to the Timescale DB, creating the required hypertable (direct SQL inputs) and provides an abstracted cursor for single or multi execution calls. If the table already exists, the server catches and ignores. 

Data that is ingested from the CSV is first cleaned by clean_csv_data to ensure no NaN values exist, it is then populated in one go to the Timescale DB (postgres SQL) via SQLAlchemy.

The gRPC_server (gRPC comms implementation) is using unary-stream format, where the gRPC_stub (client) makes a single request and the gRPC_server returns all data via a stream of records (generator queued response messages).

Note, the time in the DB is stored in timestamp/datetime format which is then converted into google.protobuf.Timestamp format to maintain the required 'timeseries' transmission. This is then converted back into datetime and finally, str for easy consumption into JSON.

The front end was first developed using Flask but had countless issues, after many attempts with various methods (packages, reformatting code etc.) it forced a re-think of strategy. "grpc_client_flask_server" is thus NOT IN USE - however, was kept and committed as a record of the attempt.

Django was then selected and functions as intended, displaying the data in a JSONResponse UI. The Django project is in "meterusagefrontend".

* The proto file use is within 'protos' while the generated files were copied and exist in both the back and front end to simulate a seperation of concern (different repos in prod)
* A production frontend server was not implemented, instead the built in Django development server ws used for this challenge.
* .env was started for secure storage of keys/pass but not completed.

## Personal note:
Timescale, gRPC and Django were all brand new to me for this challenge - there are likely some anti-patterns that I'd very much appreciate some guidance on. Thanks!


