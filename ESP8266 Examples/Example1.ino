// Include all needed libraries
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <String.h>

// Define constants
#define SENSOR_INPUT A0 // The PM10 sensor
#define WIFI_SSID "NetworkName" // The netwok name
#define WIFI_PASSWORD "Password123" // The network password
#define HTTP_LOCATION "http://192.168.0.21/" // The URL to the back-end webserver
#define HTTP_PORT 80 // Default HTTP port


void setup() {
	// Set the pinmode of all the pins that are needed
	pinMode(SENSOR_INPUT, INPUT);

	// Connect to the WiFi network
	WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

	// Wait till the ESP is connected to the WiFi network
	while (WiFi.status() != WL_CONNECTED) {
		delay(100);
	}
}

void loop() {
	// Check if the ESP is connected to the WiFi network
	if (WiFi.status() == WL_CONNECTED) {
		// Get the measured value from the PM10 sensor and convert the integer to a char[] (string)
		int measurement = analogRead(SENSOR_INPUT);
		char measurement_str[32];
		sprintf(measurement_str, "%ld", measurement);

		// Declare an object of class HTTPClient
		HTTPClient http_client;
		// Create the end URL
		char http_end_location[100];
		strcpy(http_end_location, HTTP_LOCATION);
		strcpy(http_end_location, "?measurement=");
		strcpy(http_end_location, measurement_str);
		// Start a HTTP request
		http_client.begin(http_end_location);
		// Send the HTTP request and retreive a response
		int http_code = http_client.GET();
		if (http_code == 200) { // HTTP Status 200 means "OK", so the request was successfull
			http_client.end(); // Close the HTTP connection
			delay(1000 * 60 * 10); // Wait 10 minutes before starting this cycle      again
		}
		// If the HTTP statuscode was not 200 there was an error so we do not wait 10 minutes but we start this cycle again immediately after closing the current HTTP connection
		http_client.end();
	}
}
