## Setup
To be able to run this on your local machine, start by running the following in your terminal after cloning the repository:
```
pip install -r requirements.txt
```

If you would like to re-create the output sheets used for my solution to see the creation process (documented by print statements), you can also run:
```
python scripts/main.py
```
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
3. The constituents' donation

## Data Cleaning
From manually looking at the data sheets, I found the primary key across the 3 input sheets to be **Patron ID**. I also noticed that in the donation history, there are statuses listed as "Refunded". 
For these listings, **I assumed that the donation amount should be set to zero for "Refunded" listings since there was no income**. I also **assumed that the different types of campaigns were seperate events** for the sake of simplicity.

I then started following the requirements listed in each of the output sheets ("Output Format: CueBox Constituents", "Output Format: CueBox Tags"). Based on this, as well as observations from looking at the data, I made these requirements and assumptions about the data.
### CueBox Constituents
1. Constituent ID is a unique identifier; can be used for joins.
2. If the type field does not contain a person's name or company name, the corresponding row is invalid
    1. First/last name is required for "Person" types, while company name is required for "Company" types
    2. **Assuming that names should be kept uniform using convention of capitalized first letters for first/last names**
3. If the "Created At" timestamp is empty, the corresponding row is invalid. (Found in: "Donation History")
    1. **Assuming that the timestamp should be uniform in the Month DD, YYYY format**
4. Email 1 and 2 are vaguely mentioned as having to be "standardized and well-formatted for a valid domain". (Found in "Donation History"/"Email")
    1. **Assuming that the "email-validator" library suffices to check that an email is "valid"**.
    2. **Assuming Email 1 refers to the primary email from the "Donation History" sheet or the email from the "Emails" sheet in the absence of a valid primary email**
    3. **Assuming Email 2 refers to an email from the "Emails" sheet in the presence of a different, valid primary email from the "Donation History" sheet**
5. Title can be empty (Found in: "Donation History")
6. Tags are passed through a given API to standardize: https://6719768f7fc4c5ff8f4d84f1.mockapi.io/api/v1/tags
    1. **Assuming that tag names without a mapped name should be kept as-is**
7. Format standard for currency is "$x.xx"; formatted as a string (for empty-string case)
    1. **Assumes the "Lifetime Donation" is total donations/number of donations**
8. **Assuming Month DD, YYYY format for most recent donation date**
9. **Assuming that currency should follow the same format as lifetime donation**

### CueBox Tags
1. **Assuming that tags should be passed through the same API to clean**
2. **Assuming tag number is formatted as int**

## Output sheet creation



## Conclusion & Questions
