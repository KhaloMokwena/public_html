"""
Starting content for the site, taken from the ZuriKO content document.
Loaded with:  python manage.py seed_content
"""

# (category, title, description) - in the order they appear on the Services page.
SERVICES = [
    ("IT Services & Consulting", "Software Development", "Custom enterprise-grade software solutions built with Java and .NET."),
    ("IT Services & Consulting", "Web Development", "High-performance web portals, e-commerce, and PWA development."),
    ("IT Services & Consulting", "IT Support & Help Desk", "24/7 technical support and rapid incident resolution for business continuity."),
    ("IT Services & Consulting", "DevOps & Cloud", "Cloud migration, CI/CD pipeline automation, and infrastructure orchestration."),
    ("IT Services & Consulting", "Systems Integration", "Seamlessly connecting ERP, CRM, and legacy systems for efficiency."),
    ("IT Services & Consulting", "IT Strategy & Consulting", "Digital transformation roadmaps and long-term IT architecture planning."),
    ("IT Services & Consulting", "Managed Print Services", "Optimized print fleet management and secure document digitization."),
    ("IT Services & Consulting", "Cybersecurity", "Advanced IT security, vulnerability assessments, and threat monitoring."),
    ("IT Services & Consulting", "Data Analytics", "Business intelligence, big data processing, and custom reporting dashboards."),
    ("IT Services & Consulting", "Database Management", "Database design, optimization, and high-availability cluster management."),
    ("Media & Broadcasting", "Live Videography", "High-definition event coverage with multi-cam setups."),
    ("Media & Broadcasting", "Multi-Platform Streaming", "Real-time live streaming to YouTube, Facebook, LinkedIn, and private servers."),
    ("Media & Broadcasting", "Sound Engineering", "Professional audio mixing, mastering, and live sound reinforcement."),
    ("Media & Broadcasting", "Professional Photography", "Comprehensive photography for corporate, NGO, weddings, church, and private events."),
    ("Graphic Design & Print", "Brand Identity Design", "Logo design, corporate stationary, and full brand guideline creation."),
    ("Graphic Design & Print", "Print & Signage", "Professional print of banners, brochures, business cards, and wide-format signage."),
    ("Media & Broadcasting", "Content Strategy", "Targeted marketing campaigns and digital content planning."),
    ("Graphic Design & Print", "Corporate Media", "Annual reports, booklets, magazines, and digital publications."),
    ("Graphic Design & Print", "Heat Press & Apparel", "High-quality branded workwear, t-shirts, and custom apparel printing."),
    ("Media & Broadcasting", "Production Management", "Full-scale production oversight for large-scale corporate and public media events."),
    ("Construction & Civil Engineering", "Building Information Modeling (BIM)", "Detailed 3D architectural rendering, project simulation, and spatial structural coordination."),
    ("Construction & Civil Engineering", "Site Telemetry & Security", "Deployment of remote surveillance towers, access control gates, and site data setups."),
    ("Mining & Industrial", "SCADA Integration Pipelines", "Connecting supervisory plant machinery loops into centralized operational control centers."),
    ("Mining & Industrial", "Industrial Asset Tracking", "Real-time tracking solutions for high-value logistics, ore loads, and plant equipment."),
    ("Retail & E-Commerce", "Omnichannel Point-of-Sale (POS)", "High-speed unified billing software connecting in-store points to stock ledgers."),
    ("Retail & E-Commerce", "Automated Stock Fulfillment", "Warehouse pipeline sorting mechanisms matched directly to online orders."),
    ("Real Estate & Property", "Virtual Tour Production", "3D spatial mapping and 360-degree interactive video walk-through architectural arrays."),
    ("Real Estate & Property", "Property Management Infrastructure", "Cloud portal ecosystems processing lease tracking records, tenant compliance, and billing updates."),
    ("Education & E-Learning", "Learning Management Systems (LMS)", "Customized digital academies delivering live tracking rows, grading engines, and assignment uploads."),
    ("Education & E-Learning", "Interactive Classroom Systems", "Integration of hybrid streaming webcams, smartboard software, and distance learning pipelines."),
    ("Healthcare & Medical Technology", "Telehealth Portal Orchestration", "Secure, encrypted platforms supporting live virtual consultations and patient file records."),
    ("Healthcare & Medical Technology", "Medical Facility IT Layouts", "High-reliability networks engineered to transmit diagnostic images and manage critical records."),
    ("Hospitality & Tourism", "Hospitality Booking Engines", "Direct, secure channel engines synchronizing live room rates and travel schedules."),
    ("Hospitality & Tourism", "Tourism Media Campaigns", "Cinematic visual production highlighting South African venues across international digital spaces."),
]

