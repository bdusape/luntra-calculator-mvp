# 📊 LUNTRA Beta - Data Collection Setup Guide

## 🎯 **Current Data Collection Status**

### **✅ What's Working Now**
1. **Session-Level Tracking** - Data captured during user sessions
2. **JSON Export** - Users can download their session data
3. **Built-in Dashboard** - Real-time analytics in the app

### **⚠️ What's Missing**
- **Persistent Storage** - Data is lost when sessions end
- **Cross-Session Analytics** - No way to track returning users
- **Aggregate Reporting** - No centralized data analysis

---

## 🔧 **Persistent Data Collection Options**

### **Option 1: Google Sheets (Recommended for Beta)**
**Pros:** Free, easy setup, familiar interface, good for small scale
**Cons:** Rate limits, not suitable for high volume

#### **Setup Steps:**
1. **Create Google Sheet:**
   - Go to https://sheets.google.com
   - Create new sheet named "LUNTRA Beta Analytics"
   - Create tabs: "Analytics", "Feedback", "ROI_Data"

2. **Set up Google Apps Script:**
   ```javascript
   function doPost(e) {
     var sheet = SpreadsheetApp.getActiveSheet();
     var data = JSON.parse(e.postData.contents);
     
     // Add timestamp and data to sheet
     sheet.appendRow([
       new Date(),
       data.event || data.type,
       data.session_id,
       data.user_id,
       JSON.stringify(data)
     ]);
     
     return ContentService.createTextOutput("OK");
   }
   ```

3. **Deploy as Web App:**
   - Get webhook URL
   - Update `app.py` with your webhook URL

#### **Cost:** Free (up to Google's usage limits)

---

### **Option 2: Airtable (Great for Beta)**
**Pros:** User-friendly, good API, free tier sufficient
**Cons:** Limited free records (1,200/base)

#### **Setup Steps:**
1. **Create Airtable Base:**
   - Go to https://airtable.com
   - Create base: "LUNTRA Beta Metrics"
   - Tables: Analytics, Feedback, ROI_Feedback

2. **Get API Key:**
   - https://airtable.com/create/tokens
   - Create token with full access to your base

3. **Update Code:**
   ```python
   AIRTABLE_API_KEY = "your_api_key"
   AIRTABLE_BASE_ID = "your_base_id"
   
   def send_to_airtable(data, table_name):
       url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{table_name}"
       headers = {
           "Authorization": f"Bearer {AIRTABLE_API_KEY}",
           "Content-Type": "application/json"
       }
       payload = {"records": [{"fields": data}]}
       requests.post(url, json=payload, headers=headers)
   ```

#### **Cost:** Free (1,200 records/month)

---

### **Option 3: Webhook.site (Testing Only)**
**Pros:** Instant setup, perfect for testing
**Cons:** Data not persistent, only for development

#### **Setup Steps:**
1. Go to https://webhook.site
2. Copy your unique webhook URL
3. Update `app.py` with the URL
4. View data in real-time on webhook.site

#### **Cost:** Free

---

### **Option 4: Supabase (Scalable)**
**Pros:** PostgreSQL database, real-time features, generous free tier
**Cons:** More complex setup

#### **Setup Steps:**
1. **Create Supabase Project:**
   - Go to https://supabase.com
   - Create new project

2. **Create Tables:**
   ```sql
   -- Analytics table
   CREATE TABLE analytics (
     id SERIAL PRIMARY KEY,
     created_at TIMESTAMP DEFAULT NOW(),
     event TEXT,
     session_id TEXT,
     user_id TEXT,
     properties JSONB
   );
   
   -- Feedback table
   CREATE TABLE feedback (
     id SERIAL PRIMARY KEY,
     created_at TIMESTAMP DEFAULT NOW(),
     type TEXT,
     content TEXT,
     session_id TEXT,
     properties JSONB
   );
   ```

3. **Get API Keys:**
   - Project URL
   - Anon key
   - Service role key

#### **Cost:** Free (500MB database, 2GB bandwidth)

---

### **Option 5: Simple Webhook + Google Forms**
**Pros:** No coding required, free, familiar
**Cons:** Manual data processing

#### **Setup Steps:**
1. **Create Google Forms:**
   - Analytics form
   - Feedback form
   - ROI feedback form

