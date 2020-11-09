#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Update these with values suitable for your network.

const char* ssid = "TP link";
const char* password = "arkoshakis";
const char* mqtt_server = "192.168.0.103";

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE  (50)
char msg[MSG_BUFFER_SIZE];
int value = 0;

#define srPin 10

void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
  if ((char)payload[0] == 'c' && (char)payload[1] == 'h' && (char)payload[2] == 'e' && (char)payload[3] == 'c' && (char)payload[4] == 'k') {
    client.publish("status", "board 1 online");
  }
  else if ((char)payload[0] == 't' && (char)payload[1] == 'e' && (char)payload[2] == 'm' && (char)payload[3] == 'p') {
    client.publish("tdata", "23");
  }
  else if ((char)payload[0] == 'm' && (char)payload[1] == 'b' && (char)payload[2] == 'l' && (char)payload[3] == 'o' && (char)payload[4] == 'n') {
    digitalWrite(BUILTIN_LED, LOW); 
  }
  else if ((char)payload[0] == 'm' && (char)payload[1] == 'b' && (char)payload[2] == 'l' && (char)payload[3] == 'o' && (char)payload[4] == 'f') {
    digitalWrite(BUILTIN_LED, HIGH);
  }
  else if ((char)payload[0] == 's' && (char)payload[1] == 'r' && (char)payload[2] == 'l' && (char)payload[3] == 'o' && (char)payload[4] == 'n') {
    digitalWrite(srPin, HIGH);
  }
  else if ((char)payload[0] == 's' && (char)payload[1] == 'r' && (char)payload[2] == 'l' && (char)payload[3] == 'o' && (char)payload[4] == 'f') {
    digitalWrite(srPin, LOW);
  }

}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      client.publish("status", "board 1 online");
      client.subscribe("lightsIn");
      client.subscribe("check");
      client.subscribe("temp");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup() {
  pinMode(BUILTIN_LED, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  pinMode(srPin, OUTPUT);;
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long now = millis();
  /*if (now - lastMsg > 2000) {
    lastMsg = now;
    ++value;
    snprintf (msg, MSG_BUFFER_SIZE, "hello world #%ld", value);
    Serial.print("Publish message: ");
    Serial.println(msg);
    client.publish("outTopic", msg);
  }*/
}
