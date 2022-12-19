package main

import (
	"ethz.ch/netsec/isl/handout/defense/lib"
	"github.com/scionproto/scion/go/lib/slayers"
	spath "github.com/scionproto/scion/go/lib/slayers/path/scion"
	"fmt"
//	"strings"
	"time"
	"math/rand"
	"strconv"
)

const (
// Global constants
)

type Src_Data_Payload struct {
	Src_IA			string
	Raw_Src_Addr	string//[]byte
	//Src_Port		string//uint16
	payload			string//[]byte
}

type Src_IA_IP struct {
	Src_IA			string
	Raw_Src_Addr	string//[]byte
}

type rule8_struct struct {
	src_id			string
	timestamp		time.Time	
}

type rule10_struct struct {
	header_length_occurence			int
	header_length_as_ip_occurnece	int	
}


var (
// Here, you can define variables that keep state for your firewall

	current_time = time.Now()
	
	map_src_ip_address map[string]int = make(map[string]int)
	request_from_same_src_ip_limit = 20
	
	map_src_ip_n_port map[string]int = make(map[string]int)
	request_from_same_src_ip_n_port_limit = 15
	
	map_src_ia_n_ip map[string]int = make(map[string]int)
	request_from_same_ia_n_src_limit = 15
	
	rule0_as_map map[string]int = make(map[string]int)
	rule0_as_limit = 60
	rule0_ip_port_map map[string]int = make(map[string]int)
	rule0_ip_port_limit = 20
	
	
	time_limit_constant = "30000000ns"
	time_limit, _ = time.ParseDuration(time_limit_constant) //nanoseconds
	time_mapping map[string]rule8_struct = make(map[string]rule8_struct)
	
	
	string_prev_string = ""
	
	time_map_src_ip_n_port map[string]int = make(map[string]int)
	time_request_from_same_src_ip_n_port_limit = 5
	
	map_src_ia_n_ip_n_port map[string]int = make(map[string]int)
	request_from_same_src_ia_n_ip_n_port_limit = 15
	
	map_src_ip_payload map[string]int = make(map[string]int)
	request_from_same_src_ip_n_payload_limit = 1
	
	map_src_data_payload map[Src_Data_Payload]int = make(map[Src_Data_Payload]int)
	request_expiration = time.Second//		time.Duration
	//current_time = time.Now()//			time.Time
	
	
	rule_10_current_time = time.Now()
	rule_10_limit_constant = "57500000ns"
	rule_10_duration_limit, _ = time.ParseDuration(time_limit_constant) //nanoseconds
	rule_10_timestamp_map map[string]time.Time = make(map[string]time.Time)

	
	rule_10_limit_constant_pdate = "300000000ns"
	rule_10_duration_update_limit, _ = time.ParseDuration(rule_10_limit_constant_pdate) //nanoseconds
	
	rule_10_src_map map[string]int = make(map[string]int)
	rue_10_src_limit = 19
	
	rule_10_src_as_ip_headerlen_map map[string]int = make(map[string]int)
	rule_10_headerlen_map map[string]int = make(map[string]int)
	
	rule_10_as_map map[string]int = make(map[string]int)
	rule_10_as_limit = 10
	
	rule_10_as_ip_headerlen_limit = 3 //2 seems to be too restrictive enough
	rule_10_headerlen_limit = 11
	
	rule_10_headerlen_penalty_const = 1	
	
	rule_11_ip_map map[string]int = make(map[string]int)
	rule_11_flowid_map map[string]int = make(map[string]int)
	
	rule_12_src_time_map map[string]time.Time = make(map[string]time.Time)
	rule_12_src_limit = 20
	
	rule12_proc_duration = "400ms"
	rule_12_proc_duration_const, _ = time.ParseDuration(rule12_proc_duration) 
	
	rule_12_path_as_map map[string]string = make(map[string]string)
	rule_12_path_as_ip_adv map[string]bool = make(map[string]bool)
)





func init() {
	map_src_data_payload = make(map[Src_Data_Payload]int)
	//current_time = time.Now()
	// Perform any initial setup here
}

