import sys
from client import get_data_nodes, find_file

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python main.py <ip adress> <port> <-g || -f>")
        sys.exit(1)

    ip_address = sys.argv[1]
    port = int(sys.argv[2])
    command = sys.argv[3]

    if command == "-g":
        get_data_nodes(ip_address, port)
    elif command == "-f":
        if len(sys.argv) < 5:
            print("Usage: python main.py <ip adress> <port> -f <file name>")
            sys.exit(1)
        file_name = sys.argv[4]
        find_file(ip_address, file_name)
    else:
        print("Comando no reconocido")
