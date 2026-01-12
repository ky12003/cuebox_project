## Overview + Introduction
To start my solution to this project, I first looked at the important information about the data sheet given, and the information is noted here for easy reference:

"Information about the Constituents input sheet:
* This sheet has one row per constituent.

"Information about the Emails input sheet:
* This sheet has one row per constituent per email. So if a constituent has 2 emails, then that will be 2 rows in the Emails sheet.
* If a constituent has a Primary Email in the Constituent sheet, then that email is guaranteed to be in the Emails input sheet as well, along with any additional emails that the constituent has."

"Information about the Donation History input sheet:
* This sheet has one row per donation that has ever been made."

Constituents are defined as the people and companies who attend events and make donations. The client cares a lot about this data because they use it to for marketing and fundraising outreach.

Next, I looked at the desired output:
* Produce two output spreadsheets that can be presented to the client for sign-off and then imported into CueBox. The client cares a lot about this data because they use it to for marketing and fundraising outreach.

Looking at this, there seems to be no defined output as a goal; only a repeated phrase: **The client cares a lot about this data because they use it to for marketing and fundraising outreach**.

However, I am also given 2 output sheets with the following columns:
* CueBox Constituents: CB Constituent ID, CB Constituent Type
, CB First Name , CB Last Name , CB Company Name , CB Created At , CB Email 1 (Standardized) , CB Email 2 (Standardized) , CB Title , CB Tags , CB Background Information , CB Lifetime Donation Amount , CB Most Recent Donation Date ,CB Most Recent Donation Amount
* CueBox Tags: CB Tag Name, CB Tag Count

From these 2 key pieces of information, I made the following assumptions
1. The method of outreach will primarily be by email
2. The constituents' donation amount is an important factor when choosing who to do prioritize when doing outreach.
3. 

## Data Cleaning
From manually looking at the data sheets, I found the primary key across the 3 input sheets to be **Patron ID**. I then started following the requirements listed in each of the output sheets ("Output Format: CueBox Constituents")

## Data Exploration
I looked at some key metrics for the data overall in the **data_exploration.ipynb** file to get a better understanding of the data as an extra endeavour. This was done fairly quickly, as it is more for fun/for exploration.

**Constituents**

**Emails**:

**Donation History**:

**Overall**



