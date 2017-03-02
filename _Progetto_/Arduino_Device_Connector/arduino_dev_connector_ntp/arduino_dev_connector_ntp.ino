/*Merge of NtpClient & mqtt_json*/
#include <SPI.h>
#include <Ethernet.h>
#include <EthernetUdp.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <TimeLib.h>
#include <Time.h>


/*/////////////////////////////////// SETTINGS ///////////////////////////////////////////////////////*/
//Network settings (IP and MQTT)
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
//IPAddress ip(192, 168, 1, 10);
//IPAddress broker(192, 168, 1, 151); //broker address
//IPAddress dnServer(192, 168, 1, 254);
//IPAddress gateway(192, 168, 1, 254);
//IPAddress subnet(255, 255, 255, 0);
IPAddress ip(10, 42, 0, 10);
IPAddress dnServer(10, 42, 0, 1);
IPAddress gateway(10, 42, 0, 1);
IPAddress subnet(255, 255, 255, 0);

IPAddress broker(10, 42, 0, 1); //broker address
unsigned int broker_port = 1883;

IPAddress res_cat(10, 42, 0, 1);
unsigned int res_cat_port = 8080;
char res_cat_s[24];

//NTP settings
char NTP_Server[] = "ntp1.inrim.it";  // I.N.RI.M NTP server (http://www.inrim.it/ntp/index_i.shtml)
unsigned int localPort = 8888;        // local port to listen for UDP packets
const int NTP_PACKET_SIZE = 48;       // NTP time stamp is in the first 48 bytes of the message
byte packetBuffer[ NTP_PACKET_SIZE ]; //buffer to hold incoming and outgoing packets

//INSTANCES
EthernetUDP Udp;    // UDP instance to let us send and receive packets over UDP
EthernetClient http_client;
EthernetClient ethClient;
PubSubClient client(ethClient); //MQTT client to publish

//Analog pin of Temp & Ground_humidity
int pin_temp=0;
int pin_hum=1;


/*/////////////////////////////////// SETUP ///////////////////////////////////////////////////////*/
void setup()
{
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
  ; // wait for serial port to connect. Needed for Leonardo only
  }

//  client.setServer(broker, 1883);
//  client.setCallback(callback);

  // start Ethernet (static addressing) and UDP
  Ethernet.begin(mac, ip, dnServer, gateway, subnet);
  delay(2000);
  Udp.begin(localPort);

  // POST request for device registration into resource catalog!
  // GET request to retrieve broker infos
  if (http_client.connect(res_cat, 8080)) {
    Serial.println("http_client connected");  // DEBUG
    // Make a HTTP request:
    http_client.println("GET /res_cat/broker_info HTTP/1.1");
    sprintf(res_cat_s,"%d.%d.%d.%d:%d",res_cat[0],res_cat[1],res_cat[2],res_cat[3],res_cat_port);
    http_client.print("Host: ");
    http_client.println(res_cat_s);
    http_client.println("Connection: close");
    http_client.println();
  } else {
    // if you didn't get a connection to the server:
    Serial.println("connection of http_client failed"); // DEBUG
  }
  delay(1000);
  // if there are incoming bytes available from the server, read and print them:
  String http_res;
  while(http_client.available()){
    char c = http_client.read();
    //Serial.print(c);  //DEBUG
    http_res = http_res + c;
    // Delete HTTP header
    if(http_res.endsWith("\n")){
      http_res="";
    }
  }
  // if the server's disconnected, stop the client:
  if (!client.connected()) {
    //Serial.println(http_res); // DEBUG
    
    StaticJsonBuffer<150> jsonBuffer;
    JsonObject& data = jsonBuffer.parseObject(http_res);
    if (!data.success()) {
      Serial.println("parseObject() failed");
      return;
    }
    String broker_s = data["broker_ip"];
    IPAddress broker(broker_s.substring(0,3).toInt(),broker_s.substring(4,7).toInt(),broker_s.substring(8,9).toInt(),broker_s.substring(10,13).toInt());
    broker_port = data["broker_port"];
    //Serial.println(broker_s); // DEBUG
    //Serial.println(broker_port);  // DEBUG
    //Serial.println("disconnecting."); // DEBUG
    http_client.stop();
  }

  client.setServer(broker, broker_port);
  client.setCallback(callback);
  
  //NTP request
  sendNTPpacket(Udp, NTP_Server); // send a NTP packet to a time server
  delay(1000);   // wait to see if a reply is available
  
  while (!Udp.parsePacket()) {
    delay(5000);  // if no answer, wait five seconds before asking for the time again
    Ethernet.maintain();
    sendNTPpacket(Udp, NTP_Server); // send a NTP packet to a time server
  }
  
  setTime(readNTPpacket(Udp));  // set system time to one obtained from NTP
  Serial.println(now());  //DEBUGGING
}