_MARKET = "Market related / Based on experience"
_STIPEND = "Fixed monthly stipend"
_HYBRID = "Hybrid (Centurion based)"

# Listed in the order they appear on the Careers page.
JOBS = [
    dict(department="Information Technology", title="Senior Java Developer", level=f"Senior • {_MARKET}",
         scope="Architects high-concurrency enterprise engines, manages microservice pipelines, and ensures strict system stability, high thread safety, and ACID compliance across our core transaction billing and orchestration modules.",
         requirements="7+ years experience, Spring Boot, Microservices, Cloud Architecture."),
    dict(department="Media & Marketing", title="Media Production Lead", level=f"Intermediate / Senior • {_MARKET}",
         scope="Oversees end-to-end creative outputs, managing complex multi-camera live streaming rigs, setting up field sound engineering platforms, and directing post-production layouts using the Adobe Creative Cloud Suite.",
         requirements="Expertise in multi-cam live streaming, sound engineering, and Adobe Suite."),
    dict(department="Human Resources", title="HR & Payroll Administrator", level=f"Intermediate • {_MARKET}",
         scope="Manages day-to-day HR operations, maintains structured digital employee files, handles monthly payroll variations, and ensures total operational compliance with the Basic Conditions of Employment Act (BCEA).",
         requirements="Diploma or Certificate in HR + 3+ years of experience in HR/Payroll administrative capacity, BCEA compliance knowledge."),
    dict(department="Human Resources", title="Graduate HR Intern", level=f"Junior (Internship) • {_STIPEND}",
         scope="Assists with talent acquisition routing, handles candidate screening metrics, compiles physical onboarding packs, and coordinates structural interviews while undergoing active operational training.",
         requirements="Relevant Degree or National Diploma in Human Resources. No prior experience required. Must commit to a 6-month intensive training program."),
    dict(department="Marketing", title="Digital Marketing Specialist", level=f"Intermediate • {_MARKET}",
         scope="Develops, executes, and monitors conversion-driven search and social ad campaigns across Meta and Google, constructs semantic SEO keywords metadata layouts, and produces monthly digital performance audits.",
         requirements="Certification or Diploma in Marketing + 3+ years of experience running paid campaigns (Google Ads, Meta Ads) and SEO."),
    dict(department="Social Media", title="Social Media Coordinator", level=f"Junior (Internship) • {_STIPEND}",
         scope="Deploys weekly content calendars, tracks audience engagement tags, drafts visual social assets, and flags customer service feedback rows to relevant inside operators.",
         requirements="Recent Graduate with a Marketing, Public Relations, or Media studies qualification. Zero workplace experience required. Includes 6 months of practical training."),
    dict(department="Information Technology", title="IT Support Technician", level=f"Intermediate • {_MARKET}",
         scope="Maintains infrastructure stability, configures staff laptops, builds secure cloud user directory endpoints, maps local network switches, and resolves tier-1 and tier-2 hardware tickets rapidly.",
         requirements="CompTIA A+/Network+ or IT Diploma + 3+ years of desktop/network support experience."),
    dict(department="Information Technology", title="Junior QA Tester", level=f"Junior (Internship) • {_STIPEND}",
         scope="Executes testing scripts against newly developed features, maps precise replication paths for technical bugs, and documents edge cases under direct engineer mentorship.",
         requirements="Recent Graduate with an IT, Computer Science, or Information Systems qualification. No experience required. Includes 6 months of mentorship and training."),
    dict(department="Operations", title="Office Administrator", level=f"Entry Level • {_MARKET}",
         scope="Welcomes corporate guests, routes standard switchboard queries, manages physical stationery layouts, and handles courier coordination to preserve baseline workplace productivity.",
         requirements="Matric (Grade 12) only. No previous work experience required. Basic typing abilities and professional phone manner."),
    dict(department="Finance & Billing", title="Accounts Clerk", level=f"Intermediate • {_MARKET}",
         scope="Keeps ledger records accurate, maps supplier payment invoices, coordinates overdue cash collection balances, and balances internal corporate bank accounts using Sage or Xero.",
         requirements="Higher Certificate or National Diploma in Accounting + 3+ years of experience utilizing packages like Sage, Xero, or Pastel."),
    dict(department="Finance & Billing", title="Junior Billing Clerk", level=f"Junior (Internship) • {_STIPEND}",
         scope="Learns data-capturing workflows, processes recurring billing cycles against contracts, dispatches digital customer invoices, and investigates transactional calculation imbalances.",
         requirements="Finance, Commerce, or Accounting Graduate. No corporate experience necessary. Includes a 6-month guided internship."),
    dict(department="Sales & Business Development", title="Internal Sales & Client Liaison", level=f"Entry Level • {_MARKET}",
         scope="Responds directly to inbound digital product inquiries, qualifies baseline leads, enters tracking metrics inside CRM logs, and hands high-value prospects over to technical sales managers.",
         requirements="Matric (Grade 12) only. No previous work experience required. Seeking high-energy individuals with good verbal communication skills."),
    dict(department="Customer Support", title="Customer Success Consultant", level=f"Entry Level • {_MARKET}",
         scope="Owns customer troubleshooting queues, processes simple configuration queries via email and phone calls, and keeps customer satisfaction targets high through continuous client interactions.",
         requirements="Matric (Grade 12) only. No experience required. Ideal for a fast learner with natural problem-solving abilities."),
    dict(department="Supply Chain / Logistics", title="Procurement & Logistics Clerk", level=f"Intermediate • {_MARKET}",
         scope="Places recurring product replenishment inventory requests, maps shipping tracking lines with local freight logistics networks, and reviews delivery speeds to reduce operational lag.",
         requirements="Certificate or National Diploma in Supply Chain Management or Logistics + 3+ years of experience."),
]
for _job in JOBS:
    _job["location"] = _HYBRID

