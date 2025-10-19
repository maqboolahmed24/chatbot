# NHC CRM System - Visual Flowcharts Collection

## About This Document

This document contains the **most important flowcharts** for understanding the NHC CRM system architecture. All diagrams are in **editable Mermaid.js format** - simply copy and paste into https://mermaid.live to view and edit.

---

## 1. MAIN SYSTEM ARCHITECTURE - 4 Phases Overview

This is the master diagram showing all 4 phases of the CRM system and how they connect:

```mermaid
graph TB
    Start([CRM System Start]) --> Core[Central CRM Database]
    
    Core --> Phase1[Phase 1: Awareness & Interest<br/>Top of Funnel]
    Core --> Phase2[Phase 2: Consideration & Lead Gen<br/>Middle of Funnel]
    Core --> Phase3[Phase 3: Nurturing & Sales<br/>Post-Lead Generation]
    Core --> Phase4[Phase 4: Post-Sale & Advocacy<br/>Customer Experience]
    
    Phase1 --> P1Touch{Touchpoints}
    P1Touch --> OOH[Offline Ads<br/>OOH/Airport/TV/Radio]
    P1Touch --> Sponsor[Sponsorships<br/>TV/Podcasts]
    P1Touch --> Social1[Social Media<br/>X/Instagram/Snapchat]
    
    Phase2 --> P2Touch{Touchpoints}
    P2Touch --> Landing[Landing Page<br/>Sakani Platform]
    P2Touch --> WebForm[Website Enquiry Form]
    P2Touch --> Events[Event Lead Capture<br/>Real Estate Expos]
    P2Touch --> SocialDM[Social Media DMs<br/>WhatsApp/Instagram/X]
    
    Phase3 --> P3Touch{Touchpoints}
    P3Touch --> Welcome[Automated Welcome<br/>SMS/WhatsApp]
    P3Touch --> Nurture[Personalized Nurture<br/>SMS/WhatsApp]
    P3Touch --> EventInv[Event Invitations]
    P3Touch --> SalesVis[Sales Follow-up<br/>Visibility]
    
    Phase4 --> P4Touch{Touchpoints}
    P4Touch --> CommWelcome[Welcome to Community<br/>SMS/WhatsApp]
    P4Touch --> NPS[Customer Satisfaction<br/>NPS Survey]
    P4Touch --> Referral[Referral Program<br/>Invitation]
    
    OOH --> Analytics[Analytics Engine]
    Sponsor --> Analytics
    Social1 --> Analytics
    Landing --> LeadDB[(Lead Database)]
    WebForm --> LeadDB
    Events --> LeadDB
    SocialDM --> LeadDB
    
    LeadDB --> SalesPipe[Sales Pipeline]
    SalesPipe --> Customer[(Customer Database)]
    
    Welcome --> Automation[Automation Workflows]
    Nurture --> Automation
    EventInv --> Automation
    CommWelcome --> Automation
    NPS --> Automation
    Referral --> Automation
    
    Analytics --> Reports[Reporting Dashboard]
    Automation --> Reports
    Customer --> Reports
    
    style Core fill:#2C5F7C,stroke:#1A3A4F,stroke-width:3px,color:#fff
    style LeadDB fill:#D4AF37,stroke:#8B7500,stroke-width:2px
    style Customer fill:#228B22,stroke:#006400,stroke-width:2px
    style Automation fill:#FF6B6B,stroke:#C92A2A,stroke-width:2px
    style Analytics fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px
```

---

## 2. DETAILED LEAD GENERATION FLOW

This shows exactly how leads enter the system from different sources:

```mermaid
flowchart TD
    Start([User Interaction]) --> Check{Interaction Type?}
    
    Check -->|Offline Ad| OOH[Offline Ad Exposure<br/>OOH/Airport/TV/Radio]
    Check -->|Sponsorship| Sponsor[Sponsorship Mention<br/>TV/Podcasts]
    Check -->|Social Media| Social[Social Media Engagement<br/>X/Instagram/Snapchat]
    Check -->|Landing Page| LP[Landing Page Visit<br/>Sakani Platform]
    Check -->|Website Form| WF[Website Enquiry Form]
    Check -->|Event| Event[Event Attendance<br/>Real Estate Expo]
    Check -->|Direct Message| DM[Social Media DM<br/>WhatsApp/Instagram/X]
    
    OOH --> CreateCamp1[Create Campaign Record<br/>with Unique URL/SMS Code]
    Sponsor --> CreateCamp2[Create Campaign Record<br/>with UTM-tagged URL]
    Social --> TrackEng[Track Engagement<br/>via Social Listening]
    
    CreateCamp1 --> TrackCall[Track Calls to<br/>920033499]
    CreateCamp2 --> TrackURL[Track Landing<br/>Page Visits]
    TrackEng --> TrackClick[Track Link Clicks<br/>with UTM Codes]
    
    TrackCall --> Indirect[No Direct Lead Entry<br/>Track Campaign Influence]
    TrackURL --> Indirect
    TrackClick --> Indirect
    
    LP --> Validate{Form Valid?}
    WF --> Validate
    
    Validate -->|No| Error[Show Error Message]
    Error --> LP
    
    Validate -->|Yes| CreateLead[AUTO: Create Lead Record]
    
    Event --> TabletForm[Staff Uses Tablet<br/>CRM-Integrated Form]
    TabletForm --> ManualLead[MANUAL: Create Lead Record<br/>with Event Attribution]
    
    DM --> SocialMgr[Social Media Manager<br/>Captures Info]
    SocialMgr --> ManualDM[MANUAL: Create Lead Record<br/>with DM Attribution]
    
    CreateLead --> PopulateData[Populate Lead Fields:<br/>- Name<br/>- Phone<br/>- Project of Interest<br/>- City]
    ManualLead --> PopulateData
    ManualDM --> PopulateData
    
    PopulateData --> Attribution[Set Attribution:<br/>- Source<br/>- Campaign<br/>- Medium<br/>- Timestamp]
    
    Attribution --> Trigger[TRIGGER:<br/>Automated Welcome Workflow]
    
    Trigger --> LeadCreated[(Lead Record<br/>Created in CRM)]
    
    Indirect --> Analytics[(Campaign Analytics<br/>Dashboard)]
    
    LeadCreated --> NextPhase[Proceed to<br/>Nurturing Phase]
    
    style CreateLead fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style ManualLead fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style ManualDM fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style LeadCreated fill:#2196F3,stroke:#1565C0,stroke-width:3px,color:#fff
    style Trigger fill:#E91E63,stroke:#880E4F,stroke-width:2px,color:#fff
```

---

## 3. LEAD SCORING ALGORITHM

This algorithm determines how hot/warm/cold each lead is:

```mermaid
flowchart TD
    Start([New Lead Created]) --> InitScore[Initialize Score = 0]
    
    InitScore --> CheckProject{Project of<br/>Interest Specified?}
    CheckProject -->|Yes| AddProject[+30 Points]
    CheckProject -->|No| CheckContact
    AddProject --> CheckContact
    
    CheckContact{Complete Contact<br/>Information?}
    CheckContact -->|Email + Phone| AddComplete[+20 Points]
    CheckContact -->|Phone Only| AddPhone[+10 Points]
    CheckContact -->|Email Only| AddEmail[+10 Points]
    AddComplete --> CheckCity
    AddPhone --> CheckCity
    AddEmail --> CheckCity
    
    CheckCity{City Matches<br/>Active Projects?}
    CheckCity -->|Yes| AddCity[+20 Points]
    CheckCity -->|No| CheckBudget
    AddCity --> CheckBudget
    
    CheckBudget{Budget Range<br/>Specified?}
    CheckBudget -->|Yes| AddBudget[+15 Points]
    CheckBudget -->|No| CheckCampaign
    AddBudget --> CheckCampaign
    
    CheckCampaign{Campaign<br/>Performance?}
    CheckCampaign -->|High Performing| AddCampHigh[+15 Points]
    CheckCampaign -->|Standard| AddCampStd[+7 Points]
    CheckCampaign -->|No Campaign| CheckSource
    AddCampHigh --> CheckSource
    AddCampStd --> CheckSource
    
    CheckSource{Lead Source<br/>Quality?}
    CheckSource -->|Event/Referral| AddSourceHigh[+10 Points]
    CheckSource -->|Landing Page| AddSourceMed[+5 Points]
    CheckSource -->|Social DM| AddSourceLow[+2 Points]
    AddSourceHigh --> CheckEngagement
    AddSourceMed --> CheckEngagement
    AddSourceLow --> CheckEngagement
    
    CheckEngagement{Prior<br/>Engagement?}
    CheckEngagement -->|High| AddEngHigh[+10 Points]
    CheckEngagement -->|Medium| AddEngMed[+5 Points]
    CheckEngagement -->|None| CalculateTotal
    AddEngHigh --> CalculateTotal
    AddEngMed --> CalculateTotal
    
    CalculateTotal[Calculate Total Score<br/>Max: 100]
    
    CalculateTotal --> Categorize{Score<br/>Category?}
    
    Categorize -->|80-100| Hot[HOT Lead<br/>Priority: Urgent<br/>SLA: 5 minutes]
    Categorize -->|60-79| Warm[WARM Lead<br/>Priority: High<br/>SLA: 30 minutes]
    Categorize -->|40-59| Cold[COLD Lead<br/>Priority: Standard<br/>SLA: 4 hours]
    Categorize -->|0-39| VCold[VERY COLD Lead<br/>Priority: Low<br/>SLA: 24 hours]
    
    Hot --> AssignRule1[Auto-assign to<br/>Top Sales Rep]
    Warm --> AssignRule2[Auto-assign to<br/>Available Rep]
    Cold --> AssignRule3[Add to<br/>Nurture Queue]
    VCold --> AssignRule4[Auto-nurture<br/>No immediate assignment]
    
    AssignRule1 --> Notify1[Send Instant<br/>Notification]
    AssignRule2 --> Notify2[Send Standard<br/>Notification]
    AssignRule3 --> Notify3[Daily Digest]
    AssignRule4 --> Notify4[No Notification]
    
    Notify1 --> End([Lead Scored<br/>& Routed])
    Notify2 --> End
    Notify3 --> End
    Notify4 --> End
    
    style Hot fill:#FF4444,stroke:#CC0000,stroke-width:3px,color:#fff
    style Warm fill:#FF9933,stroke:#CC6600,stroke-width:2px,color:#fff
    style Cold fill:#FFCC00,stroke:#CC9900,stroke-width:2px
    style VCold fill:#99CCFF,stroke:#6699CC,stroke-width:2px
```

---

## 4. DATA FLOW ARCHITECTURE

This shows how data moves through the entire system:

```mermaid
graph LR
    subgraph External Sources
        A1[Offline Ads<br/>OOH/TV/Radio] 
        A2[Social Media<br/>X/Instagram/Snapchat]
        A3[Sakani Landing Page]
        A4[NHC Website Forms]
        A5[Events/Expos]
        A6[Direct Messages]
    end
    
    subgraph Data Ingestion Layer
        B1[Campaign Tracker]
        B2[UTM Parameter Parser]
        B3[Form API Handler]
        B4[Event Capture App]
        B5[Social Integration API]
    end
    
    subgraph CRM Core Database
        C1[(Campaign Records)]
        C2[(Lead Records)]
        C3[(Contact Records)]
        C4[(Opportunity Records)]
        C5[(Customer Records)]
    end
    
    subgraph Processing Engine
        D1[Lead Scoring Engine]
        D2[Attribution Engine]
        D3[Segmentation Engine]
        D4[Automation Workflow Engine]
    end
    
    subgraph Output Systems
        E1[SMS Gateway]
        E2[WhatsApp Business API]
        E3[Sales Dashboard]
        E4[Analytics & Reports]
        E5[Marketing Dashboard]
    end
    
    A1 --> B1
    A2 --> B2
    A3 --> B3
    A4 --> B3
    A5 --> B4
    A6 --> B5
    
    B1 --> C1
    B2 --> C2
    B3 --> C2
    B4 --> C2
    B5 --> C2
    
    C1 --> D2
    C2 --> D1
    C2 --> D3
    C2 --> D2
    
    D1 --> C4
    D2 --> C4
    D3 --> D4
    C4 --> C5
    
    D4 --> E1
    D4 --> E2
    C4 --> E3
    C2 --> E4
    C1 --> E5
    C5 --> E4
    
    style C1 fill:#FFE5B4,stroke:#D4A574
    style C2 fill:#FFE5B4,stroke:#D4A574
    style C3 fill:#FFE5B4,stroke:#D4A574
    style C4 fill:#FFE5B4,stroke:#D4A574
    style C5 fill:#FFE5B4,stroke:#D4A574
```

