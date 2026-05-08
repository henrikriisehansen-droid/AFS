# AFS Validator: Comprehensive Feature Walkthrough

The **AFS Validator** is a high-performance desktop utility designed to streamline the testing and validation of **Trustpilot Automatic Feedback Service (AFS)** invitations. This document provides a detailed tour of its features and architectural highlights.

---

## 🎨 User Interface & Layout

The application features a premium, GitHub-inspired dark theme built with **Flet**. The main window is divided into three functional zones for an efficient workflow:

1.  **Left Panel (Email Settings)**: Configure the primary invitation context.
2.  **Center Panel (Payload Preview)**: Real-time visualization of the generated email.
3.  **Right Panel (Parameters)**: Granular control over the JSON metadata.

---

## 🚀 Core Features

### 1. Real-time Payload Generation
As you toggle checkboxes or edit values in the **Parameters** panel, the **Center Preview** updates instantly.
- **HTML Wrapper**: The app generates a standard email body.
- **JSON Script Tag**: It automatically embeds the `<script type="application/json+trustpilot">` block containing your structured data.

### 2. Intelligent Invitation Types
Select from three distinct modes in the **Left Panel**:
- **Service Review**: Minimalist payload for service-only feedback.
- **Service & Product Review (SKU)**: Uses `productSkus` array for simple product matching.
- **Service & Product Review (Direct)**: Uses the `products` array with detailed metadata (URLs, images, brands).
- **Auto-Logic**: Switching types automatically enables/disables relevant fields in the Parameters panel (e.g., toggling `sku` and `name` on for product reviews).

### 3. Integrated JSON Validator
Click the **Validate JSON** button to open a specialized two-column window.
- **Left Column**: Paste any JSON snippet or use the auto-extracted JSON from your current preview.
- **Right Column**: Displays detailed validation results against the official Trustpilot JSON schema.
- **Error Highlighting**: Provides specific line/path information for schema violations (e.g., missing `referenceId` or invalid `locale` format).

### 4. AgentMail Integration
The app integrates directly with the **AgentMail API** to send actual test emails.
- **Direct Send**: Sends the email directly to the AFS address.
- **BCC Mode**: Sends the email to a test recipient (you) while BCC'ing the AFS address, simulating a real-world implementation.

### 5. Advanced Parameter Management
- **Dynamic Fields**: Supports `templateId`, `locale`, `locationId`, `tags`, and `preferredSendTime`.
- **Date Calculation**: Enter a number of days (e.g., "7") for `preferredSendTime`, and the app automatically calculates the ISO timestamp.
- **Randomization Tools**:
    - **Random Reference Number**: Automatically generates a unique 20-character ID for every update.
    - **Random Product Generation**: Generates N number of realistic mock products (Wireless Headphones, Ceramic Mugs, etc.) with unique SKUs and URLs.

---

## 🛠️ Configuration & Settings

Accessed via the **Settings** button, the configuration dialog allows you to manage:
- **API Credentials**: Securely enter your AgentMail API Key and Inbox ID.
- **Afs Direct Toggle**: Switch between sending directly to Trustpilot or using a BCC workflow.
- **Product Generation**: Set the count (1-50) for random product testing.

---

## 🏗️ Technical Architecture

- **Language**: Python 3.12+
- **UI Framework**: Flet (Flutter-based)
- **State Management**: Model-View-Controller (MVC) pattern.
    - `MainController`: Orchestrates data flow and business logic.
    - `PayloadBuilder`: Handles complex dictionary construction and HTML templating.
    - `ConfigManager`: Manages persistent storage in `config.toml`.
- **Validation**: `jsonschema` library for robust payload verification.