// This function receives all packets destined to the customer server.
//
// Your task is to decide whether to forward or drop a packet based on the
// headers and payload.
// References for the given packet types:
// - SCION header
//   https://pkg.go.dev/github.com/scionproto/scion/go/lib/slayers#SCION
// - UDP header
//   https://pkg.go.dev/github.com/scionproto/scion/go/lib/slayers#UDP
//

func print_meta_data(scion slayers.SCION, udp slayers.UDP, payload []byte) {
	fmt.Println(scion.Version)
	prettyPrintSCION(scion)
	prettyPrintUDP(udp)
	fmt.Println("Payload: ", payload)
//	fmt.Println(payload)
	fmt.Println("-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-")
}

/*

+--------------------------------------------------------------------------+
| SCION                                                                    |
+-------+----------------+-------------+---+------------+------------------+
| SrcIA | 17-ffaa:0:1117 | SrcAddrType | 0 | RawSrcAddr | [191 227 136 80] |
| DstIA | 17-ffaa:0:1119 | DstAddrType | 0 | RawDstAddr | [10 57 109 133]  |
+-------+----------------+-------------+---+------------+------------------+
+---------------+----------------------------------------------------+
| InfoFields[0] | {Peer: false, SegID: 45985, Timestamp: 1669762438} |
| HopFields[0]  | &{false false 63 4 3 [15 61 156 205 76 89]}        |
| HopFields[1]  | &{false false 63 1 2 [91 243 2 145 82 154]}        |
| HopFields[2]  | &{false false 63 1 0 [135 68 236 236 5 237]}       |
+---------------+----------------------------------------------------+
+------------------------------------+
| UDP                                |
+---------+-------+----------+-------+
| SrcPort | 34314 | DstPort  |   443 |
| Length  |    29 | Checksum | 21202 |
+---------+-------+----------+-------+

*/

//func rule1() bool {
//	cur_time := time.Now()
//	diff := cur_time.Sub(current_time)
//	current_time = cur_time
//	if diff > request_expiration {
//		return false
//	}
//	return true
//}
//
//func rule2(information Src_Data_Payload) bool {
//	counter, key_exists := map_src_data_payload[information]
//	if (!key_exists) || (key_exists && counter == 0) {
//		map_src_data_payload[information] = 1
//		return true //first time seeing packet from this src
//	}
//		
//	if key_exists && counter < request_from_same_src_limit {
//		map_src_data_payload[information] = counter + 1
//		return true //reject packet - already seen from 
//	}
//	
//	if key_exists && counter > request_from_same_src_limit {
//		map_src_data_payload[information] = counter + 1
//		return false //reject packet - already seen from 
//	}
//	
//	return true //default value	
//}



func rule1(src_ip_address string) bool {
	counter, key_exists := map_src_ip_address[src_ip_address]
	if (!key_exists) || (key_exists && counter == 0) {
		map_src_ip_address[src_ip_address] = 1
		return false //first time seeing packet from this src
		//return false//for def1, the first few packets are wrong -> try false
	}
		
	if key_exists && counter <= request_from_same_src_ip_limit {
		map_src_ip_address[src_ip_address] = counter + 1
		return true //accept ; it's under threshold
	}
		
	if key_exists && counter > request_from_same_src_ip_limit {
		map_src_ip_address[src_ip_address] = counter + 1
		return false //reject packet - already seen too  many times 
	}
		
	return true //default value		
}




func rule2(information string) bool {
	counter, key_exists := map_src_ip_n_port[information]
	if (!key_exists) || (key_exists && counter == 0) {
		map_src_ip_n_port[information] = 1
		return false //first time seeing packet from this src
	}
		
	if key_exists && counter <= request_from_same_src_ip_n_port_limit {
		map_src_ip_n_port[information] = counter + 1
		return true //accept ; it's under threshold
	}
		
	if key_exists && counter > request_from_same_src_ip_n_port_limit {
		map_src_ip_n_port[information] = counter + 1
		return false //reject packet - already seen too  many times 
	}
		
	return true //default value		
}