2. **Use Zapier/Make to connect:**
   - Webhook → Google Forms submission
   - Automatic spreadsheet population

#### **Cost:** Free (Google) + Zapier free tier

---

## 🚀 **Recommended Setup for LUNTRA Beta**

### **Phase 1: Immediate (This Week)**
**Use Google Sheets + Apps Script**

```bash
# Steps to implement:
1. Create Google Sheet with tabs for Analytics/Feedback/ROI
2. Set up Apps Script webhook (5 minutes)
3. Update app.py with webhook URLs
4. Deploy to Streamlit Cloud
5. Test data collection
```

### **Phase 2: Growth (Month 2)**
**Upgrade to Airtable or Supabase**

```bash
# When you hit limits or need better analysis:
1. Export data from Google Sheets
2. Set up Airtable/Supabase
3. Import historical data
4. Update webhook endpoints
5. Build dashboard in Looker Studio/Tableau
```

### **Phase 3: Scale (Month 3+)**
**Professional Analytics Stack**

```bash
# Full production setup:
1. GA4 + GTM for web analytics
2. Mixpanel/PostHog for product analytics
3. BigQuery for data warehouse
4. Looker Studio for dashboards
5. Automated email reports
```

---

## 📋 **Implementation Checklist**

### **Google Sheets Setup (Recommended First Step)**

- [ ] Create Google Sheet: "LUNTRA Beta Analytics"
- [ ] Add tabs: Analytics, Feedback, ROI_Data
- [ ] Set up Google Apps Script webhook
- [ ] Deploy script as web app
- [ ] Copy webhook URLs
- [ ] Update `app.py` webhook URLs
- [ ] Test with sample data
- [ ] Deploy to Streamlit Cloud
- [ ] Verify data collection working

### **Data Structure Setup**

#### **Analytics Sheet Columns:**
- Timestamp
- Event
- Session ID
- User ID
- Properties (JSON)
- Purchase Price
- Workflow Type
- Session Duration

#### **Feedback Sheet Columns:**
- Timestamp
- Type (feature_request, bug_report, rating, roi_feedback)
- Content
- Session ID
- User Agent
- Workflow Count
- Properties (JSON)

#### **ROI Sheet Columns:**
- Timestamp
- Time Saved
- Helped Decision
- Manual Cost
- Thumbs Feedback
- Workflow Count
- Session ID

---

## 📊 **Data Analysis Setup**

### **Google Sheets Analysis**
- Pivot tables for event counts
- Charts for workflow success rates
- ROI feedback analysis
- Session duration trends

### **Looker Studio Dashboard (Free)**
- Connect to Google Sheets
- Real-time analytics dashboard
- Shareable reports
- KPI tracking

### **Key Metrics to Track**
1. **Daily Active Sessions**
2. **Workflow Completion Rate**
3. **Time-to-First-Value (TTFV)**
4. **User Satisfaction Scores**
5. **ROI Feedback Trends**
6. **Feature Request Themes**

---

## 🔧 **Quick Implementation Commands**

```bash
# 1. Update the app with your webhook URLs
# Edit app.py lines 156-157 with your webhook URLs

# 2. Test locally
streamlit run app.py

# 3. Commit and deploy
git add app.py DATA_COLLECTION_SETUP.md
git commit -m "Add persistent data collection setup"
git push origin main

# 4. Verify data collection in your chosen service
```

---

## 📈 **Expected Data Volume (Beta)**

### **Week 1:**
- 100 sessions × 5 events/session = 500 analytics events
- 20 feedback submissions
- 10 ROI feedback responses

### **Month 1:**
- 2,000 sessions × 5 events/session = 10,000 analytics events
- 200 feedback submissions  
- 100 ROI feedback responses

**Total: ~10,300 records/month** (well within free tiers of most services)

---

## ⚡ **Next Steps**

1. **Choose your data collection method** (recommend Google Sheets for beta)
2. **Set up the webhook/API endpoint** (15 minutes)
3. **Update the app code** with your endpoints
4. **Deploy and test** data collection
5. **Start collecting beta feedback** with persistent storage!

**🎯 Ready to start collecting persistent data for your LUNTRA Beta launch!**