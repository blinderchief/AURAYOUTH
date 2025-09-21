+---------------+         +---------------+
|   Youth User  |         | Mental Health |
|               |         | Professional  |
+---------------+         +---------------+
         |                           |
         |                           |
         V                           V
+------------------------------------------+
|              AuraYouth System            |
|                                          |
| - Use Case 1: Engage in Chatbot Session  |
|   (Actor: User; Goal: Get CBT advice)    |
|                                          |
| - Use Case 2: Perform Mood Check         |
|   (Actor: User; Goal: Detect emotions)   |
|                                          |
| - Use Case 3: Join Echo Network          |
|   (Actor: User; Goal: Peer support)      |
|                                          |
| - Use Case 4: Review Flagged Cases       |
|   (Actor: Professional; Goal: Intervene) |
+------------------------------------------+



Start
 |
 V
User Opens App --> Anonymous Login
 |
 V
+--------------------+
| Choose Action      |
+--------------------+
 |          |        |
 V          V        V
Chat      Mood     Echo
Query     Check    Network
 |          |        |
 V          V        |
NLP       Multimodal  Peer Match
Process   Scan       |
 |          |        |
 V          V        |
Fuse Data ------------> Update Digital Twin
 |                       |
 V                       V
Predict Risk? --> Yes --> Offer Exercise / Alert Human
 |                                |
 No                               V
 |                              Escalate if Crisis
 V
Log Progress --> End / Reminder



+-------------------+          +-------------------+
|   User Device     |          |   FastAPI Backend |
| - React Native App| <------> | - APIs / WebSockets|
| - On-Device AI    |          | - MongoDB Metadata |
|   (TF Lite, PyTorch)|        +-------------------+
+-------------------+                 |
         |                             V
         V                       +-----------------+
   +-------------+               |   AI Core       |
   | Multimodal  |               | - VaultGemma LLM|
   | Sensing     | <-----------> | - Digital Twins |
   +-------------+               | - Agentic AI    |
                                 +-----------------+
                                       |
                                       V
                                 +-----------------+
                                 | Privacy Layer   |
                                 | - Federated     |
                                 |   Learning      |
                                 +-----------------+
                                       |
                                       V
                                 +-----------------+
                                 | Oversight       |
                                 | - Human Dashboard|
                                 +-----------------+