func rule3(information string) bool {
	counter, key_exists := map_src_ip_payload[information]
	if (!key_exists) || (key_exists && counter == 0) {
		map_src_ip_n_port[information] = 1
		return true //first time seeing packet from this src
	}
		
	if key_exists && counter < request_from_same_src_ip_n_payload_limit {
		map_src_ip_payload[information] = counter + 1
		return true //accept ; it's under threshold
	}
		
	if key_exists && counter >= request_from_same_src_ip_n_payload_limit {
		map_src_ip_payload[information] = counter + 1
		return false //reject packet - already seen too  many times 
	}
		
	return true //default value		
}

func rule4(information string) bool {
	counter, key_exists := map_src_ia_n_ip_n_port[information]
	if (!key_exists) || (key_exists && counter == 0) {
		map_src_ip_n_port[information] = 1
		return false //first time seeing packet from this src
		//see above
	}
		
	if key_exists && counter <= request_from_same_src_ia_n_ip_n_port_limit {
		map_src_ia_n_ip_n_port[information] = counter + 1
		return true //accept ; it's under threshold
	}
		
	if key_exists && counter > request_from_same_src_ia_n_ip_n_port_limit {
		map_src_ia_n_ip_n_port[information] = counter + 1
		return false //reject packet - already seen too  many times 
	}
		
	return true //default value		
}

func rule5(information string) bool {
	counter, key_exists := map_src_ia_n_ip[information]
	if (!key_exists) || (key_exists && counter == 0) {
		map_src_ip_n_port[information] = 1
		return false //first time seeing packet from this src
		//see above
	}
		
	if key_exists && counter <= request_from_same_ia_n_src_limit {
		map_src_ia_n_ip[information] = counter + 1
		return true //accept ; it's under threshold
	}
		
	if key_exists && counter > request_from_same_ia_n_src_limit {
		map_src_ia_n_ip[information] = counter + 1
		return false //reject packet - already seen too  many times 
	}
		
	return true //default value		
}


func rule6(time_difference time.Duration, information string) bool {
	
	//time_decision := time_difference >= time_limit
	if string_prev_string == "" {
		string_prev_string = information
		if time_difference < time_limit {
			return false
		}
		return true
	}
	
	if (time_difference < time_limit) && (string_prev_string != information) {
		string_prev_string = information
		return false
	}
	return true
}

func rule7(time_difference time.Duration, information string) bool {
	
	time_decision := time_difference >= time_limit
	threshold_decision := true
	
//	if time_difference < time_limit {
//		return false	
//	}
	
	counter, key_exists := time_map_src_ip_n_port[information]
	if (!key_exists) || (key_exists && counter == 0) {
		time_map_src_ip_n_port[information] = 1
		threshold_decision = false //first time seeing packet from this src
		//return false//for def1, the first few packets are wrong -> try false
		//matters for 3
	}
		
	if key_exists && counter <= time_request_from_same_src_ip_n_port_limit {
		time_map_src_ip_n_port[information] = counter + 1
		threshold_decision = true //accept ; it's under threshold
	}
		
	if key_exists && counter > time_request_from_same_src_ip_n_port_limit {
		time_map_src_ip_n_port[information] = counter + 1
		threshold_decision = false //reject packet - already seen too  many times 
	}
	
	return time_decision || threshold_decision
		
	//return true //default value	
}

func rule8(timestamp time.Time, src_id string) bool {
	struct_element, key_exists := time_mapping[src_id]
	new_struct := rule8_struct{src_id, timestamp}
	if !key_exists {
		time_mapping[src_id] = new_struct
		return false
	} 		
	time_interval := timestamp.Sub(struct_element.timestamp)
	time_mapping[src_id] = new_struct
	if time_interval < time_limit {
		return true	
	}
	return true
}


