// Code generated by protoc-gen-go. DO NOT EDIT.
// source: synse.proto

/*
Package synse is a generated protocol buffer package.

It is generated from these files:
	synse.proto

It has these top-level messages:
	ReadRequest
	WriteRequest
	MetainfoRequest
	TransactionId
	ReadResponse
	MetainfoResponse
	WriteResponse
	MetaOutputUnit
	MetaOutputRange
	MetaOutput
	MetaLocation
*/
package synse

import proto "github.com/golang/protobuf/proto"
import fmt "fmt"
import math "math"

import (
	context "golang.org/x/net/context"
	grpc "google.golang.org/grpc"
)

// Reference imports to suppress errors if they are not otherwise used.
var _ = proto.Marshal
var _ = fmt.Errorf
var _ = math.Inf

// This is a compile-time assertion to ensure that this generated file
// is compatible with the proto package it is being compiled against.
// A compilation error at this line likely means your copy of the
// proto package needs to be updated.
const _ = proto.ProtoPackageIsVersion2 // please upgrade the proto package

type ReadingType int32

const (
	ReadingType_UNKNOWN               ReadingType = 0
	ReadingType_TEMPERATURE           ReadingType = 1
	ReadingType_DIFFERENTIAL_PRESSURE ReadingType = 2
	ReadingType_AIRFLOW               ReadingType = 3
	ReadingType_HUMIDITY              ReadingType = 4
	ReadingType_LED_STATE             ReadingType = 5
	ReadingType_LED_BLINK             ReadingType = 6
)

var ReadingType_name = map[int32]string{
	0: "UNKNOWN",
	1: "TEMPERATURE",
	2: "DIFFERENTIAL_PRESSURE",
	3: "AIRFLOW",
	4: "HUMIDITY",
	5: "LED_STATE",
	6: "LED_BLINK",
}
var ReadingType_value = map[string]int32{
	"UNKNOWN":               0,
	"TEMPERATURE":           1,
	"DIFFERENTIAL_PRESSURE": 2,
	"AIRFLOW":               3,
	"HUMIDITY":              4,
	"LED_STATE":             5,
	"LED_BLINK":             6,
}

func (x ReadingType) String() string {
	return proto.EnumName(ReadingType_name, int32(x))
}
func (ReadingType) EnumDescriptor() ([]byte, []int) { return fileDescriptor0, []int{0} }

type WriteResponse_WriteStatus int32

const (
	WriteResponse_UNKNOWN WriteResponse_WriteStatus = 0
	WriteResponse_PENDING WriteResponse_WriteStatus = 1
	WriteResponse_WRITING WriteResponse_WriteStatus = 2
	WriteResponse_DONE    WriteResponse_WriteStatus = 3
)

var WriteResponse_WriteStatus_name = map[int32]string{
	0: "UNKNOWN",
	1: "PENDING",
	2: "WRITING",
	3: "DONE",
}
var WriteResponse_WriteStatus_value = map[string]int32{
	"UNKNOWN": 0,
	"PENDING": 1,
	"WRITING": 2,
	"DONE":    3,
}

func (x WriteResponse_WriteStatus) String() string {
	return proto.EnumName(WriteResponse_WriteStatus_name, int32(x))
}
func (WriteResponse_WriteStatus) EnumDescriptor() ([]byte, []int) { return fileDescriptor0, []int{6, 0} }

type WriteResponse_WriteState int32

const (
	WriteResponse_OK    WriteResponse_WriteState = 0
	WriteResponse_ERROR WriteResponse_WriteState = 1
)

var WriteResponse_WriteState_name = map[int32]string{
	0: "OK",
	1: "ERROR",
}
var WriteResponse_WriteState_value = map[string]int32{
	"OK":    0,
	"ERROR": 1,
}

func (x WriteResponse_WriteState) String() string {
	return proto.EnumName(WriteResponse_WriteState_name, int32(x))
}
func (WriteResponse_WriteState) EnumDescriptor() ([]byte, []int) { return fileDescriptor0, []int{6, 1} }

// Read
// ~~~~
// the read request message contains the uuid of the device that
// we desire to read. the uuid of the device should be generated
// by the owning background process and should be returned to the
// synse application in the MetainfoResponse, which Synse will
// cache and use as a lookup table for routing requests.
type ReadRequest struct {
	Uid string `protobuf:"bytes,1,opt,name=uid" json:"uid,omitempty"`
}

func (m *ReadRequest) Reset()                    { *m = ReadRequest{} }
func (m *ReadRequest) String() string            { return proto.CompactTextString(m) }
func (*ReadRequest) ProtoMessage()               {}
func (*ReadRequest) Descriptor() ([]byte, []int) { return fileDescriptor0, []int{0} }