---

## 5. SALES PIPELINE STAGES

The journey of a lead through the sales process:

```mermaid
flowchart LR
    New[New Lead<br/>Status: New] --> Contacted[First Contact Made<br/>Status: Contacted]
    Contacted --> Qualified[Lead Qualified<br/>Status: Qualified]
    Qualified --> OpptyCreated[Opportunity Created<br/>Status: Opportunity]
    OpptyCreated --> NeedsAnalysis[Needs Analysis<br/>Stage: Discovery]
    NeedsAnalysis --> Proposal[Proposal/Quote<br/>Stage: Proposal]
    Proposal --> Negotiation[Negotiation<br/>Stage: Negotiation]
    Negotiation --> Decision{Decision Point}
    
    Decision -->|Won| ClosedWon[Deal Closed-Won<br/>Status: Customer]
    Decision -->|Lost| ClosedLost[Deal Closed-Lost<br/>Status: Dead]
    Decision -->|Delayed| Nurture[Back to Nurture<br/>Status: Long-term]
    
    Qualified -->|Not Qualified| Disqualified[Disqualified<br/>Status: Dead]
    
    ClosedWon --> CustomerJourney[Customer Journey<br/>Phase 4]
    ClosedLost --> Analytics1[Loss Analysis]
    Disqualified --> Analytics2[Disqualification Tracking]
    Nurture --> AutomatedNurture[Automated Nurture<br/>Campaign]
    
    AutomatedNurture -.->|Re-engaged| Qualified
    
    style New fill:#E3F2FD,stroke:#1976D2,stroke-width:2px
    style Contacted fill:#FFF9C4,stroke:#F57F17,stroke-width:2px
    style Qualified fill:#C8E6C9,stroke:#388E3C,stroke-width:2px
    style OpptyCreated fill:#BBDEFB,stroke:#1565C0,stroke-width:2px
    style NeedsAnalysis fill:#B2DFDB,stroke:#00695C,stroke-width:2px
    style Proposal fill:#D1C4E9,stroke:#5E35B1,stroke-width:2px
    style Negotiation fill:#FFCCBC,stroke:#E64A19,stroke-width:2px
    style ClosedWon fill:#81C784,stroke:#2E7D32,stroke-width:3px,color:#fff
    style ClosedLost fill:#E57373,stroke:#C62828,stroke-width:2px,color:#fff
    style CustomerJourney fill:#4DB6AC,stroke:#00695C,stroke-width:3px,color:#fff
```

---

## 6. AUTOMATION WORKFLOW ENGINE

How automated messages and actions are triggered:

```mermaid
flowchart TD
    subgraph Trigger Events
        T1[New Lead Created]
        T2[Lead Score Changes]
        T3[Lead Inactive for X Days]
        T4[Deal Closed-Won]
        T5[3-6 Months Post Move-in]
        T6[NPS Score = 9 or 10]
    end
    
    subgraph Workflow Decision Engine
        WE[Workflow Engine]
    end
    
    subgraph Automated Actions
        A1[Send Welcome SMS/WhatsApp]
        A2[Add to Nurture Campaign]
        A3[Send Re-engagement Message]
        A4[Send Community Welcome]
        A5[Send NPS Survey]
        A6[Send Referral Invitation]
        A7[Update Lead Status]
        A8[Assign to Sales Rep]
        A9[Create Task for Sales]
    end
    
    subgraph Communication Channels
        CH1[SMS Gateway API]
        CH2[WhatsApp Business API]
    end
    
    subgraph Logging & Tracking
        L1[(Activity Timeline Log)]
        L2[(Campaign Performance DB)]
        L3[(Customer Interaction History)]
    end
    
    T1 --> WE
    T2 --> WE
    T3 --> WE
    T4 --> WE
    T5 --> WE
    T6 --> WE
    
    WE -->|New Lead| A1
    WE -->|Qualified Lead| A2
    WE -->|30 Days Inactive| A3
    WE -->|Closed-Won| A4
    WE -->|Post Move-in Timer| A5
    WE -->|High NPS| A6
    WE -->|Status Change| A7
    WE -->|Lead Score >70| A8
    WE -->|High Priority| A9
    
    A1 --> CH1
    A1 --> CH2
    A2 --> CH1
    A2 --> CH2
    A3 --> CH1
    A3 --> CH2
    A4 --> CH2
    A5 --> CH1
    A5 --> CH2
    A6 --> CH2
    
    CH1 --> L1
    CH2 --> L1
    A2 --> L2
    A4 --> L3
    A5 --> L3
    A6 --> L3
    
    style WE fill:#9C27B0,stroke:#6A1B9A,stroke-width:3px,color:#fff
    style CH1 fill:#00BCD4,stroke:#006064,stroke-width:2px,color:#fff
    style CH2 fill:#4CAF50,stroke:#1B5E20,stroke-width:2px,color:#fff
```

---

## 7. DATABASE ENTITY RELATIONSHIP DIAGRAM (SIMPLIFIED)

The core database structure:

```mermaid
erDiagram
    LEAD ||--o{ ACTIVITY : has
    LEAD ||--|| CONTACT : converts_to
    LEAD }o--|| CAMPAIGN : attributed_to
    LEAD }o--|| SOURCE : comes_from
    CONTACT ||--o{ OPPORTUNITY : has
    OPPORTUNITY ||--|| CUSTOMER : converts_to
    CUSTOMER ||--o{ NPS_SURVEY : receives
    CUSTOMER ||--o{ REFERRAL : makes
    REFERRAL }o--|| LEAD : creates
    
    LEAD {
        uuid lead_id PK
        string first_name
        string last_name
        string phone_number UK
        string email
        string city
        string project_of_interest
        uuid campaign_id FK
        string lead_source
        string lead_status
        int lead_score
        datetime created_date
    }
    
    CONTACT {
        uuid contact_id PK
        uuid lead_id FK
        string preferred_language
        string preferred_channel
        datetime last_contacted
    }
    
    CAMPAIGN {
        uuid campaign_id PK
        string campaign_name
        string campaign_type
        string channel
        date start_date
        date end_date
        decimal budget
    }
    
    ACTIVITY {
        uuid activity_id PK
        uuid lead_id FK
        string activity_type
        string channel
        datetime activity_date
        string status
    }
    
    OPPORTUNITY {
        uuid opportunity_id PK
        uuid contact_id FK
        string project_name
        string stage
        decimal deal_value
        date expected_close
    }
    
    CUSTOMER {
        uuid customer_id PK
        uuid opportunity_id FK
        date purchase_date
        date move_in_date
        string property_id
    }
    
    NPS_SURVEY {
        uuid survey_id PK
        uuid customer_id FK
        int nps_score
        text feedback
        datetime completed_at
    }
    
    SOURCE {
        uuid source_id PK
        string source_name
        string source_type
    }
    
    REFERRAL {
        uuid referral_id PK
        uuid customer_id FK
        uuid referred_lead_id FK
        string referral_code UK
        string status
        decimal reward_amount
    }
```

