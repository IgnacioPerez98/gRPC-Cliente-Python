import grpc
import usuarios_pb2 as pb2
import usuarios_pb2_grpc as pb2_grpc

def get_users_from_server():
    # Establish a secure gRPC channel to the server
    with grpc.secure_channel('www.redesdatos.duckdns.org:443', grpc.ssl_channel_credentials()) as channel:
        stub = pb2_grpc.UsersStub(channel)

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



get_users_from_server()

        
        



