# Copyright [yyyy] [name of copyright owner]

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

import meterusage_pb2
import meterusage_pb2_grpc

SERVER_ADDRESS = 'localhost:23333'
SERVER_ID = 1


class MeterUsage(meterusage_pb2_grpc.MeterUsageServicer):

    def GetAllRecords(self, request, context):
        print("Incoming request from client_id:(%d) ... The Message: %s" % (request.client_id, request.request_data))
        response = meterusage_pb2.AllRecordsResponse(server_id=SERVER_ID,
                                                    response_data="THESE ARE ALL THE RECORDS")
        return response


def main():
    server = grpc.server(futures.ThreadPoolExecutor())
    meterusage_pb2_grpc.add_MeterUsageServicer_to_server(MeterUsage(), server)
    server.add_insecure_port(SERVER_ADDRESS)
    print("> gRPC Server Online...")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    main()
