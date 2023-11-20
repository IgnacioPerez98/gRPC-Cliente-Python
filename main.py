import grpc
import usuarios_pb2 as pb2
import usuarios_pb2_grpc as pb2_grpc
import requests
import time
import csv

def grpc_request(stub):
    # Create an empty request message (in this case, the GetUsers RPC doesn't require a request)
    request = pb2.Empty()

    try:
        # Call the GetUsers RPC method
        response = stub.GetUsers(request)

        # Process the response
        for user in response.users:
            print(f"User ID: {user.id}, Name: {user.name}, Curso: {user.curso}")

    except grpc.RpcError as e:
        print(f"Error calling GetUsers: {e}")

def http_request():
    try:
        response = requests.get('https://www.redesdatoshttp.duckdns.org/api/Usuarios/getusers')
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else", err)
    else:
        print("Successful Response:")
        print(response.text)  # or response.json() if response is in JSON format

def write_response_time_to_csv(method, response_time, filename='response_times.csv'):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([method, response_time])

with open('response_times.csv', mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['gRPC', 'HTTP'])

    with grpc.secure_channel('www.redesdatos.duckdns.org:443', grpc.ssl_channel_credentials()) as channel:
        stub = pb2_grpc.UsersStub(channel)
        for x in range(0,10000):
            # print("gRPC")
            start_time = time.time()
            grpc_request(stub)
            end_time = time.time()

            grpc_response_time = end_time - start_time
            # print(f"Response time: {grpc_response_time} seconds")

            # print("HTTP")
            start_time = time.time()
            http_request()
            end_time = time.time()

            http_response_time = end_time - start_time
            # print(f"Response time: {http_response_time} seconds")

            writer.writerow([grpc_response_time, http_response_time])
            print(x)