DIVISIONS = [
    dict(
        title="Enterprise Software Engineering & Architecture",
        subtitle="High-Concurrency Backend Processing, Distributed Services, and ACID-Compliant Structural Integrity",
        description=(
            "At the absolute core of ZuriKO Technologies lies our high-performance custom enterprise software division. "
            "We specialize in building reliable multi-tier systems, robust orchestration layers, and real-time transaction processing networks. "
            "Our engineering philosophy is strictly production-first, focusing intensely on thread safety, query execution optimizations, and absolute "
            "ACID (Atomicity, Consistency, Isolation, Durability) transactional compliance. We build large-scale corporate web backends and microservices "
            "frameworks utilizing the industry's most stable ecosystems: Java with Spring Boot and modern C# within the .NET Core runtime environment. "
            "Our systems are specifically designed to eliminate typical corporate operational bottlenecks like resource deadlock conditions, unexpected "
            "connection pooling drops, and memory leaks under sudden load spikes. By utilizing domain-driven design parameters, we cleanly modularize "
            "complex business operations into fault-tolerant distributed services protected by automated input-sanitization frameworks, secure "
            "event-driven message brokers, and enterprise-grade OAuth2 token management. We translate legacy, fragmented corporate databases into secure, "
            "highly scalable microservices frameworks built to handle high volume traffic fluidly."
        ),
        bullets=(
            "Multi-Threaded Concurrency Profiling and Race-Condition Elimination Engines\n"
            "High-Availability Billing Engines and Automated Financial Ledger Reconciliation Layers\n"
            "Fault-Tolerant Distributed Enterprise Orchestration via Camunda and Flowable BPMN Tools\n"
            "Strict Data Protection Boundary Safeguards aligned to POPIA Regulatory Standards"
        ),
        stats="Java & .NET Core | Ecosystem Focus\nMicroservices | Architecture Model\nACID Compliance | Data Integrity",
        comparison=(
            "Architectural Metric | Legacy Corporate Monoliths | ZuriKO Microservices Grid\n"
            "Concurrency Throughput | Thread-blocking / Serial Latency | Non-blocking / Reactive Async Threads\n"
            "Fault Domain Isolation | Single Error Cascades and Crashes Entire App | Isolated Containers / Self-Healing Routing\n"
            "Database Scaling Limits | Row Contention / Heavy Deadlocks | Distributed Read Replicas / Schema Partitioning"
        ),
    ),
    dict(
        title="High-Performance Web & Mobile Application Development",
        subtitle="Optimized Web Vitals, Progressive Web Apps (PWAs), and Secure Digital Gateways",
        description=(
            "ZuriKO Technologies crafts progressive, ultra-responsive web portals, high-conversion e-commerce hubs, and cross-platform mobile environments. "
            "We utilize decoupled frontend architectures matching modern JavaScript engineering standards alongside semantic HTML5 frameworks and clean, "
            "highly optimized CSS layout engines. Every interface we build undergoes meticulous front-end tuning to guarantee lightning-fast load speeds, "
            "even on constrained mobile networks across South Africa. We optimize for Core Web Vitals, aggressively minimizing Cumulative Layout Shifts (CLS), "
            "accelerating Largest Contentful Paint (LCP) speeds, and ensuring excellent accessibility metrics. Our teams develop full-featured Progressive "
            "Web Applications (PWAs) that run offline data caching systems naturally using secure local service workers. These applications connect with "
            "backend networks through highly secure API meshes defended against Cross-Site Scripting (XSS), SQL Injection, and Cross-Origin Resource Sharing "
            "(CORS) misconfigurations. Whether building secure tenant booking management applications, custom multi-tier client portals, or intensive "
            "corporate reporting dashboards, we deliver lightning-fast, high-security, and completely seamless end-user experiences."
        ),
        bullets=(
            "Decoupled Single-Page Architecture with Optimized Execution Lifecycles\n"
            "Automated Asset Compression Pipelines and Lazy-Loading Image Layouts\n"
            "State Preservation Mechanisms tracking user input across view switches\n"
            "Token-Based Authentication Networks using Encrypted Session Storage Profiles"
        ),
        stats="HTML5 / CSS / JS | Frontend Engine\nPWA Offline Caching | Mobile Access\nXSS / CORS Proof | Security Core",
        comparison=(
            "Performance Parameter | Standard Static Website Templates | ZuriKO Dynamic Applications\n"
            "Mobile Performance | Heavy DOM / High Latency Paint Overheads | Minimal Footprint / Service Worker Accelerated\n"
            "State Retention | Page Refresh Resets Form Entries completely | Asynchronous Memory Preserves User State\n"
            "API Integration | Rigid, Monolithic Hardcoded Data Feeds | Dynamic Fetch Layer parsing multi-source endpoints"
        ),
    ),
    dict(
        title="Elite Brand Strategy & Visual Identity Design",
        subtitle="Vector Graphic Engineering, Corporate Styling Standards, and Brand Positioning",
        description=(
            "A company's operational capability must be immediately reflected in its visual presentation. The ZuriKO Creative Studio uncovers your "
            "organization's core strengths to translate them into high-impact visual design systems that build immediate consumer trust. We build complete "
            "corporate brand assets from the ground up, engineering infinitely scalable vector logos, business stationery layouts, professional pitch "
            "presentations, and detailed corporate brand manuals. These style guides define mandatory typography hierarchies, precise geometric spacing grids, "
            "exact color profile references (Pantone, CMYK, RGB, Hex layout models), and strict clear-space boundaries. This precise attention to detail "
            "ensures your company maintains absolute aesthetic consistency across all print materials, corporate signs, digital platforms, and advertising "
            "campaigns. We transform vague corporate ideas into clear, bold, and modern visual identities that establish clear market leadership."
        ),
        bullets=(
            "Infinite Vector Scaling preserving absolute geometry across displays\n"
            "Corporate Stationery Templates customized for professional documentation layouts\n"
            "Mandatory Typographical Rules defining scale and line height boundaries\n"
            "Distinct Palette Maps structuring exact digital and offset printing profiles"
        ),
        stats="Scalable Vectors | Design Format\nStyle Books | Consistency Tool\nPantone / CMYK | Color Models",
        comparison=(
            "Visual Asset Criteria | Amateur Non-Standard Graphics | ZuriKO Structural Guidelines\n"
            "Resolution Behavior | Raster Images blur and distort when magnified | Vector Mathematics maintain clean crisp edges\n"
            "Color Representation | Shifting tones between screens and print sets | Locked Pantone channels match physical proofs\n"
            "Structural Identity | Inconsistent font usage across corporate layouts | Locked Typography Matrices force consistency"
        ),
    ),
    dict(
        title="Broadcast Media, HD Videography & Sound Engineering",
        subtitle="Multi-Camera Production Layouts, Live Broadcast Networks, and Studio Audio Mastering",
        description=(
            "Our Broadcast Media and Production division coordinates high-definition corporate video documentation, dynamic live assemblies, large-scale "
            "event captures, and custom content pipelines. We configure advanced on-site production layouts using multi-camera systems matching Blackmagic "
            "Design or Sony Cinema standards to film in pristine 4K resolution with professional color depth. We establish complete studio lighting profiles "
            "using high-CRI LED arrays and 3-point active lighting setups to ensure perfect visual clarity in any venue environment. For live streaming setups, "
            "we run specialized mobile live-broadcast hardware encoding systems to stream multi-input video feeds, informational title overlays, and remote "
            "presenter feeds to YouTube, LinkedIn, and private servers simultaneously. To eliminate local network dropouts, we deploy cellular network bonding "
            "rigs that combine multiple cellular networks (MTN, Vodacom, Telkom) with local fiber channels into a single ultra-stable upload link, guaranteeing "
            "rock-solid stream reliability. Our audio engineering team ensures completely clear sound by using premium wireless lapel setups, dynamic podium "
            "microphones, and digital mixing systems to eliminate background noise, balance channels, and output broadcast-ready audio."
        ),
        bullets=(
            "Multi-Channel Live Stream Aggregators broadcasting to parallel end-points\n"
            "Industrial Cellular Bonding modules stabilizing fluctuating remote uplinks\n"
            "Acoustic Calibration Routines eliminating phase cancellation and environment echo\n"
            "Post-Production Color Grading utilizing high dynamic range (HDR) profiles"
        ),
        stats="4K Multi-Cam | Video Standards\nLink Bonding | Stream Network\nLoudness Matched | Audio Profile",
        comparison=(
            "Media Metric | Standard Consumer Video Recording | ZuriKO Broadcast Staging\n"
            "Stream Stability | Single router dropouts cause buffering issues | Bonded Network Backends handle path failures seamlessly\n"
            "Audio Resolution | Imbalanced signals capture ambient echo artifacts | Active Spectral Filtering outputs crisp speech clarity\n"
            "Visual Control | Flat automatic color balances lose target details | Custom HDR Cine-LUT grading creates deep definition"
        ),
    ),
    dict(
        title="Industrial Wide-Format Printing & Signage",
        subtitle="High-DPI Matrix Layouts, Weatherproof Vinyl Production, and Corporate Apparel",
        description=(
            "Our production facility bridges digital design and physical merchandise using advanced, high-precision industrial printing machinery. We process "
            "graphic designs onto diverse physical substrates with absolute sharpness and true color fidelity. Our production scope spans promotional pull-up "
            "banners, high-quality information brochures, business cards, and wide-format outdoor storefront signage. Our print specialists carefully monitor "
            "dots-per-inch (DPI benchmarks), manage bleed lines, and track precise vector cut contours for custom vinyl applications. We use premium, "
            "weather-resistant UV inks and industrial-grade protective coatings, ensuring your outdoor signs, custom vehicle wraps, and event banners retain "
            "deep, vibrant color tones and resist fading under harsh South African sun exposure. Concurrently, our apparel division transfers corporate "
            "branding onto rugged workwear and premium promotional clothing using automated direct-to-film (DTF) printing, screen printing, and high-density "
            "embroidery, using precise heat-curing to ensure your branded gear lasts through tough daily use."
        ),
        bullets=(
            "Wide-Format Plotters processing multi-meter industrial signage assets\n"
            "Lamination Frameworks sealing vinyl layers against severe scratching risks\n"
            "Precision Automated Plotting executing complex vector structural contours\n"
            "High-Density Thread Embroidery systems reproducing fine brand detail lines"
        ),
        stats="High-DPI Matrix | Print Quality\nWeatherproof UV | Ink Tech\nDTF / Embroidery | Apparel Finish",
        comparison=(
            "Merchandise Factor | Low-Tier Desk Print Outs | ZuriKO Industrial Production\n"
            "Climate Lifespan | Colors quickly blur and wash away under rain exposure | UV Stabilized Inks maintain integrity under UV rays\n"
            "Color Alignment | Uncalibrated heads produce mismatched muddy profiles | Strict Pre-Flight RIP engines balance CMYK values\n"
            "Apparel Endurance | Branded logos quickly flake and peel when laundered | Industrial Heat Fusion cures prints into the fabric"
        ),
    ),
    dict(
        title="Industrial Automation & Specialized Sector Operations",
        subtitle="SCADA Automation Pipelines, Telemetry Networks, and Connected Logistics Systems",
        description=(
            "Extending beyond standard software applications, ZuriKO Technologies engineers automated systems for the mining, construction, and industrial "
            "sectors. Our automation division integrates physical manufacturing machinery and factory sensors directly into centralized Supervisory Control "
            "and Data Acquisition (SCADA) systems. We write custom data extraction connections for industrial programmable logic controllers (PLCs), set up "
            "secure data transmission links, and build interactive dashboards for plant operators to track operational safety, system pressure changes, and "
            "throughput capacity in real time. For logistics and mining operations, we deploy rugged Industrial Internet of Things (IoT) hardware and "
            "telemetry sensors to track high-value transport fleets and conveyor machinery. These field nodes continuously monitor GPS location tracking, "
            "fuel usage patterns, system vibrations, and operating runtime hours. In the civil construction sector, we process standard architectural data "
            "into immersive 3D Building Information Modeling (BIM) files to resolve design conflicts before construction begins, while deploying standalone "
            "solar-powered surveillance towers and biometric access gates to secure remote project sites."
        ),
        bullets=(
            "Supervisory Data Collection via Modbus and OPC-UA Industrial Link Protocols\n"
            "Rugged Multi-Sensor Fleet Integration logging vibration and thermal telemetry\n"
            "Conflict Resolution Engineering isolating spatial clashes inside structural blueprints\n"
            "Solar-Powered Perimeter Remote Surveillance Hubs running edge processing"
        ),
        stats="SCADA / PLC | Automation Core\nIoT Mesh Network | Telemetry\n4D BIM Modeling | Civil Integration",
        comparison=(
            "Operational Metric | Manual Log Sheet Monitoring | ZuriKO Automated Telemetry\n"
            "Data Access Speeds | Retrospective tracking blocks operational overview | Sub-Second Event Triggers capture machine failures instantly\n"
            "Asset Visibility | Fragmented checkpoints hide real driver fuel leaks | Continuous Data Ingestion tracks exact tank variances\n"
            "Blueprint Safety | Field clashing maps force sudden costly modifications | Pre-Execution Spatial BIM maps eliminate structure errors"
        ),
    ),
]

