#if defined(ESP8266)
#include <ESP8266WiFi.h>
#else
#include <WiFi.h>
#endif
#include <WiFiUdp.h>
#include <OSCMessage.h>
#include <Adafruit_NeoPixel.h>
#include "pitches.h";

#ifdef _AVR_
 #include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif
const int Trigger = 2;   // Pin digitale 2 per il Trigger del sensore
const int Echo = 4;      // Pin digitale 4 per l'Echo del sensore
const int buzzer = 10;
const int interval = 8;
const int floor_distance = 50;

#define PIN        7 // On Trinket or Gemma, suggest changing this to 1

char ssid[] = "GL-AR300M-319";              // your network SSID (name)
char pass[] = "goodlife";  // your network password

WiFiUDP Udp;  // A UDP instance to let us send and receive packets over UDP
//192.168.1.137
//const IPAddress outIp(10,40,10,105);        // remote IP of your computer
const IPAddress outIp(192,168,8,185);
const unsigned int outPort = 9999;    // remote port to receive OSC ()
const unsigned int localPort = 8888;  // local port to listen for OSC packets (actually not used for sending)

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS 60 // Popular NeoPixel ring size

// When setting up the NeoPixel library, we tell it how many pixels,
// and which pin to use to send signals. Note that for older NeoPixel
// strips you might need to change the third parameter -- see the
// strandtest example for more information on possible values.
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

#define DELAYVAL 100 // Time (in milliseconds) to pause between pixels

void setup() {
  Serial.begin(9600);
  pinMode(Trigger, OUTPUT);
  pinMode(Echo, INPUT);
 // pinMode(smoke, INPUT);
  pinMode(buzzer, OUTPUT);
  digitalWrite(Trigger, LOW);

// Connect to WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, pass);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");

  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  Serial.println("Starting UDP");
  Udp.begin(localPort);
  Serial.print("Local port: ");
#ifdef ESP32
  Serial.println(localPort);
#else
  Serial.println(Udp.localPort());
#endif
#if defined(_AVR_ATtiny85_) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
#endif
  // END of Trinket-specific code.
pixels.begin(); // INITIALIZE NeoPixel strip object (REQUIRED)
}

void loop() {
  long t;
  long d;
  int pitch = 0;

  digitalWrite(Trigger, HIGH);
  delayMicroseconds(5);
  digitalWrite(Trigger, LOW);
  
  t = pulseIn(Echo, HIGH);
  d = t/59;
  
  Serial.print("Distance: ");
  Serial.print(d);
  Serial.print("cm");
  Serial.println();

sendingOSC(d);
if(d < floor_distance) {
    pitch = NOTE_E1;
  } else if (d < floor_distance + 1*interval) {
    pitch = NOTE_F2;
  } else if (d < floor_distance + 2*interval) {
    pitch = NOTE_C3;
  } else if (d < floor_distance + 3*interval) {
    pitch = NOTE_A3;
  } else if (d < floor_distance + 4*interval) {
    pitch = NOTE_D4;
  } else if (d < floor_distance + 5*interval) {
    pitch = NOTE_C5;
  } else if (d < floor_distance + 6*interval) {
    pitch = NOTE_F5;
  } else if (d < floor_distance + 7*interval) {
    pitch = NOTE_D6;
  }else if (d < floor_distance + 8*interval) {
    pitch = NOTE_G7;
  } else {
    pitch = 0;
  }

  if(pitch == 0) {
    noTone(buzzer);
  } else {
    tone(buzzer, pitch);
  }


  pixels.clear(); // Set all pixel colors to 'off'

  // The first NeoPixel in a strand is #0, second is 1, all the way up
  // to the count of pixels minus one.
     if (d < floor_distance) {
        // Calcola l'intensità dei LED in base alla distanza
        // Usa una mappatura lineare per convertire la distanza in un valore PWM
        int brightness = map(d, 0, floor_distance, 255, 0); // Da 0 a 15 cm, mappa in 255 a 0 (massima a nessuna luminosità)
        
        // Accendi i LED con l'intensità calcolata
        for (int i = 0; i < NUMPIXELS; i++) {
            pixels.setPixelColor(i, pixels.Color(brightness, 0, 0)); // Accendi il LED con l'intensità calcolata in rosso
        }
        pixels.show(); // Invia i colori dei LED all'hardware per accenderli
    } else {
        // Spegni tutti i LED se la distanza è maggiore o uguale a 15 cm
        pixels.clear(); // Spegni tutti i LED
        pixels.show(); // Invia i colori dei LED all'hardware per spegnerli
    }
    delay(DELAYVAL); // Pause before next pass through loop
 }
 void sendingOSC(long d) {
  OSCMessage msg("/test");  // The ID of the OSC Message
  //msg.add("hello, osc!"); // Test hello message
  msg.add(d);
  msg.add(1.0);
  //msg.add(d2); // Send sensor value
  Udp.beginPacket(outIp, outPort);
  msg.send(Udp);
  Udp.endPacket();
  msg.empty();

}

