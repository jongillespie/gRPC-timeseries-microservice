# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC meterusage. MeterUsage client."""

import datetime
import json

from google.protobuf.timestamp_pb2 import Timestamp
import grpc

from . import meterusage_pb2
from . import meterusage_pb2_grpc

SERVER_ADDRESS = "localhost:23333"
CLIENT_ID = 1


def get_all_records(channel):
    stub = meterusage_pb2_grpc.MeterUsageStub(channel)
    
    print("grpc_stub           | > Client's gRPC Stub requesting all MeterUsage Data...")
    request = meterusage_pb2.AllRecordsRequest( client_id=CLIENT_ID,
                                                request_data="Provide All Records Please")
    response_iterator = stub.GetAllRecords(request)
    
    # Display first 10 records to console: (*for CLI stub testing.)
    # print("grpc_stub           | > First 10 records are:")
    # range = 10

    # Prepare for JSON
    meterusage_data = {}

    for response in response_iterator:
        # Convert the timestamp back into Datetime
        time_raw = Timestamp.ToDatetime(response.time)
        # Convert datetime into String for JSON display
        time = str(time_raw)
        # Display first 10 records to console: (*for CLI stub testing.)
        # if range > 0:
        #     print(str(time), str(response.meterusage))
        #     range -= 1
        meterusage_data.update( {time: response.meterusage} )

    return meterusage_data


# NOTE Below kept as reference for solo stub testing. DevNotes explains the change.
# def main():
#     with grpc.insecure_channel(SERVER_ADDRESS) as channel:
#         stub = meterusage_pb2_grpc.MeterUsageStub(channel)
#         get_all_records(stub)


# if __name__ == '__main__':
#     main()