func (m *ReadRequest) GetUid() string {
	if m != nil {
		return m.Uid
	}
	return ""
}

// Write
// ~~~~~
// the write request message contains the uuid of the device that
// we desire to write to, as well as a repeated string (e.g. a
// list of strings in Python) which makes up the data that we
// which to write to that device.
type WriteRequest struct {
	Uid string `protobuf:"bytes,1,opt,name=uid" json:"uid,omitempty"`
	// TODO: should this be string or bytes?
	Data []string `protobuf:"bytes,2,rep,name=data" json:"data,omitempty"`
}

func (m *WriteRequest) Reset()                    { *m = WriteRequest{} }
func (m *WriteRequest) String() string            { return proto.CompactTextString(m) }
func (*WriteRequest) ProtoMessage()               {}
func (*WriteRequest) Descriptor() ([]byte, []int) { return fileDescriptor0, []int{1} }

func (m *WriteRequest) GetUid() string {
	if m != nil {
		return m.Uid
	}
	return ""
}

func (m *WriteRequest) GetData() []string {
	if m != nil {
		return m.Data
	}
	return nil
}

// Metainfo
// ~~~~~~~~
// the metainfo request message contains a field for rack and board,
// but neither are required. if specified, the response will contain
// only information relating to the rack/board filter applied. if
// they are left unspecified, the response will contain the entirety
// of the metainfo scan information.
type MetainfoRequest struct {
	Rack  string `protobuf:"bytes,1,opt,name=rack" json:"rack,omitempty"`
	Board string `protobuf:"bytes,2,opt,name=board" json:"board,omitempty"`
}

func (m *MetainfoRequest) Reset()                    { *m = MetainfoRequest{} }
func (m *MetainfoRequest) String() string            { return proto.CompactTextString(m) }
func (*MetainfoRequest) ProtoMessage()               {}
func (*MetainfoRequest) Descriptor() ([]byte, []int) { return fileDescriptor0, []int{2} }

func (m *MetainfoRequest) GetRack() string {
	if m != nil {
		return m.Rack
	}
	return ""
}

func (m *MetainfoRequest) GetBoard() string {
	if m != nil {
		return m.Board
	}
	return ""
}

// TransactionCheck
// ~~~~~~~~~~~~~~~~
// the transaction id gives identity to a single 'write' action. since
// device writes are handled asynchronously, the background process
// returns the transaction id when a write is registered, which the
// caller can later pass back to `TransactionCheck` to get the status
// of that write.
type TransactionId struct {
	Id string `protobuf:"bytes,1,opt,name=id" json:"id,omitempty"`
}

func (m *TransactionId) Reset()                    { *m = TransactionId{} }
func (m *TransactionId) String() string            { return proto.CompactTextString(m) }
func (*TransactionId) ProtoMessage()               {}
func (*TransactionId) Descriptor() ([]byte, []int) { return fileDescriptor0, []int{3} }

func (m *TransactionId) GetId() string {
	if m != nil {
		return m.Id
	}
	return ""
}

// Read
// ~~~~
// the read response provides the timestamp at which the reading was
// taken, the type of the reading (e.g. temperature, humidity, led
// state, etc.), and the value of that reading. read responses are
// returned to the client as a stream, so a single device can return
// multiple readings. (e.g. a humidity sensor can return a %humidity
// reading and a temperature reading).
type ReadResponse struct {
	Timestamp string      `protobuf:"bytes,1,opt,name=timestamp" json:"timestamp,omitempty"`
	Type      ReadingType `protobuf:"varint,2,opt,name=type,enum=synse.ReadingType" json:"type,omitempty"`
	Value     string      `protobuf:"bytes,3,opt,name=value" json:"value,omitempty"`
}

func (m *ReadResponse) Reset()                    { *m = ReadResponse{} }
func (m *ReadResponse) String() string            { return proto.CompactTextString(m) }
func (*ReadResponse) ProtoMessage()               {}
func (*ReadResponse) Descriptor() ([]byte, []int) { return fileDescriptor0, []int{4} }

func (m *ReadResponse) GetTimestamp() string {
	if m != nil {
		return m.Timestamp
	}
	return ""
}

func (m *ReadResponse) GetType() ReadingType {
	if m != nil {
		return m.Type
	}
	return ReadingType_UNKNOWN
}

func (m *ReadResponse) GetValue() string {
	if m != nil {
		return m.Value
	}
	return ""
}

