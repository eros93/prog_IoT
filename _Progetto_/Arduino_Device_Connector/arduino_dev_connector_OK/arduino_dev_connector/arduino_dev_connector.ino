#include <SPI.h>
#include <Ethernet.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <TimeLib.h>
#include <Time.h>


/*/////////////////////////////////// SETTINGS ///////////////////////////////////////////////////////*/
//Network settings (IP and MQTT)
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
IPAddress ip(192, 168, 1, 10);
IPAddress dnServer(192, 168, 1, 254);
IPAddress gateway(192, 168, 1, 254);
IPAddress subnet(255, 255, 255, 0);
//IPAddress ip(10, 42, 0, 10);
//IPAddress dnServer(10, 42, 0, 1);
//IPAddress gateway(10, 42, 0, 1);
//IPAddress subnet(255, 255, 255, 0);

//IPAddress broker(10, 42, 0, 1); //broker address
IPAddress broker(192, 168, 1, 151); //broker address
unsigned int broker_port = 1883;

//IPAddress res_cat(10, 42, 0, 1);
IPAddress res_cat(192, 168, 1, 71);
unsigned int res_cat_port = 8080;
char res_cat_s[24];

//INSTANCES
EthernetClient http_client;
EthernetClient ethClient;
PubSubClient client(ethClient); //MQTT client to publish

//Analog pin of Temp & Ground_humidity
int pin_hum = 0;
int pin_temp = 1;

//POST-DATA
String rn = "ard1";
String subn = "1";
String res = "[\"temp\",\"hum_gr\"]";
char mqtt_r = 'p';
String mqtt_t;


/*/////////////////////////////////// SETUP ///////////////////////////////////////////////////////*/
void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }

  // Start Ethernet (static addressing)
  Ethernet.begin(mac, ip, dnServer, gateway, subnet);
  delay(2000);

  //Create JSON and make REGISTRATION to resource catalog
  String PostData = create_PostData_json();
  res_cat_registration(PostData);

  //GET and SET Broker IP and port
  get_set_broker_ip_port();
}


/*/////////////////////////////////// LOOP /////////////////////////////////////////////////////*/
void loop() {
  //MQTT stuffs
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  //CREATE JSON of data from SENSOR
  // Memory pool for JSON object tree.
  StaticJsonBuffer<150> jsonBuffer;
  // Create the root of the object tree.
  JsonObject& data = jsonBuffer.createObject();
  // Fill the json obj
  data["rn"] = rn;
  //data["hum_gr"] = analogRead(pin_hum);
  data["hum_gr"] = ground_hum(pin_hum);
  data["un_hum"] = "%";
  data["temp"] = analogRead(pin_temp);
  data["un_temp"] = "°C";
  data["timestamp"] = now();
  char string[100];                       //DEBUG
  data.printTo(string, sizeof(string));   //DEBUG
  Serial.println(string);                 //DEBUG

  client.publish(mqtt_t.c_str(), string, true); // true --> RETAIN
  //delay(600000);  //Publish every 10 minutes
  //delay(300000);  //Publish every 5 minutes
  //delay(120000);  //Publish every 2 minutes
  delay(60000);  //Publish every minute
  //delay(1000);  //Publish every5 second DEBUG
}






/*/////////////////////////////////// FUNCTIONS ///////////////////////////////////////////////////////*/
/*HUMIDITY & TEMPERATURE functions*/
int ground_hum(int pin) {
  int reading = analogRead(pin);
  if (reading < 400) {
    reading = 400;
  }
  int sensorValue = map(reading, 1023, 400, 0, 100);
  return sensorValue;
}

/*RESOURCE CATALOG tools & communications*/
String create_PostData_json() {
  String ip_s = String(ip[0]) + "." + String(ip[1]) + "." + String(ip[2]) + "." + String(ip[3]);
  mqtt_t = "sensor/subnet/" + String(subn) + "/hum_temp";
  String PostData = "{\"subnet\":\"" + subn + "\",\"mqtt_topic\":\"" + mqtt_t + "\",\"mqtt_role\":\"" + mqtt_r + "\",\"rn\":\"" + rn + "\",\"ip_address\":\"" + ip_s + "\",\"resources\":" + res + "}";
  //Serial.println(PostData);
  return PostData;
}

