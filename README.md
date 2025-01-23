# Game-Day-Notifications
Game Day Notifications is an alert system that sends real-time MLS game day score notifications to subscribed users. It leverages Amazon SNS, AWS Lambda and Python, Amazon EventBridge and NBA APIs to provide sports fans with up-to-date game information. The project demonstrates cloud computing principles and efficient notification mechanisms.

## Features 
- Fetches live MLS game scores using an external API.
- Sends formatted score updates to subscribers via SMS/Email using Amazon SNS.
- Scheduled automation for regular updates using Amazon EventBridge.
- Designed with security in mind, following the principle of least privilege for IAM roles.

## Technologies 
**Cloud Provider:** AWS
**Core Services:** SNS, Lambda, EventBridge
**External API:** NBA Game API (SportsData.io)
**Programming Language:** Python 3.x
**IAM Security:**
  - Least privilege policies for Lambda, SNS, and EventBridge.

## Project Structure
  game-day-notifications/
  ├── src/
  │   ├── gd_notifications.py          # Main Lambda function code
  ├── policies/
  │   ├── gb_sns_policy.json           # SNS publishing permissions
  │   ├── gd_eventbridge_policy.json   # EventBridge to Lambda permissions
  │   └── gd_lambda_policy.json        # Lambda execution role permissions
  ├── .gitignore
  └── README.md                        # Project documentation

## Technical Architecture
  ![Screenshot 2025-01-22 205003](https://github.com/user-attachments/assets/c3094faf-f507-490c-bd07-6ea74459eb40)