/*/////////////////////////////////// LOOP ///////////////////////////////////////////////////////*/
void loop()
{
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Memory pool for JSON object tree.
  StaticJsonBuffer<150> jsonBuffer;
  // Create the root of the object tree.
  JsonObject& data = jsonBuffer.createObject();
  // Fill the json obj
  data["rn"] = "ard1";
  data["hum_gr"] = analogRead(pin_hum);
  data["un_hum"] = "%";
  data["temp"] = analogRead(pin_temp);
  data["un_temp"] = "°C";
  data["timestamp"] = now();
  char string[256];                       //DEBUG
  data.printTo(string, sizeof(string));   //DEBUG
  Serial.println(string);                 //DEBUG
  
  client.publish("outTopic",string,true);   // true --> RETAIN
  delay(5000);
}


/*/////////////////////////////////// FUNCTIONS ///////////////////////////////////////////////////////*/
/*MQTT FUNCTIONS*/
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i=0;i<length;i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("arduinoClient")) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      //client.publish("outTopic","hello world");
      // ... and subscribe
      client.subscribe("inTopic");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}


/*NTP FUNCTIONS*/
// send an NTP request to the time server at the given address
void sendNTPpacket(EthernetUDP Udp, char* address) {
  // set all bytes in the buffer to 0
  memset(packetBuffer, 0, NTP_PACKET_SIZE);
  // Initialize values needed to form NTP request
  // (see URL above for details on the packets)
  packetBuffer[0] = 0b11100011;   // LI, Version, Mode
  packetBuffer[1] = 0;     // Stratum, or type of clock
  packetBuffer[2] = 6;     // Polling Interval
  packetBuffer[3] = 0xEC;  // Peer Clock Precision
  // 8 bytes of zero for Root Delay & Root Dispersion
  packetBuffer[12]  = 49;
  packetBuffer[13]  = 0x4E;
  packetBuffer[14]  = 49;
  packetBuffer[15]  = 52;

  // all NTP fields have been given values, now
  // you can send a packet requesting a timestamp:
  Udp.beginPacket(address, 123); //NTP requests are to port 123
  Udp.write(packetBuffer, NTP_PACKET_SIZE);
  Udp.endPacket();
}

// read packet and return unix time format time
unsigned long readNTPpacket(EthernetUDP Udp){
  // We've received a packet, read the data from it
  Udp.read(packetBuffer, NTP_PACKET_SIZE); // read the packet into the buffer

  // the timestamp starts at byte 40 of the received packet and is four bytes,
  // or two words, long. First, extract the two words:
  unsigned long highWord = word(packetBuffer[40], packetBuffer[41]);
  unsigned long lowWord = word(packetBuffer[42], packetBuffer[43]);
  
  // combine the four bytes (two words) into a long integer
  // this is NTP time (seconds since Jan 1 1900):
  unsigned long secsSince1900 = highWord << 16 | lowWord;

  // now convert NTP time into everyday time:
  // Unix time starts on Jan 1 1970. In seconds, that's 2208988800:
  const unsigned long seventyYears = 2208988800UL;
  // subtract seventy years:
  unsigned long epoch = secsSince1900 - seventyYears;
  return epoch;
}
