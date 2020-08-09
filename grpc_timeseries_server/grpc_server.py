# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC meterusage. MeterUsage server."""

from concurrent import futures

import grpc
from google.protobuf.timestamp_pb2 import Timestamp

import meterusage_pb2
import meterusage_pb2_grpc
import timescale_helper

SERVER_ADDRESS = 'localhost:23333'
SERVER_ID = 1


class MeterUsage(meterusage_pb2_grpc.MeterUsageServicer):

    def GetAllRecords(self, request, context):
        print("grpc_server         | > Incoming request from client_id:(%d) ... The Message: %s" % (request.client_id, request.request_data))

        # Retreive the data using the timescale helper
        print("grpc_server         | > Timescale Helper Retrieving Data...")
        raw_data = timescale_helper.get_all_data()

        # Create a generator
        def response_messages():
            for record in raw_data:
                # Convert the datetime format into timestamp for transmission
                timestamp = Timestamp()
                timestamp.FromDatetime(record[0])
                response = meterusage_pb2.AllRecordsResponse(
                    time=timestamp,
                    meterusage=record[1])
                # print(response)
                yield response

        print("grpc_server         | > Transmission of data to client completed...")
        return response_messages()


def main():
    server = grpc.server(futures.ThreadPoolExecutor())
    meterusage_pb2_grpc.add_MeterUsageServicer_to_server(MeterUsage(), server)
    server.add_insecure_port(SERVER_ADDRESS)
    print("grpc_server         | > gRPC Server Online...")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    main()
