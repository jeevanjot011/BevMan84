# BevMan84 – Premium Beverage Ordering System  
**x24231584 – Jeevanjot Singh**  
**Food & Beverage Manufacturing Sector (penultimate digit = 8)**  

Live Application (AWS Cloud9):  
[https://6c55333ff0514a429d88d8735f8b667e.vfs.cloud9.us-east-1.amazonaws.com/]

## Architecture Overview
```mermaid
graph TD
    A[User Browser<br/>Django App] -->|Place Order| B[SNS Topic<br/>BevMan84-Notifications]
    B -->|Subscription| C[SQS Queue<br/>bevman84-queue]
    C -->|Trigger| D[AWS Lambda<br/>.zip Deployment<br/>Python 3.9]
    D -->|PutItem| E[DynamoDB<br/>BevMan84-Orders]
    A -->|Product Images| F[S3 Bucket<br/>bevman84-images]
    B -->|Email/SMS| G[User Notifications]