// Metainfo
// ~~~~~~~~
// the metainfo response represents a single device that is owned by
// the process. metainfo responses are returned to the client as a stream
// so a background process can support any number of devices. the response
// itself contains a timestamp for when the response was generated, an
// for the device, and all other meta-information we have pertaining to
// that device. the caller, Synse, will cache this information and use it
// to route requests to the appropriate device as well as provide responses
// for scan and info requests.
type MetainfoResponse struct {
	Timestamp    string        `protobuf:"bytes,1,opt,name=timestamp" json:"timestamp,omitempty"`
	Uid          string        `protobuf:"bytes,2,opt,name=uid" json:"uid,omitempty"`
	Type         string        `protobuf:"bytes,3,opt,name=type" json:"type,omitempty"`
	Model        string        `protobuf:"bytes,4,opt,name=model" json:"model,omitempty"`
	Manufacturer string        `protobuf:"bytes,5,opt,name=manufacturer" json:"manufacturer,omitempty"`
	Protocol     string        `protobuf:"bytes,6,opt,name=protocol" json:"protocol,omitempty"`
	Info         string        `protobuf:"bytes,7,opt,name=info" json:"info,omitempty"`
	Comment      string        `protobuf:"bytes,8,opt,name=comment" json:"comment,omitempty"`
	Location     *MetaLocation `protobuf:"bytes,9,opt,name=location" json:"location,omitempty"`
	Output       []*MetaOutput `protobuf:"bytes,10,rep,name=output" json:"output,omitempty"`
}

func (m *MetainfoResponse) Reset()                    { *m = MetainfoResponse{} }
func (m *MetainfoResponse) String() string            { return proto.CompactTextString(m) }
func (*MetainfoResponse) ProtoMessage()               {}
func (*MetainfoResponse) Descriptor() ([]byte, []int) { return fileDescriptor0, []int{5} }

func (m *MetainfoResponse) GetTimestamp() string {
	if m != nil {
		return m.Timestamp
	}
	return ""
}

func (m *MetainfoResponse) GetUid() string {
	if m != nil {
		return m.Uid
	}
	return ""
}

func (m *MetainfoResponse) GetType() string {
	if m != nil {
		return m.Type
	}
	return ""
}

func (m *MetainfoResponse) GetModel() string {
	if m != nil {
		return m.Model
	}
	return ""
}

func (m *MetainfoResponse) GetManufacturer() string {
	if m != nil {
		return m.Manufacturer
	}
	return ""
}

func (m *MetainfoResponse) GetProtocol() string {
	if m != nil {
		return m.Protocol
	}
	return ""
}

func (m *MetainfoResponse) GetInfo() string {
	if m != nil {
		return m.Info
	}
	return ""
}

func (m *MetainfoResponse) GetComment() string {
	if m != nil {
		return m.Comment
	}
	return ""
}

func (m *MetainfoResponse) GetLocation() *MetaLocation {
	if m != nil {
		return m.Location
	}
	return nil
}

func (m *MetainfoResponse) GetOutput() []*MetaOutput {
	if m != nil {
		return m.Output
	}
	return nil
}

// TransactionCheck
// ~~~~~~~~~~~~~~~~
// the response for a transaction check command gives the status of the
// transaction. transactions correspond to write requests. since writes
// are performed asynchronously, the transaction id is used to track the
// progress of that transaction.
type WriteResponse struct {
	Timestamp string                    `protobuf:"bytes,1,opt,name=timestamp" json:"timestamp,omitempty"`
	Status    WriteResponse_WriteStatus `protobuf:"varint,2,opt,name=status,enum=synse.WriteResponse_WriteStatus" json:"status,omitempty"`
	State     WriteResponse_WriteState  `protobuf:"varint,3,opt,name=state,enum=synse.WriteResponse_WriteState" json:"state,omitempty"`
}

func (m *WriteResponse) Reset()                    { *m = WriteResponse{} }
func (m *WriteResponse) String() string            { return proto.CompactTextString(m) }
func (*WriteResponse) ProtoMessage()               {}
func (*WriteResponse) Descriptor() ([]byte, []int) { return fileDescriptor0, []int{6} }

func (m *WriteResponse) GetTimestamp() string {
	if m != nil {
		return m.Timestamp
	}
	return ""
}

func (m *WriteResponse) GetStatus() WriteResponse_WriteStatus {
	if m != nil {
		return m.Status
	}
	return WriteResponse_UNKNOWN
}

func (m *WriteResponse) GetState() WriteResponse_WriteState {
	if m != nil {
		return m.State
	}
	return WriteResponse_OK
}

type MetaOutputUnit struct {
	Name   string `protobuf:"bytes,1,opt,name=name" json:"name,omitempty"`
	Symbol string `protobuf:"bytes,2,opt,name=symbol" json:"symbol,omitempty"`
}

