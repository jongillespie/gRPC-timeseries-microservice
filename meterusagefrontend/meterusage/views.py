from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .grpc_stub_mod import grpc_stub, meterusage_pb2_grpc, meterusage_pb2
import grpc
import json

SERVER_ADDRESS = "localhost:23333"


def index(request):
    channel = grpc.insecure_channel(SERVER_ADDRESS)
    results = grpc_stub.get_all_records(channel)
    return JsonResponse(results)


