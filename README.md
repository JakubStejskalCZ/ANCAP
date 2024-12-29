# Ancap Simulation Bot

Ancap Simulation Bot is a Discord bot designed to simulate a decentralized anarcho-capitalist society. It allows users to create virtual citizens, manage resources, run companies, participate in trade, and handle various other economic and social functions within a simulated society.

---

## **Features**
- Create and manage virtual citizens.
- Simulate ownership and management of companies, roads, and regions.
- Handle insurance, loans, public projects, and trade routes.
- Dynamic language support with persistent user preferences.
- Test mode for safe experimentation.
- Background tasks for economic updates, insurance payments, and loan management.

---

## **Commands**

### **Citizen Commands**
#### **`!create_citizen`**
- **Description:** Create a new citizen for the simulation.
- **Parameters:** None.
- **Example:** `!create_citizen`

#### **`!view_citizen`**
- **Description:** View details about your citizen.
- **Parameters:** None.
- **Example:** `!view_citizen`

#### **`!delete_citizen`**
- **Description:** Delete your citizen.
- **Parameters:** None.
- **Example:** `!delete_citizen`

---

### **Company Commands**
#### **`!create_company <name>`**
- **Description:** Create a new company.
- **Parameters:**
  - `<name>`: The name of the company.
- **Example:** `!create_company "MyCompany"`

#### **`!view_companies`**
- **Description:** View all existing companies.
- **Parameters:** None.
- **Example:** `!view_companies`

#### **`!set_price <company_id> <price>`**
- **Description:** Set the price of services offered by a company.
- **Parameters:**
  - `<company_id>`: The ID of the company.
  - `<price>`: The price of the service.
- **Example:** `!set_price 1 100`

---

### **Region Commands**
#### **`!create_region <name>`**
- **Description:** Create a new region.
- **Parameters:**
  - `<name>`: The name of the region.
- **Example:** `!create_region "NewRegion"`

#### **`!list_regions`**
- **Description:** List all regions.
- **Parameters:** None.
- **Example:** `!list_regions`

#### **`!update_prosperity <region_id> <value>`**
- **Description:** Update the prosperity of a region.
- **Parameters:**
  - `<region_id>`: The ID of the region.
  - `<value>`: The new prosperity value.
- **Example:** `!update_prosperity 1 75`

---

### **Road Commands**
#### **`!create_road <name> <fee>`**
- **Description:** Create a new road with a specified access fee.
- **Parameters:**
  - `<name>`: The name of the road.
  - `<fee>`: The access fee for the road.
- **Example:** `!create_road "MainRoad" 10`

#### **`!list_roads`**
- **Description:** List all roads and their details.
- **Parameters:** None.
- **Example:** `!list_roads`

#### **`!update_access_fee <road_id> <fee>`**
- **Description:** Update the access fee for a road.
- **Parameters:**
  - `<road_id>`: The ID of the road.
  - `<fee>`: The new access fee.
- **Example:** `!update_access_fee 1 15`

---

### **Housing Commands**
#### **`!view_housing`**
- **Description:** View available housing options.
- **Parameters:** None.
- **Example:** `!view_housing`

#### **`!rent_house <house_id>`**
- **Description:** Rent a house by specifying its ID.
- **Parameters:**
  - `<house_id>`: The ID of the house.
- **Example:** `!rent_house 1`

---

### **Insurance Commands**
#### **`!view_insurance`**
- **Description:** View available insurance plans.
- **Parameters:** None.
- **Example:** `!view_insurance`

#### **`!apply_insurance <company_id>`**
- **Description:** Apply for insurance with a specific company.
- **Parameters:**
  - `<company_id>`: The ID of the company offering insurance.
- **Example:** `!apply_insurance 2`

---

### **Loan Commands**
#### **`!offer_loan <borrower_id> <amount> <interest_rate> <term>`**
- **Description:** Offer a loan to another citizen.
- **Parameters:**
  - `<borrower_id>`: The ID of the borrower.
  - `<amount>`: The loan amount.
  - `<interest_rate>`: The interest rate in percentage.
  - `<term>`: The repayment term in months.
- **Example:** `!offer_loan 3 1000 5 12`

#### **`!list_loans`**
- **Description:** List all loans.
- **Parameters:** None.
- **Example:** `!list_loans`

#### **`!repay_loan <loan_id> <amount>`**
- **Description:** Repay a specified loan.
- **Parameters:**
  - `<loan_id>`: The ID of the loan.
  - `<amount>`: The amount to repay.
- **Example:** `!repay_loan 1 500`

---

### **Trade Commands**
#### **`!create_trade_route <region_a_id> <region_b_id> <tariff_rate>`**
- **Description:** Create a trade route between two regions.
- **Parameters:**
  - `<region_a_id>`: The ID of the first region.
  - `<region_b_id>`: The ID of the second region.
  - `<tariff_rate>`: The tariff rate in percentage.
- **Example:** `!create_trade_route 1 2 10`

#### **`!list_trade_routes`**
- **Description:** List all trade routes.
- **Parameters:** None.
- **Example:** `!list_trade_routes`

---

### **Public Project Commands**
#### **`!create_public_project <name> <cost>`**
- **Description:** Create a new public project.
- **Parameters:**
  - `<name>`: The name of the project.
  - `<cost>`: The total cost of the project.
- **Example:** `!create_public_project "BridgeProject" 5000`

#### **`!fund_project <project_id> <amount>`**
- **Description:** Fund a public project with a specified amount.
- **Parameters:**
  - `<project_id>`: The ID of the project.
  - `<amount>`: The amount to contribute.
- **Example:** `!fund_project 1 500`

---

### **Locale Commands**
#### **`!set_locale <locale>`**
- **Description:** Set your preferred language.
- **Parameters:**
  - `<locale>`: The locale to set (e.g., `en`, `cs`).
- **Example:** `!set_locale en`

#### **`!get_locale`**
- **Description:** Get your current language setting.
- **Parameters:** None.
- **Example:** `!get_locale`

---

## **Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ancap-simulation-bot.git
   cd ancap-simulation-bot
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create and configure the `.env` file:
   ```plaintext
   DISCORD_BOT_TOKEN=your_discord_bot_token_here
   DATABASE_URL=sqlite+aiosqlite:///database.db
   PREFIX=!
   LOCALE=en
   GUILD_NAME=YourGuildNameHere
   TEST_MODE=False
   ```

5. Run the bot:
   ```bash
   python bot.py
   ```

---

## **License**

This project is licensed under the MIT License. See the LICENSE file for details.

```plaintext
MIT License

Copyright (c) [Year]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```