func (m *MetaOutputUnit) Reset()                    { *m = MetaOutputUnit{} }
func (m *MetaOutputUnit) String() string            { return proto.CompactTextString(m) }
func (*MetaOutputUnit) ProtoMessage()               {}
func (*MetaOutputUnit) Descriptor() ([]byte, []int) { return fileDescriptor0, []int{7} }

func (m *MetaOutputUnit) GetName() string {
	if m != nil {
		return m.Name
	}
	return ""
}

func (m *MetaOutputUnit) GetSymbol() string {
	if m != nil {
		return m.Symbol
	}
	return ""
}

type MetaOutputRange struct {
	Min int32 `protobuf:"varint,1,opt,name=min" json:"min,omitempty"`
	Max int32 `protobuf:"varint,2,opt,name=max" json:"max,omitempty"`
}

func (m *MetaOutputRange) Reset()                    { *m = MetaOutputRange{} }
func (m *MetaOutputRange) String() string            { return proto.CompactTextString(m) }
func (*MetaOutputRange) ProtoMessage()               {}
func (*MetaOutputRange) Descriptor() ([]byte, []int) { return fileDescriptor0, []int{8} }

func (m *MetaOutputRange) GetMin() int32 {
	if m != nil {
		return m.Min
	}
	return 0
}

func (m *MetaOutputRange) GetMax() int32 {
	if m != nil {
		return m.Max
	}
	return 0
}

type MetaOutput struct {
	Type      string           `protobuf:"bytes,1,opt,name=type" json:"type,omitempty"`
	Precision int32            `protobuf:"varint,2,opt,name=precision" json:"precision,omitempty"`
	Unit      *MetaOutputUnit  `protobuf:"bytes,3,opt,name=unit" json:"unit,omitempty"`
	Range     *MetaOutputRange `protobuf:"bytes,4,opt,name=range" json:"range,omitempty"`
}

func (m *MetaOutput) Reset()                    { *m = MetaOutput{} }
func (m *MetaOutput) String() string            { return proto.CompactTextString(m) }
func (*MetaOutput) ProtoMessage()               {}
func (*MetaOutput) Descriptor() ([]byte, []int) { return fileDescriptor0, []int{9} }

func (m *MetaOutput) GetType() string {
	if m != nil {
		return m.Type
	}
	return ""
}

func (m *MetaOutput) GetPrecision() int32 {
	if m != nil {
		return m.Precision
	}
	return 0
}

func (m *MetaOutput) GetUnit() *MetaOutputUnit {
	if m != nil {
		return m.Unit
	}
	return nil
}

func (m *MetaOutput) GetRange() *MetaOutputRange {
	if m != nil {
		return m.Range
	}
	return nil
}

type MetaLocation struct {
	Rack   string `protobuf:"bytes,1,opt,name=rack" json:"rack,omitempty"`
	Board  string `protobuf:"bytes,2,opt,name=board" json:"board,omitempty"`
	Device string `protobuf:"bytes,3,opt,name=device" json:"device,omitempty"`
}

func (m *MetaLocation) Reset()                    { *m = MetaLocation{} }
func (m *MetaLocation) String() string            { return proto.CompactTextString(m) }
func (*MetaLocation) ProtoMessage()               {}
func (*MetaLocation) Descriptor() ([]byte, []int) { return fileDescriptor0, []int{10} }

func (m *MetaLocation) GetRack() string {
	if m != nil {
		return m.Rack
	}
	return ""
}

func (m *MetaLocation) GetBoard() string {
	if m != nil {
		return m.Board
	}
	return ""
}

func (m *MetaLocation) GetDevice() string {
	if m != nil {
		return m.Device
	}
	return ""
}

func init() {
	proto.RegisterType((*ReadRequest)(nil), "synse.ReadRequest")
	proto.RegisterType((*WriteRequest)(nil), "synse.WriteRequest")
	proto.RegisterType((*MetainfoRequest)(nil), "synse.MetainfoRequest")
	proto.RegisterType((*TransactionId)(nil), "synse.TransactionId")
	proto.RegisterType((*ReadResponse)(nil), "synse.ReadResponse")
	proto.RegisterType((*MetainfoResponse)(nil), "synse.MetainfoResponse")
	proto.RegisterType((*WriteResponse)(nil), "synse.WriteResponse")
	proto.RegisterType((*MetaOutputUnit)(nil), "synse.MetaOutputUnit")
	proto.RegisterType((*MetaOutputRange)(nil), "synse.MetaOutputRange")
	proto.RegisterType((*MetaOutput)(nil), "synse.MetaOutput")
	proto.RegisterType((*MetaLocation)(nil), "synse.MetaLocation")
	proto.RegisterEnum("synse.ReadingType", ReadingType_name, ReadingType_value)
	proto.RegisterEnum("synse.WriteResponse_WriteStatus", WriteResponse_WriteStatus_name, WriteResponse_WriteStatus_value)
	proto.RegisterEnum("synse.WriteResponse_WriteState", WriteResponse_WriteState_name, WriteResponse_WriteState_value)
}

