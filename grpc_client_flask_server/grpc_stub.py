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
"""The Python implementation of the GRPC meterusage. MeterUsage client."""

import grpc

import meterusage_pb2
import meterusage_pb2_grpc

SERVER_ADDRESS = "localhost:23333"
CLIENT_ID = 1


def get_all_records(stub):
    request = meterusage_pb2.AllRecordsRequest( client_id=CLIENT_ID,
                                                request_data="Provide All Records Please")
    response = stub.GetAllRecords(request)
    print("> Server's Response ID: (%d) ... The Message: %s" % (response.server_id, response.response_data))


def main():
    with grpc.insecure_channel(SERVER_ADDRESS) as channel:
        stub = meterusage_pb2_grpc.MeterUsageStub(channel)
        get_all_records(stub)


if __name__ == '__main__':
    main()