func rule0(as string, ip_port string) bool {
	counter_as, key_exists_as := rule0_as_map[as]
	counter_ip_port, key_exists_ip_port := rule0_ip_port_map[ip_port]
	
	if !key_exists_as && !key_exists_ip_port {
		rule0_as_map[as] = 1
		rule0_ip_port_map[ip_port] = 1
		return rand.Float32() < 0.5
	}
	
	if !key_exists_as && key_exists_ip_port {
		rule0_as_map[as] = 1
		rule0_ip_port_map[ip_port] = counter_ip_port + 1
		return rand.Float32() < 0.5
	}
	
	if key_exists_as && !key_exists_ip_port {
		rule0_as_map[as] = counter_as + 1
		rule0_ip_port_map[ip_port] = 1
		return rand.Float32() < 0.5
	}
	
	if counter_as > rule0_as_limit || counter_ip_port > rule0_ip_port_limit {
		return false
	}
	
	return true

}

func rule10(timestamp time.Time, as_ip string, headerlen string, port string, as string) bool {
	
	
	counter_hl, key_exists_hl := rule_10_headerlen_map[headerlen]
	if (!key_exists_hl) || (key_exists_hl && counter_hl == 0) {
		rule_10_headerlen_map[headerlen] = 1
	}
	

	as_ip_headerlen := as_ip + headerlen
	counter_asiphl, key_exists_asiphl := rule_10_src_as_ip_headerlen_map[as_ip_headerlen]
	
	//counter_hl, key_exists_hl := rule_10_headerlen_map[headerlen]
	
	if (!key_exists_asiphl) || (key_exists_asiphl && counter_asiphl == 0) {
		rule_10_src_as_ip_headerlen_map[as_ip_headerlen] = 1
	} else {
		rule_10_src_as_ip_headerlen_map[as_ip_headerlen] = counter_asiphl + 1
		if counter_asiphl >= 3 {
			rule_10_headerlen_map[headerlen] = counter_hl + 10
		}
	}
	
	counter_asiphl, key_exists_asiphl = rule_10_src_as_ip_headerlen_map[as_ip_headerlen]
	counter_hl, key_exists_hl = rule_10_headerlen_map[headerlen]
	
	if (counter_asiphl > 19 + 1) && counter_hl > 9 {
		return false
	}
		
	key := as_ip// + port
	counter, key_exists := rule_10_src_map[key]
	if (!key_exists) || (key_exists && counter == 0) {
		rule_10_src_map[key] = 1
		rule_10_timestamp_map[key] = timestamp
		return false //first time seeing packet from this src
		//return false//for def1, the first few packets are wrong -> try false
		//matters for 3
	}
	
	//deprecated
//	rule_10_src_map[key] = counter + 1
//	if time_interval > rule_10_duration_update_limit {
//		rule_10_src_map[key] = counter
//	}	
	
	rule_10_src_map[key] = counter + 1	
	src_threshold_bool := counter > 19
	
	if src_threshold_bool { //too many
		return false
	}
	
	prev_time_stamp, _ := rule_10_timestamp_map[key]
	rule_10_timestamp_map[key] = timestamp
	time_interval := timestamp.Sub(prev_time_stamp)
	time_threshold_bool := time_interval <= rule_10_duration_limit 
	
	if time_threshold_bool { //too quick
		return false
	}

	return true
	
	//return src_threshold_bool && time_threshold_bool
}


func rule11(as string, ip string, flowid string) bool {
	counter_ip, key_exists_ip := rule_11_ip_map[ip]
	if (!key_exists_ip) || (key_exists_ip && counter_ip == 0) {
		rule_11_ip_map[ip] = 0
	}
	
	counter_ip, key_exists_ip = rule_11_ip_map[ip]
	rule_11_ip_map[ip] = counter_ip + 1
	
	if len(rule_11_ip_map) > 10 {
		counter_flowid, key_exists_flowid := rule_11_flowid_map[flowid]
		if (!key_exists_flowid) || (key_exists_flowid && counter_flowid == 0) {
			rule_11_flowid_map[flowid] = 0
		}
		counter_flowid, key_exists_flowid = rule_11_flowid_map[flowid]
		rule_11_flowid_map[flowid] = counter_flowid + 1
		if counter_flowid > 2 {
			return false
		} 
	} else {
		if counter_ip > 20 {
			return false
		}	
	}
	return true	
}