---

## 8. INTEGRATION ARCHITECTURE

How the CRM connects to external systems:

```mermaid
graph TB
    subgraph External Systems
        EXT1[Sakani Platform]
        EXT2[NHC Website]
        EXT3[Social Media APIs]
        EXT4[SMS Gateway]
        EXT5[WhatsApp Business API]
        EXT6[Event Platform]
        EXT7[Survey Platform]
        EXT8[Google Analytics]
    end
    
    subgraph API Gateway
        API[API Gateway<br/>REST/GraphQL]
    end
    
    subgraph CRM Core
        CRM[CRM Platform]
    end
    
    subgraph Integration Services
        INT1[Form Handler]
        INT2[Social Listener]
        INT3[Communication Service]
        INT4[Attribution Service]
        INT5[Webhook Handler]
        INT6[Data Sync]
    end
    
    subgraph Data Storage
        DB1[(Main Database)]
        DB2[(Analytics DB)]
        DB3[(File Storage)]
        DB4[(Cache - Redis)]
    end
    
    EXT1 --> API
    EXT2 --> API
    EXT3 --> API
    EXT4 --> API
    EXT5 --> API
    EXT6 --> API
    EXT7 --> API
    EXT8 --> API
    
    API --> INT1
    API --> INT2
    API --> INT3
    API --> INT4
    API --> INT5
    API --> INT6
    
    INT1 --> CRM
    INT2 --> CRM
    INT3 --> CRM
    INT4 --> CRM
    INT5 --> CRM
    INT6 --> CRM
    
    CRM --> DB1
    CRM --> DB2
    CRM --> DB3
    CRM --> DB4
    
    style API fill:#FF6B6B,stroke:#C92A2A,stroke-width:3px,color:#fff
    style CRM fill:#4ECDC4,stroke:#006064,stroke-width:4px,color:#fff
    style DB1 fill:#FFD93D,stroke:#F4A300,stroke-width:2px
```

---

## HOW TO USE THESE FLOWCHARTS

### Method 1: Mermaid Live Editor (Easiest)
1. Visit **https://mermaid.live**
2. Copy any diagram code above (between ```mermaid and ```)
3. Paste into the editor
4. Diagram renders instantly
5. Edit the text to modify the diagram
6. Export as PNG, SVG, or PDF

### Method 2: VS Code
1. Install extension: "Markdown Preview Mermaid Support"
2. Open this file in VS Code
3. Press `Ctrl+Shift+V` to preview
4. Diagrams render automatically

### Method 3: GitHub
- Commit this file to your repository
- Mermaid diagrams render automatically

### Method 4: Copy to Documentation
- Paste into Notion, Confluence, or Docusaurus
- Most modern tools support Mermaid natively

---

## EDITING TIPS

### Change Node Text
```
OldNode[Old Text] --> NewNode[New Text]
```

### Add New Connection
```
ExistingNode --> NewNode[New Node Name]
```

### Change Colors
```
style NodeName fill:#FF0000,stroke:#000,color:#fff
```

### Add Decision Point
```
A --> B{Question?}
B -->|Answer 1| C
B -->|Answer 2| D
```

---

## KEY TAKEAWAYS FOR IT TEAM

1. **4 Phases**: Awareness → Lead Gen → Nurturing → Advocacy
2. **Primary Entry Point**: Sakani Landing Page (automatic lead creation)
3. **Lead Scoring**: 0-100 score determines priority and SLA
4. **No Email**: Focus on SMS/WhatsApp for communication
5. **Attribution Critical**: Every lead must know its source
6. **Speed Matters**: Hot leads get 5-minute response SLA

---

**For complete technical specs and implementation details, see:**
- `nhc_crm_technical_specs.md` - Database schemas, APIs, code examples
- `nhc_crm_implementation_guide.md` - Timeline, testing, deployment
- `README.md` - Project overview and navigation

---

© 2025 National Housing Company (NHC) - Technical Documentation