# The content document lists these three questions without answers. The answers below are drafted
# only from claims already made elsewhere in the document (no turnaround times or guarantees were
# invented) - review and edit them in /manage/.
FAQS = [
    (
        "How does ZuriKO Technologies guarantee software transactional safety under heavy enterprise loads?",
        "Our engineering approach is production-first. We design around thread safety, query execution optimization and full ACID "
        "(Atomicity, Consistency, Isolation, Durability) compliance, and we build systems to avoid resource deadlocks, unexpected connection "
        "pooling drops and memory leaks under sudden load spikes. Complex business operations are modularized into fault-tolerant distributed "
        "services protected by automated input sanitization, secure event-driven message brokers and enterprise-grade OAuth2 token management.",
    ),
    (
        "What standard delivery turnarounds exist for wide-format print and custom signage assets?",
        "Turnaround depends on the size, material and finishing of the job, for example vinyl signage, banners, vehicle wraps or apparel. "
        "Send us your artwork, quantities and deadline through the Contact page and we will confirm a delivery timeline for your order.",
    ),
    (
        "Can your media division capture and stream live broadcasts from remote locations lacking fiber lines?",
        "Our broadcast team uses cellular network bonding rigs that combine multiple cellular networks (MTN, Vodacom, Telkom), together with "
        "local fiber where it is available, into a single upload link, and streams multi-camera feeds to YouTube, LinkedIn and private servers. "
        "Contact us with your venue details and we will confirm the right setup for your location.",
    ),
]