func rule12(timestamp time.Time, pkt slayers.SCION) bool {

	ia := pkt.SrcIA.String()
	ip := string(pkt.RawSrcAddr[:])
	
	time_key := ia + ip
	
		
	fresh_timestamp := false
	prev_time, key_exists_time := rule_12_src_time_map[time_key]
	if (!key_exists_time) {
		rule_12_src_time_map[time_key] = timestamp
		fresh_timestamp = true //first time seeing packet from this src
	} else {
		rule_12_src_time_map[time_key] = timestamp
	}
		
	if !fresh_timestamp {
		time_interval := timestamp.Sub(prev_time)
		time_threshold_bool := time_interval <= rule_12_proc_duration_const 
		if time_threshold_bool {
			return false
		}
	}
	
	packet_path := ""//strconv.Itoa(int(pkt.HdrLen))
	
	raw := make([]byte, pkt.Path.Len())
	pkt.Path.SerializeTo(raw)
	path := &spath.Decoded{}
	path.DecodeFromBytes(raw)
	
//	// Print in table format
//	for i, info := range path.InfoFields {
//		t.AppendRow(table.Row{
//			fmt.Sprintf("InfoFields[%d]", i),
//			fmt.Sprintf("{Peer: %v, SegID: %d, Timestamp: %v}",
//				info.Peer, info.SegID, info.Timestamp),
//		})
//	}

	for _, info := range path.InfoFields {
		packet_path = packet_path + strconv.Itoa(int(info.SegID)) + "+"
	}
	
	
		
	mapped_as, key_exists_path_as := rule_12_path_as_map[packet_path]
	if (!key_exists_path_as) {
		rule_12_path_as_map[packet_path] = ia
		return true
	}
	
	if mapped_as != ia {
		rule_12_path_as_ip_adv[time_key] = true
		return false
	}
	rule_12_path_as_ip_adv[time_key] = false
		
	is_adv, key_exists_bool:= rule_12_path_as_ip_adv[time_key]
	if (!key_exists_bool) {
		rule_12_path_as_ip_adv[time_key] = false
		return true
	}
	
	if is_adv {
		return false
	}
		
	return true		
}



	
func filter(scion slayers.SCION, udp slayers.UDP, payload []byte) bool {
	// Print packet contents (disable this before submitting your code)
	//print_meta_data(scion, udp, payload)

	new_time := time.Now()
	
	return rule12(new_time, scion)
//	
//	decision12 := rule12(new_time, scion)
//	if decision12 {
//		return true
//	}
//		
//	decision1 := rule1(string(scion.RawSrcAddr[:]))
//	if decision1 {
//		return true
//	}
//	
//	decision2 := rule2(string(scion.RawSrcAddr[:]) + strconv.Itoa(int(udp.SrcPort)))
//	
//	return decision2
//	if decision2 {
//		return true
//	}
//	
//	return false
	
//	decision10 := rule10(new_time, scion.SrcIA.String() + string(scion.RawSrcAddr[:]), strconv.Itoa(int(scion.HdrLen)), strconv.Itoa(int(udp.SrcPort)), scion.SrcIA.String())
//	
//	decision11 := rule11(scion.SrcIA.String(), string(scion.RawSrcAddr[:]), strconv.Itoa(int(scion.FlowID))) 
//	
//	if decision11 {
//		return true
//	}
//	
//	return decision10

	
	//time_difference := new_time.Sub(current_time)
	//current_time = new_time
	
	
	
	
	//return rule11(scion.SrcIA.String(), string(scion.RawSrcAddr[:]), strconv.Itoa(int(scion.FlowID))) 
	
	//information := Src_Data_Payload{scion.SrcIA.String(), string(scion.RawSrcAddr[:]), /*strconv.Itoa(int(udp.SrcPort)),*/ string(payload[:])}
	
	//decision1 := rule1(scion.SrcIA.String() + string(scion.RawSrcAddr[:]))
	
	//decision2 := rule2(string(scion.RawSrcAddr[:]) + strconv.Itoa(int(udp.SrcPort)))
	
	//decision10 := rule10(new_time, scion.SrcIA.String() + string(scion.RawSrcAddr[:]))
	
	//decision10 := rule10(new_time, scion.SrcIA.String() + string(scion.RawSrcAddr[:]), strconv.Itoa(int(scion.HdrLen)), strconv.Itoa(int(udp.SrcPort)), scion.SrcIA.String())
//	
//	if decision1 {
//		return true
//	}
	
//	if decision2 {
//		return true
//	}
	
	//return decision10
	
//	if decision2 {
//		return true
//	}
	
//	if decision10 {
//		return true
//	}
//	
	
	
	
	
//	decision11 := rule11(scion.SrcIA.String(), string(scion.RawSrcAddr[:]), strconv.Itoa(int(scion.FlowID))) 
//	
//	if decision11 {
//		return true
//	}
//	
//	return decision10
	
	
	
	
//	
//	if decision10 {
//		return true
//	}
//	
//	if decision2 {
//		return true
//	}
//	
//	if decision1 {
//		return true
//	}
//	
//	return false
	
	//return rule11(scion.SrcIA.String(), string(scion.RawSrcAddr[:]), strconv.Itoa(int(scion.FlowID))) 
//	
//	return false
//	
	
	
	
	
//	if decision10 {
//		return true
//	}
	
//	if decision10 {
//		return true
//	}
	
//	if decision1 {
//		return true
//	}
		
//	return false
		
//	return false
	
//	decision2 := rule2(scion.SrcIA.String() + string(scion.RawSrcAddr[:]) + strconv.Itoa(int(udp.SrcPort)))
	
	//decision3 := rule3(string(scion.RawSrcAddr[:]) + string(payload[:]))
	
	//decision4 := rule4(scion.SrcIA.String() + string(scion.RawSrcAddr[:]) + strconv.Itoa(int(udp.SrcPort)))
	
	//decision5 := rule5(string(scion.RawSrcAddr[:]))
	
	
	
	//decision6 := rule6(time_difference, scion.SrcIA.String() + string(scion.RawSrcAddr[:]) + strconv.Itoa(int(udp.SrcPort)))
	
	//decision8 := rule8(new_time, string(scion.RawSrcAddr[:]))
	
//	if decision6 {
//		return true
//	}
	
	//decision0 := rule0(scion.SrcIA.String(), string(scion.RawSrcAddr[:]))
			

	
	//return decision8
//	if decision8 {
//		return true
//	}
//	
//	return true
	//return !(rand.Float32() < 0.95)
	
//	if decision0 {
//		return true
//	}
	
//	if decision8 {
//		return true
//	}
	
//	if decision2 {
//		return true	
//	}
//	return !(rand.Float32() < 0.99)
	//return false
		
//	if decision5 {
//		return true
//	}
	
//	if decision6 {
//		return true
//	}
	
//	if decision2 {
//		return true
//	}
//
//	if decision6 {
//		return true
//	}
	
	
	
//	return false
	
	//return !decision4

	
	//return decision2

	
	//return decision1 && decision2
	
//	dest_ia := scion.DstIA.String()
//	index := strings.Index(dest_ia, "-")
//	
////	i64, _ := strconv.ParseInt(slayers.AS(dest_ia), 10, 64)
//	
//	IP_string := dest_ia[:index] + string(scion.RawSrcAddr)
//
//
//	//if we receive the first packet of an IP and we did not detect that
//	//we are in def1 (yet) we drop the packet.
//	if MapASIP[IP_string] < 1 {
//		MapASIP[IP_string]++
//		if drop_first_packets{
//			return false
//		}
//	}else{
//		//we still update the number of packets from an IP
//		MapASIP[IP_string]++
//	}
//
//	if MapASIP[IP_string] > TreshholdIP {
//		drop_first_packets = false
//		return false
//	}
//	return true
	
	
	
	
//	prettyPrintSCION(scion)
//	prettyPrintUDP(udp)
	
	//check if payload already received once from src (nonce -> if yes reject)
	
	// Decision
	// | true  -> forward packet
	// | false -> drop packet
	//return true
}

func main() {
	// Start the firewall. Code after this line will not be executed
	//init()
	lib.RunFirewall(filter)
}
