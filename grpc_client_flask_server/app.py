# from flask import Flask, render_template, request
# import asyncio
# import datetime
# import json


import asyncio
from quart import Quart

async def abar(a):
    print(a)

app = Quart(__name__)

@app.route("/")
async def notify():
    await abar("abar")
    return "OK"

if __name__ == "__main__":
    app.run(debug=False)

# # NOTE Strange! grpc was the original and makes this work when running from CLI. 
# # However, Flask won't recognise grpc and when checking pip list its grcpio... what's going on...?
# import grpc

# import meterusage_pb2
# import meterusage_pb2_grpc

# SERVER_ADDRESS = "localhost:23333"
# CLIENT_ID = 1

# # def get_all_records(stub):
# def get_all_records():
#     # with grpc.insecure_channel(SERVER_ADDRESS) as channel:
#     stub = meterusage_pb2_grpc.MeterUsageStub(grpc.insecure_channel(SERVER_ADDRESS))

#     print("grpc_stub           | > Client's gRPC Stub requesting all MeterUsage Data...")
#     request = meterusage_pb2.AllRecordsRequest( client_id=CLIENT_ID,
#                                                 request_data="Provide All Records Please")
#     response_iterator = stub.GetAllRecords(request)
#     print("grpc_stub           | > First 10 records are:")
#     range = 10

#     # Prepare for JSON
#     meterusage_data = {}

#     for response in response_iterator:
#         # time = datetime.datetime.fromtimestamp(response.time)
#         time = str(response.time)

#         # Display first 10 records to console:
#         if range > 0:
#             print(str(time), str(response.meterusage))
#             range -= 1

#         meterusage_data.update( {time: response.meterusage} )

#     meterusage_json = json.dumps(meterusage_data)
#     print(meterusage_json)
#     return meterusage_json



# app = Flask(__name__)




# @app.route('/')
# def home():
#     return render_template('main.html')


# @app.route('/meterusage')#, methods=['GET'])
# def meterusage():
#     # if request.method == 'GET':
#     loop.run_until_complete(test("boom"))
#     # meterusage_json = get_all_records()
#     return render_template('meterusage.html')#, meterusage_data = meterusage_json)


# # @app.errorhandler(500)
# # def internal_error(error):
# #     return render_template('errors/500.html'), 500


# # @app.errorhandler(404)
# # def not_found_error(error):
# #     return render_template('errors/404.html'), 404


# if __name__ == '__main__':
#     app.run(debug=True)



# from gevent import monkey
# monkey.patch_all()
# from flask import Flask
# from gevent import wsgi

# app = Flask(__name__)

# @app.route('/')
# def index():
#   return 'Hello World'

# server = wsgi.WSGIServer(('127.0.0.1', 5000), app)
# server.serve_forever()