// Reference imports to suppress errors if they are not otherwise used.
var _ context.Context
var _ grpc.ClientConn

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
const _ = grpc.SupportPackageIsVersion4

// Client API for InternalApi service

type InternalApiClient interface {
	// Read from the specified device(s).
	Read(ctx context.Context, in *ReadRequest, opts ...grpc.CallOption) (InternalApi_ReadClient, error)
	// Write to the specified device(s).
	Write(ctx context.Context, in *WriteRequest, opts ...grpc.CallOption) (*TransactionId, error)
	// Get the metainformation from the background process that describes
	// all of the available devices which that process owns
	Metainfo(ctx context.Context, in *MetainfoRequest, opts ...grpc.CallOption) (InternalApi_MetainfoClient, error)
	// Check on the state of a write transaction.
	TransactionCheck(ctx context.Context, in *TransactionId, opts ...grpc.CallOption) (*WriteResponse, error)
}

type internalApiClient struct {
	cc *grpc.ClientConn
}

func NewInternalApiClient(cc *grpc.ClientConn) InternalApiClient {
	return &internalApiClient{cc}
}

func (c *internalApiClient) Read(ctx context.Context, in *ReadRequest, opts ...grpc.CallOption) (InternalApi_ReadClient, error) {
	stream, err := grpc.NewClientStream(ctx, &_InternalApi_serviceDesc.Streams[0], c.cc, "/synse.InternalApi/Read", opts...)
	if err != nil {
		return nil, err
	}
	x := &internalApiReadClient{stream}
	if err := x.ClientStream.SendMsg(in); err != nil {
		return nil, err
	}
	if err := x.ClientStream.CloseSend(); err != nil {
		return nil, err
	}
	return x, nil
}

type InternalApi_ReadClient interface {
	Recv() (*ReadResponse, error)
	grpc.ClientStream
}

type internalApiReadClient struct {
	grpc.ClientStream
}

func (x *internalApiReadClient) Recv() (*ReadResponse, error) {
	m := new(ReadResponse)
	if err := x.ClientStream.RecvMsg(m); err != nil {
		return nil, err
	}
	return m, nil
}