void res_cat_registration(String PostData) {
  // POST request for device registration into resource catalog!
  if (http_client.connect(res_cat, 8080)) {
    Serial.println("Connected to Resource Catalog for registration");  // DEBUG
    // Make a HTTP request:
    http_client.println("POST /res_cat/new_dev HTTP/1.1");
    http_client.print("Host: ");

    sprintf(res_cat_s, "%d.%d.%d.%d:%d", res_cat[0], res_cat[1], res_cat[2], res_cat[3], res_cat_port);
    http_client.println(res_cat_s);

    http_client.println("Connection: close");
    http_client.print("Content-Length: ");
    http_client.println(PostData.length());
    http_client.println();
    http_client.println(PostData);
    http_client.println();
  }
  else {
    // if you didn't get a connection to the server:
    Serial.println("connection to res_cat failed"); // DEBUG
  }
  delay(1000);
  // if there are incoming bytes available from the server, read and work on them:
  String http_res;
  while (http_client.available()) {
    char c = http_client.read();
    //Serial.print(c);  //DEBUG
    http_res = http_res + c;
    // Delete HTTP header
    if (http_res.endsWith("200 OK")) {
      Serial.println("Device Registration OK!"); // DEBUG
    }
  }
  // if the server's disconnected, stop the client:
  if (!http_client.connected()) {
    Serial.println("Disconnecting."); // DEBUG
    http_client.stop();
  }
}

void get_set_broker_ip_port() {
  // GET request to retrieve broker infos
  if (http_client.connect(res_cat, 8080)) {
    Serial.println("Connected to Resource Catalog to get broker infos");  // DEBUG
    // Make a HTTP request:
    http_client.println("GET /res_cat/broker_info HTTP/1.1");
    sprintf(res_cat_s, "%d.%d.%d.%d:%d", res_cat[0], res_cat[1], res_cat[2], res_cat[3], res_cat_port);
    http_client.print("Host: ");
    http_client.println(res_cat_s);
    http_client.println("Connection: close");
    http_client.println();
  }
  else {
    // if you didn't get a connection to the server:
    Serial.println("connection of http_client failed"); // DEBUG
  }
  delay(1000);
  // if there are incoming bytes available from the server, read and print them:
  String http_res;
  while (http_client.available()) {
    char c = http_client.read();
    //Serial.print(c);  //DEBUG
    http_res = http_res + c;
    // Delete HTTP header
    if (http_res.endsWith("\n")) {
      http_res = "";
    }
  }
  // if the server's disconnected, stop the client:
  if (!http_client.connected()) {
    //Serial.println(http_res); // DEBUG

    StaticJsonBuffer<150> jsonBuffer;
    JsonObject& data = jsonBuffer.parseObject(http_res);
    if (!data.success()) {
      Serial.println("parseObject() failed");
      return;
    }
    String broker_s = data["broker_ip"];
    IPAddress broker(broker_s.substring(0, 3).toInt(), broker_s.substring(4, 7).toInt(), broker_s.substring(8, 9).toInt(), broker_s.substring(10, 13).toInt());
    broker_port = data["broker_port"];
    setTime(data["timestamp"]); // set system time to one obtained from json
    Serial.print("Broker: ");
    Serial.print(broker_s); // DEBUG
    Serial.print(":");
    Serial.println(broker_port);  // DEBUG
    //Serial.println(now());  // DEBUG
    Serial.println("Disconnecting."); // DEBUG
    http_client.stop();
  }

  //SET Broker Ip and port
  client.setServer(broker, broker_port);
  client.setCallback(callback);
}


/*MQTT FUNCTIONS*/
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
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
