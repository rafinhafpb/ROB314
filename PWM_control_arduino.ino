#define NUM_MOTORS 4

// PWM pins to control motor speed
const int pwmPins[NUM_MOTORS] = {3, 5, 6, 9};
// Direction pins to set motor rotation direction
const int dirPins[NUM_MOTORS] = {2, 4, 7, 8};

void setup() {
  Serial.begin(115200);  // Initialize serial communication
  for (int i = 0; i < NUM_MOTORS; i++) {
    pinMode(pwmPins[i], OUTPUT);  // Set PWM pins as output
    pinMode(dirPins[i], OUTPUT);  // Set direction pins as output
  }
}

void loop() {
  // Check if there is incoming serial data
  if (Serial.available() > 0) {
    // Read the incoming data until newline character is detected
    String inputString = Serial.readStringUntil('\n');
    int speeds[NUM_MOTORS] = {0, 0, 0, 0};
    
    // Parse the comma-separated values from the input string
    if (parseSpeeds(inputString, speeds)) {
      for (int i = 0; i < NUM_MOTORS; i++) {
        int speedValue = abs(speeds[i]);                    // Get the absolute speed (0 to 100)
        int pwmValue = map(speedValue, 0, 100, 0, 255);      // Map speed to PWM value (0 to 255)
        
        // Set the motor direction: HIGH for positive, LOW for negative speed values
        digitalWrite(dirPins[i], speeds[i] >= 0 ? HIGH : LOW);
        // Write the PWM value to control the motor speed
        analogWrite(pwmPins[i], pwmValue);
      }
    }
  }
}

// Function to parse a comma-separated string of 4 integers into an array
bool parseSpeeds(String input, int *speeds) {
  // Create a buffer for the input string
  char buf[input.length() + 1];
  input.toCharArray(buf, input.length() + 1);
  
  // Tokenize the string using comma as the delimiter
  char *token = strtok(buf, ",");
  int index = 0;
  while (token != NULL && index < NUM_MOTORS) {
    speeds[index++] = atoi(token);
    token = strtok(NULL, ",");
  }
  // Return true if exactly 4 values have been parsed
  return (index == NUM_MOTORS);
}