func (c *internalApiClient) Write(ctx context.Context, in *WriteRequest, opts ...grpc.CallOption) (*TransactionId, error) {
	out := new(TransactionId)
	err := grpc.Invoke(ctx, "/synse.InternalApi/Write", in, out, c.cc, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *internalApiClient) Metainfo(ctx context.Context, in *MetainfoRequest, opts ...grpc.CallOption) (InternalApi_MetainfoClient, error) {
	stream, err := grpc.NewClientStream(ctx, &_InternalApi_serviceDesc.Streams[1], c.cc, "/synse.InternalApi/Metainfo", opts...)
	if err != nil {
		return nil, err
	}
	x := &internalApiMetainfoClient{stream}
	if err := x.ClientStream.SendMsg(in); err != nil {
		return nil, err
	}
	if err := x.ClientStream.CloseSend(); err != nil {
		return nil, err
	}
	return x, nil
}

type InternalApi_MetainfoClient interface {
	Recv() (*MetainfoResponse, error)
	grpc.ClientStream
}

type internalApiMetainfoClient struct {
	grpc.ClientStream
}

func (x *internalApiMetainfoClient) Recv() (*MetainfoResponse, error) {
	m := new(MetainfoResponse)
	if err := x.ClientStream.RecvMsg(m); err != nil {
		return nil, err
	}
	return m, nil
}

func (c *internalApiClient) TransactionCheck(ctx context.Context, in *TransactionId, opts ...grpc.CallOption) (*WriteResponse, error) {
	out := new(WriteResponse)
	err := grpc.Invoke(ctx, "/synse.InternalApi/TransactionCheck", in, out, c.cc, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// Server API for InternalApi service

type InternalApiServer interface {
	// Read from the specified device(s).
	Read(*ReadRequest, InternalApi_ReadServer) error
	// Write to the specified device(s).
	Write(context.Context, *WriteRequest) (*TransactionId, error)
	// Get the metainformation from the background process that describes
	// all of the available devices which that process owns
	Metainfo(*MetainfoRequest, InternalApi_MetainfoServer) error
	// Check on the state of a write transaction.
	TransactionCheck(context.Context, *TransactionId) (*WriteResponse, error)
}

func RegisterInternalApiServer(s *grpc.Server, srv InternalApiServer) {
	s.RegisterService(&_InternalApi_serviceDesc, srv)
}

func _InternalApi_Read_Handler(srv interface{}, stream grpc.ServerStream) error {
	m := new(ReadRequest)
	if err := stream.RecvMsg(m); err != nil {
		return err
	}
	return srv.(InternalApiServer).Read(m, &internalApiReadServer{stream})
}

type InternalApi_ReadServer interface {
	Send(*ReadResponse) error
	grpc.ServerStream
}

type internalApiReadServer struct {
	grpc.ServerStream
}

func (x *internalApiReadServer) Send(m *ReadResponse) error {
	return x.ServerStream.SendMsg(m)
}

func _InternalApi_Write_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(WriteRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(InternalApiServer).Write(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/synse.InternalApi/Write",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(InternalApiServer).Write(ctx, req.(*WriteRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _InternalApi_Metainfo_Handler(srv interface{}, stream grpc.ServerStream) error {
	m := new(MetainfoRequest)
	if err := stream.RecvMsg(m); err != nil {
		return err
	}
	return srv.(InternalApiServer).Metainfo(m, &internalApiMetainfoServer{stream})
}

type InternalApi_MetainfoServer interface {
	Send(*MetainfoResponse) error
	grpc.ServerStream
}

type internalApiMetainfoServer struct {
	grpc.ServerStream
}

func (x *internalApiMetainfoServer) Send(m *MetainfoResponse) error {
	return x.ServerStream.SendMsg(m)
}

func _InternalApi_TransactionCheck_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(TransactionId)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(InternalApiServer).TransactionCheck(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/synse.InternalApi/TransactionCheck",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(InternalApiServer).TransactionCheck(ctx, req.(*TransactionId))
	}
	return interceptor(ctx, in, info, handler)
}

var _InternalApi_serviceDesc = grpc.ServiceDesc{
	ServiceName: "synse.InternalApi",
	HandlerType: (*InternalApiServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "Write",
			Handler:    _InternalApi_Write_Handler,
		},
		{
			MethodName: "TransactionCheck",
			Handler:    _InternalApi_TransactionCheck_Handler,
		},
	},
	Streams: []grpc.StreamDesc{
		{
			StreamName:    "Read",
			Handler:       _InternalApi_Read_Handler,
			ServerStreams: true,
		},
		{
			StreamName:    "Metainfo",
			Handler:       _InternalApi_Metainfo_Handler,
			ServerStreams: true,
		},
	},
	Metadata: "synse.proto",
}

func init() { proto.RegisterFile("synse.proto", fileDescriptor0) }

var fileDescriptor0 = []byte{
	// 785 bytes of a gzipped FileDescriptorProto
	0x1f, 0x8b, 0x08, 0x00, 0x00, 0x09, 0x6e, 0x88, 0x02, 0xff, 0x8c, 0x54, 0xdd, 0x6e, 0xe3, 0x44,
	0x14, 0x8e, 0x9d, 0x38, 0x4d, 0x8e, 0xd3, 0xae, 0x39, 0xdd, 0x5d, 0x4c, 0xb5, 0x52, 0xa3, 0xb9,
	0x40, 0x5d, 0x84, 0x16, 0x94, 0xdd, 0x95, 0x90, 0x40, 0x40, 0x20, 0x2e, 0x58, 0x4d, 0x93, 0x6a,
	0xea, 0xaa, 0xe2, 0x6a, 0x35, 0x8d, 0x67, 0x17, 0x43, 0xfc, 0x83, 0x3d, 0x5e, 0xb5, 0x57, 0x3c,
	0x06, 0x6f, 0xc2, 0xcb, 0x71, 0x01, 0x9a, 0x9f, 0x24, 0xb6, 0x0a, 0xa8, 0x77, 0xe7, 0x3b, 0xff,
	0xf3, 0xcd, 0x39, 0x07, 0xdc, 0xea, 0x2e, 0xab, 0xf8, 0x8b, 0xa2, 0xcc, 0x45, 0x8e, 0x8e, 0x02,
	0xe4, 0x18, 0x5c, 0xca, 0x59, 0x4c, 0xf9, 0x6f, 0x35, 0xaf, 0x04, 0x7a, 0xd0, 0xad, 0x93, 0xd8,
	0xb7, 0xc6, 0xd6, 0xc9, 0x90, 0x4a, 0x91, 0xbc, 0x82, 0xd1, 0x75, 0x99, 0x08, 0xfe, 0x9f, 0x1e,
	0x88, 0xd0, 0x8b, 0x99, 0x60, 0xbe, 0x3d, 0xee, 0x9e, 0x0c, 0xa9, 0x92, 0xc9, 0x97, 0xf0, 0xe8,
	0x9c, 0x0b, 0x96, 0x64, 0x6f, 0xf3, 0x4d, 0x20, 0x42, 0xaf, 0x64, 0xab, 0x5f, 0x4d, 0xa4, 0x92,
	0xf1, 0x31, 0x38, 0x37, 0x39, 0x2b, 0x63, 0xdf, 0x56, 0x4a, 0x0d, 0xc8, 0x31, 0xec, 0x47, 0x25,
	0xcb, 0x2a, 0xb6, 0x12, 0x49, 0x9e, 0x85, 0x31, 0x1e, 0x80, 0xbd, 0x2d, 0x69, 0x27, 0x31, 0xf9,
	0x05, 0x46, 0xba, 0xe9, 0xaa, 0xc8, 0xb3, 0x8a, 0xe3, 0x33, 0x18, 0x8a, 0x24, 0xe5, 0x95, 0x60,
	0x69, 0x61, 0xdc, 0x76, 0x0a, 0xfc, 0x18, 0x7a, 0xe2, 0xae, 0xe0, 0xaa, 0xc6, 0xc1, 0x04, 0x5f,
	0x68, 0x16, 0x64, 0x82, 0x24, 0x7b, 0x17, 0xdd, 0x15, 0x9c, 0x2a, 0xbb, 0x6c, 0xe6, 0x3d, 0x5b,
	0xd7, 0xdc, 0xef, 0xea, 0x66, 0x14, 0x20, 0x7f, 0xda, 0xe0, 0xed, 0x9e, 0xf2, 0xa0, 0x82, 0x86,
	0x22, 0xbb, 0x45, 0x91, 0x6a, 0x41, 0x67, 0xde, 0x96, 0x4b, 0xf3, 0x98, 0xaf, 0xfd, 0x9e, 0x2e,
	0xa7, 0x00, 0x12, 0x18, 0xa5, 0x2c, 0xab, 0xdf, 0xb2, 0x95, 0xa8, 0x4b, 0x5e, 0xfa, 0x8e, 0x32,
	0xb6, 0x74, 0x78, 0x04, 0x03, 0xf5, 0x87, 0xab, 0x7c, 0xed, 0xf7, 0x95, 0x7d, 0x8b, 0x65, 0x25,
	0xd9, 0xa9, 0xbf, 0xa7, 0x2b, 0x49, 0x19, 0x7d, 0xd8, 0x5b, 0xe5, 0x69, 0xca, 0x33, 0xe1, 0x0f,
	0x94, 0x7a, 0x03, 0xf1, 0x33, 0x18, 0xac, 0xf3, 0x15, 0x93, 0x34, 0xfb, 0xc3, 0xb1, 0x75, 0xe2,
	0x4e, 0x0e, 0x0d, 0x3d, 0xf2, 0xc9, 0x73, 0x63, 0xa2, 0x5b, 0x27, 0x7c, 0x0e, 0xfd, 0xbc, 0x16,
	0x45, 0x2d, 0x7c, 0x18, 0x77, 0x4f, 0xdc, 0xc9, 0x07, 0x0d, 0xf7, 0xa5, 0x32, 0x50, 0xe3, 0x40,
	0xfe, 0xb6, 0x60, 0xdf, 0x4c, 0xce, 0x83, 0x58, 0xfb, 0x02, 0xfa, 0x95, 0x60, 0xa2, 0xae, 0xcc,
	0x47, 0x8d, 0x4d, 0xea, 0x56, 0x0e, 0x8d, 0x2e, 0x95, 0x1f, 0x35, 0xfe, 0xf8, 0x1a, 0x1c, 0x29,
	0x69, 0x7a, 0x0f, 0x26, 0xc7, 0xff, 0x1f, 0xc8, 0xa9, 0xf6, 0x26, 0x5f, 0x83, 0xdb, 0xc8, 0x86,
	0x2e, 0xec, 0x5d, 0x2d, 0xce, 0x16, 0xcb, 0xeb, 0x85, 0xd7, 0x91, 0xe0, 0x22, 0x58, 0xcc, 0xc2,
	0xc5, 0x0f, 0x9e, 0x25, 0xc1, 0x35, 0x0d, 0x23, 0x09, 0x6c, 0x1c, 0x40, 0x6f, 0xb6, 0x5c, 0x04,
	0x5e, 0x97, 0x1c, 0x03, 0xec, 0x92, 0x62, 0x1f, 0xec, 0xe5, 0x99, 0xd7, 0xc1, 0x21, 0x38, 0x01,
	0xa5, 0x4b, 0xea, 0x59, 0xe4, 0x2b, 0x38, 0xd8, 0xf1, 0x72, 0x95, 0x25, 0x6a, 0x07, 0x32, 0x96,
	0xf2, 0xcd, 0x0e, 0x48, 0x19, 0x9f, 0x42, 0xbf, 0xba, 0x4b, 0x6f, 0xf2, 0xb5, 0x19, 0x18, 0x83,
	0xc8, 0x6b, 0xbd, 0x42, 0x86, 0x55, 0x96, 0xbd, 0xe3, 0x72, 0xb0, 0xd2, 0x24, 0x53, 0xd1, 0x0e,
	0x95, 0xa2, 0xd2, 0xb0, 0x5b, 0x15, 0x29, 0x35, 0xec, 0x96, 0xfc, 0x61, 0x01, 0xec, 0xe2, 0xb6,
	0x93, 0x67, 0x35, 0x26, 0xef, 0x19, 0x0c, 0x8b, 0x92, 0xaf, 0x92, 0x4a, 0x7e, 0xbb, 0x0e, 0xdd,
	0x29, 0xf0, 0x39, 0xf4, 0xea, 0x2c, 0x11, 0x8a, 0x4c, 0x77, 0xf2, 0xe4, 0xde, 0x07, 0xcb, 0x87,
	0x50, 0xe5, 0x82, 0x9f, 0x82, 0x53, 0xca, 0xc6, 0xd4, 0x08, 0xbb, 0x93, 0xa7, 0xf7, 0x87, 0x41,
	0x5a, 0xa9, 0x76, 0x22, 0x17, 0x30, 0x6a, 0x4e, 0xd5, 0xc3, 0x0f, 0x82, 0xa4, 0x28, 0xe6, 0xef,
	0x93, 0xd5, 0x66, 0x81, 0x0c, 0xfa, 0xe4, 0x77, 0x7d, 0xbc, 0xcc, 0x1a, 0xb7, 0x7f, 0xf0, 0x11,
	0xb8, 0x51, 0x70, 0x7e, 0x11, 0xd0, 0x69, 0x74, 0x45, 0x03, 0xcf, 0xc2, 0x8f, 0xe0, 0xc9, 0x2c,
	0x3c, 0x3d, 0x0d, 0x68, 0xb0, 0x88, 0xc2, 0xe9, 0xfc, 0xcd, 0x05, 0x0d, 0x2e, 0x2f, 0xa5, 0xc9,
	0x96, 0x81, 0xd3, 0x90, 0x9e, 0xce, 0x97, 0xd7, 0x5e, 0x17, 0x47, 0x30, 0xf8, 0xf1, 0xea, 0x3c,
	0x9c, 0x85, 0xd1, 0x4f, 0x5e, 0x0f, 0xf7, 0x61, 0x38, 0x0f, 0x66, 0x6f, 0x2e, 0xa3, 0x69, 0x14,
	0x78, 0xce, 0x06, 0x7e, 0x37, 0x0f, 0x17, 0x67, 0x5e, 0x7f, 0xf2, 0x97, 0x05, 0x6e, 0x98, 0x09,
	0x5e, 0x66, 0x6c, 0x3d, 0x2d, 0x12, 0x7c, 0x09, 0x3d, 0xd9, 0x10, 0x36, 0x8f, 0x8c, 0xb9, 0x7f,
	0x47, 0x87, 0x2d, 0x9d, 0x9e, 0x4a, 0xd2, 0xf9, 0xdc, 0xc2, 0x57, 0xe0, 0xa8, 0x39, 0xc2, 0xc3,
	0xf6, 0xe0, 0xea, 0xb0, 0xc7, 0x46, 0xd9, 0xba, 0x88, 0xa4, 0x83, 0xdf, 0xc0, 0x60, 0x73, 0x96,
	0xb0, 0x49, 0x7c, 0xe3, 0xe4, 0x1e, 0x7d, 0x78, 0x4f, 0xdf, 0x28, 0xfb, 0x2d, 0x78, 0x8d, 0x9c,
	0xdf, 0xff, 0xcc, 0x25, 0xfd, 0xff, 0x56, 0x6c, 0xdb, 0x42, 0x6b, 0xa1, 0x48, 0xe7, 0xa6, 0xaf,
	0xae, 0xce, 0xcb, 0x7f, 0x02, 0x00, 0x00, 0xff, 0xff, 0x48, 0xc0, 0x03, 0x88, 0x58, 0x06, 0x00,
	0x00,
}
