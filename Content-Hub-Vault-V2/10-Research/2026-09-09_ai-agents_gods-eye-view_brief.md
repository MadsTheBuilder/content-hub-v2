---
date: 2026-09-09
niche: AI agents
repos_researched: 1
primary_sources_found: 1
notebook_ids: [48fc1df1-fd83-478d-bca4-2316061bbef1]
---

# Research Brief — AI agents
*2026-09-09 — 1 repos, each in its own notebook*

## bilawalsidhu-gods-eye-view
Source: https://github.com/bilawalsidhu/gods-eye-view  
notebook_id: 48fc1df1-fd83-478d-bca4-2316061bbef1  

[Synthesis failed]

## Sources

- **Architectural Analysis of the God's Eye View Spatial Intelligence Platform**
- **DATA_SOURCES.md - bilawalsidhu/gods-eye-view - GitHub**
- **GitHub - bilawalsidhu/gods-eye-view: A spy satellite simulator in your browser, except the data is real. Live open source spatial intelligence on a photorealistic 3D globe.**
- **GitHub - bilawalsidhu/gods-eye-view: A spy satellite simulator in your browser, except the data is real. Live open source spatial intelligence on a photorealistic 3D globe. · GitHub**
- **God's Eye View Release and Smart Work Zones with AADT Exposure - Cesium Community**
- **God's Eye View: Open-Source Spy-Satellite Simulator You Can Talk To - explainx.ai**
- **What is God's Eye View? - Dictionary - explainx.ai**
- **gods-eye-view — A spy satellite simulator in your browser, except the data is real. Live open source spatial intelligence on a photorealistic 3D globe. | Kitploit**
- **gods-eye-view/CONTRIBUTING.md at main - GitHub**
- **gods-eye-view/README.md at main - GitHub**
- **gods-eye-view: Real-time global intelligence on a 3D globe, no - Open Source Alternatives**
- **https://raw.githubusercontent.com/bilawalsidhu/gods-eye-view/main/README.md**


## Raw Findings

<details><summary>Expand for full Q&A and angle battery</summary>

### Research Questions

**What live data layers are included in the 3D globe?**

# Technical Briefing Document: Live Data Layers & Spatial Signal Fusion in *God's Eye View*

**Platform:** `bilawalsidhu/gods-eye-view`  
**License:** MIT License (Source Code) with per-provider third-party data restrictions [1-4].  
**Core Architecture:** Browser-native WebGL spatial intelligence console built with vanilla JavaScript, CesiumJS, and Vite, featuring local-first proxy execution and optional OpenAI Realtime voice control [5-8].

---

## Executive Summary

The **God's Eye View** platform fuses public open-source intelligence (OSINT) signals—spanning aviation transponders, maritime beacons, orbital mechanics, seismographs, environmental sensors, municipal CCTV networks, and telecommunications infrastructure—into a unified 3D coordinate space [1, 5, 9]. Designed as a local-first alternative to proprietary geospatial suites, the platform executes directly in client browsers without heavy single-page web frameworks [5-7].

> *"Half the magic is that it looks like a forbidden cockpit. The other half is that every line of code is inspectable."* [10-12]

The application integrates **thirteen data layers**, eleven of which feature a keyless default deployment pathway that requires no user accounts or paid subscriptions [9, 13-15].

---

## Master Inventory of Data Layers & Basemaps

| Ingestion Layer | Data Provider Feed | Authentication / Key Status | Ingestion & Update Pattern | Computational Engine & Client Behavior |
| :--- | :--- | :--- | :--- | :--- |
| **Commercial Flights** | OpenSky Network (`adsb.lol` fallback) | **Keyless (🟢)** *(Optional OAuth key increases credits)* [9, 13, 16] | Polling: 15–30s [9] | Renders 11,000+ live aircraft; interpolates telemetry one step behind real time using dead reckoning to eliminate jitter [9, 13, 17]. |
| **Military Aviation** | `adsb.lol` API | **Keyless (🟢)** [9, 13, 18] | Polling: 15–30s [9] | Highlights military transponders in amber with tactical glyphs; silently backfills ~24 hours of real trace history as stacked 3D loops [9, 19, 20]. |
| **Maritime Shipping** | `AISStream.io` | **Free API Key (🟡)** [9, 13, 21] | WebSocket Live Stream [9] | Streams real-time NMEA payloads directly to client layers; tracks commercial vessels, tankers, and cargo ships globally [9, 13, 19]. |
| **Orbital Satellites** | CelesTrak TLE Catalog | **Keyless (🟢)** [9, 13, 18] | Disk-Cached TLE Catalog [9] | Tracks an 838+ object catalog using SGP4 orbital propagation aligned to Greenwich Mean Sidereal Time (GMST); includes a "DENSE" toggle for the Starlink constellation [9, 13, 17, 22]. |
| **Seismic Activity** | USGS Earthquake Catalog | **Keyless (🟢)** [9, 13, 23] | Polling: 5 min [9] | Renders global earthquake events recorded over the trailing 24 hours [9, 13]. |
| **Active Wildfires** | NASA FIRMS (VIIRS / MODIS) | **Free API Key (🟡)** [9, 13, 24] | Polling: 30 min (Trailing 24h) [9, 24] | Merges NOAA-20, NOAA-21, and Suomi-NPP thermal anomaly vectors with fail-soft handling if keys are omitted [9, 24]. |
| **CCTV Traffic Mesh** | City Open Data APIs (Austin, Caltrans, TfL) | **Keyless (🟢)** *(Optional TfL key raises rate limit)* [9, 13, 25] | Live Frame Pull [9] | Projects ~800 public cameras directly onto 3D city structures with interactive drag-and-drop gizmos to calibrate estimated camera poses and viewsheds [9, 13, 26]. |
| **Simulated & Live Traffic** | OpenStreetMap (roads) + TomTom Traffic API | **Keyless Simulation (🟢)** / **Free Key (🟡)** [13, 27, 28] | Real-time procedural / Vector tiles [13, 28] | Simulates vehicle movement on OSM road geometries; optional TomTom API key injects live flow speeds and congestion color ramps below 8 km camera altitude [10, 13, 28]. |
| **Global Radio** | Radio-Browser API | **Keyless (🟢)** [9, 13, 29] | Dynamic Fetch [9] | Geolocates up to 750 internet radio stations; includes an analog tuner needle that flies the camera to the broadcaster's location upon selection [9, 13, 19]. |
| **Bikeshare Networks** | GBFS Feeds (Austin BCycle, Lyft) | **Keyless (🟢)** [9, 13, 30] | Polling: 5 min [9] | Tracks real-time dock availability and micro-mobility fleet counts while monitoring payload size to prevent buffer overflow [9, 13]. |
| **Space Missions** | Launch Library 2 (The Space Devs) | **Keyless (🟢)** *(Optional token raises allowance)* [9, 13, 25] | Polling: 15 min [9, 25] | Maps active launchpad coordinates and rolling 30-day launch metadata; scrubbable launch ascent replays (0.25×–4×) are explicitly labeled `RECONSTRUCTED ESTIMATE` [9, 13, 19, 25]. |
| **Mapped Installations** | OpenStreetMap Overpass API | **Keyless (🟢)** [13, 27, 28] | Viewport-bounded query [13, 28] | Extracts military site boundaries within a maximum 10° viewport; explicitly labeled as incomplete community mapping context [13, 28]. |
| **Datacenters (Static)** | Bundled OpenStreetMap Snapshot | **Built-in / Local** [9, 31] | Static File [9] | Renders geographic coordinates and metadata for 4,351 global datacenters (ODbL 1.0) [9, 31]. |
| **Dams & Reservoirs (Static)** | Bundled OpenInfraMap / OSM Snapshot | **Built-in / Local** [9, 31] | Static File [9] | Renders spatial locations for 704 major global dams and reservoirs (ODbL 1.0) [9, 31]. |
| **Submarine Fiber Cables (Static)** | Bundled TeleGeography Database | **Built-in / Local** [9, 31] | Static File [9] | Renders geometries for 712 transoceanic submarine fiber-optic cables and 1,917 landing points (CC BY-NC-SA 3.0 NonCommercial) [9, 31, 32]. |

---

## Operational Domain Analysis

### 1. Aviation & Aerospace Intelligence
* **Commercial Aviation:** Ingests live state vectors from the OpenSky Network REST API [9, 16]. When OpenSky encounters outages or credit limits, the local server proxy falls back to a capped 250 nautical-mile point snapshot from `api.adsb.lol` [18, 25]. To ensure fluid animation despite 15–30 second API polling windows, the client engine renders telemetry one interval behind real time and applies dead-reckoning extrapolation [9, 17]. Selecting an aircraft opens a **250-kilometer roster** of surrounding entities and enables **Cockpit Mode**, which fixes the camera to the airframe, aligns orientation via vertical datum calculations, and renders real local weather effects or volumetric clouds via Open-Meteo observations [17, 22, 28, 33-35].
* **Military Aviation:** Filtered through `adsb.lol` ADS-B streams, military aircraft are rendered in amber tactical glyphs [9, 36]. Selecting a military contact backfills its prior ~24-hour trace history, resolving flight patterns into stacked 3D loop lines above the terrain [19, 20].
* **Space Missions:** Driven by Launch Library 2, this layer tracks spaceport launchpads, payloads, rocket stages, and recovery statuses across a rolling 30-day window [9, 13, 25]. Launch ascent trajectories can be replayed at variable playback speeds (0.25× to 4×) [19, 20].

### 2. Maritime & Nautical Tracking
* **Live Vessel Traffic:** Powered by a live WebSocket proxy connection to `AISStream.io`, the platform parses raw NMEA transponder payloads broadcast by ships worldwide [9, 37]. The system models wake trails, surfaces vessel draft/destination metadata, and allows one-click camera handoffs from a tracked vessel to the nearest public CCTV camera [19, 38].

### 3. Orbital Mechanics & Satellite Constellations
* **Satellite Tracking:** Uses disk-cached Two-Line Element (TLE) sets from CelesTrak [9]. Position propagation is executed client-side using the Simplified General Perturbations (SGP4) model [17, 22]. Orbital paths are synchronized with Earth's rotation via Greenwich Mean Sidereal Time (GMST) calculations, preventing visual drift or orbit ring jitter [17, 22]. The system tracks ~840 satellites (color-coded by mission class) and includes a dedicated "DENSE" toggle to render the complete Starlink constellation shell [9, 13].

### 4. Environmental & Geothermal Monitoring
* **Seismic Activity:** Polls the USGS Earthquake Catalog every 5 minutes to plot seismic events over the trailing 24 hours, displaying magnitude, depth, and epicenter coordinates [9, 13].
* **Active Wildfires:** Ingests NASA FIRMS Near Real-Time (NRT) thermal anomaly data from MODIS and VIIRS sensors (NOAA-20, NOAA-21, Suomi-NPP) [9, 24]. Active thermal hotspots are plotted on the 3D globe; selecting a fire allows the analyst to measure thermal intensity and jump to adjacent ground cameras [13, 19].

### 5. Municipal Infrastructure, CCTV Mesh & Mobility
* **3D CCTV Projection & Viewsheds:** Ingests public camera catalogs and live frame URLs from municipal feeds (City of Austin, Caltrans in California, and Transport for London) [9, 30, 39]. Rather than displaying flat 2D video embeds, the platform projects camera frames directly onto 3D building geometry [5, 9, 40]. In "VIEWSHED" mode, the engine draws calculated frustum volumes showing camera coverage and blind spots [26, 40]. Users can manually fine-tune estimated camera headings and pitch using an interactive drag-and-drop 3D gizmo [13, 26].
* **Roadway Traffic:** Keyless installations run procedural vehicle simulation along OpenStreetMap road networks using aggregate location data [10, 13]. Integrating a free TomTom API key upgrades the layer to fetch live traffic flow vector tiles, painting real-time rush-hour congestion speeds directly onto city streets at camera altitudes below ~8 km [13, 28].
* **Bikeshare Networks:** Queries General Bikeshare Feed Specification (GBFS) endpoints (e.g., Austin BCycle) every 5 minutes, displaying dock locations and micro-mobility counts [9, 13, 30].

### 6. Global Radio & Infrastructure Datasets
* **Geolocated Radio:** Integrates the Radio-Browser directory, mapping up to 750 geolocated internet radio streams [9, 13]. Includes an interactive analog tuner control; dragging the needle snaps to active stations and automatically flies the 3D globe to the station's broadcast origin [13, 19, 25].
* **Bundled Static Infrastructure:** Shipped locally in `src/data/local_data/` to provide offline situational context without API dependencies [9, 31, 41]:
  * **Datacenters:** 4,351 global datacenter facility coordinates (ODbL 1.0) [9, 31].
  * **Dams & Reservoirs:** 704 major dam structures (ODbL 1.0) [9, 31].
  * **Submarine Cables:** 712 transoceanic fiber-optic cable routes and 1,917 landing points from TeleGeography (CC BY-NC-SA 3.0) [9, 31, 32].

---

## Basemap & 3D Terrain Hierarchy (The Basemap Ladder)

The rendering pipeline relies on CesiumJS and manages terrain elevation, vertical datums, and 3D photogrammetry through a four-tiered basemap structure [22, 42, 43]:

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Level 4 (Premium / Direct 3D): Google Photorealistic 3D Tiles           │
│ • Paid/Metered Google Key • 3D Photogrammetry Mesh • Place Search        │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │ (Downgrade / Alternative)
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ Level 3 (Personal 3D): Cesium ion Token + Google 3D / Bing Maps          │
│ • Free Cesium ion Key • Global Terrain Mesh • High-Res Satellite Stacks  │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │ (Default Fallback)
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ Level 2 (Standard Sat / Keyless Default): Esri World Imagery Basemap     │
│ • No API Key Required • Flat Ellipsoid / Re:Earth Keyless Terrain        │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │ (Network Outage Fallback)
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ Level 1 (Fallback Vector): OpenStreetMap (OSM) Tiles                     │
│ • No API Key Required • 2D Vector Basemap                                │
└──────────────────────────────────────────────────────────────────────────┘
```

1. **Level 1 (Fallback Vector):** OpenStreetMap 2D vector tiles used as an automatic network fallback if Esri servers are unreachable [43, 44].
2. **Level 2 (Standard Satellite):** Esri World Imagery satellite basemap paired with keyless terrain via Re:Earth / Mapterhorn quantized-mesh providers [28, 43, 44]. This serves as the default out-of-the-box landing state [43-45].
3. **Level 3 (Personal 3D):** Activated via a free Cesium ion token, rendering global 3D terrain meshes and Google Photorealistic 3D Tiles for eligible personal/non-commercial use [43, 44].
4. **Level 4 (Premium / Direct 3D):** Uses a direct Google Maps API Key (`Map Tiles API`) to stream direct Google Photorealistic 3D Tiles and enable in-app Google Place Search [16, 43, 44].

---

## Data Integrity, Live vs. Simulated Disclaimers & Ethical Boundaries

The project's architectural policy enforces clear visual labeling to distinguish verified live telemetry from modeled approximations, while maintaining strict ethical boundaries regarding individual privacy [37, 46]:

> *"Most feeds are live or regularly refreshed. Traffic is simulated along real roads using aggregate location data. CCTV camera poses and rocket launch trajectories are coarse estimates."* [10, 47-49]

> *"This project models events, assets, infrastructure, and systems — aircraft, vessels, satellites, fires, cameras, cities. It does not build features for named-person search, face recognition, or tracking individuals, and pull requests that cross that line won't be merged. People are not a query type here."* [37, 50-53]

> *"God's Eye View is an exploratory visualization of public and third-party data. Data may be delayed, incomplete, modeled, inferred, or wrong. Do not use it for flight or maritime navigation, emergency response, medical or health decisions, investment decisions, or other safety-critical or operational purposes."* [54-58]

---

💡 *Would you like to explore how to extend this platform by developing a custom data layer module, or shall we examine the local server proxy security configuration for brokering API keys?*

**Follow-up: Keyless Layer Count and the Two Key-Gated Layers**

The two live data layers that require API keys are **Live Vessels** (Maritime Shipping) and **Active Fires** (Active Wildfires) [1-3]:

1. **Live Vessels (Maritime Shipping)**
   * **Gating Provider:** **AISStream.io** [1-4].
   * **What to Obtain:** A free API key (`AISSTREAM_API_KEY`) obtained by completing a **free signup** at `aisstream.io` [3, 5-7].

2. **Active Fires (Active Wildfires)**
   * **Gating Provider:** **NASA FIRMS** (Fire Information for Resource Management System) [1-3, 8].
   * **What to Obtain:** A free API key (`FIRMS_MAP_KEY` / `MAP_KEY`) obtained directly from `firms.modaps.eosdis.nasa.gov/api/map_key/` [3, 5, 7, 8].

*(Note: Other optional keys exist to enhance existing layers—such as a **TomTom** key to upgrade simulated traffic to live flow speeds [2, 3] or an **OpenSky** / **Launch Library 2** credential to increase polling allowances [9, 10]—but Live Vessels and Active Fires are the two data layers requiring an API key to display their respective feeds [1-3].)*

💡 *Would you like to review how these API keys are stored locally (e.g., in `.env` files or the macOS Keychain) and handled securely by the local server proxy?*

**Follow-up: Dead Reckoning Interpolation and the 11,000+ Aircraft Figure**

Regarding the flight tracking layer in *God's Eye View*:

### Aircraft Count (11,000+)
* The source documents state that the Live Flights layer renders **"11,000+ live aircraft"** via the OpenSky Network and `adsb.lol` feeds [1-3].
* **The sources do not specify whether this figure is a measured benchmark or a provider feed ceiling**; it is presented directly in the data tables as the baseline live entity count delivered by the feed [1, 2].

---

### Dead Reckoning & Interpolation Method
* **Update / Polling Window:** Live telemetry feeds arrive on a **15–30 second polling interval** [1, 4].
* **Time Offset:** To create smooth motion from choppy API updates, the rendering engine runs **one interval (step) behind real time** [1, 4].
* **Interpolation & Dead Reckoning:** The platform **interpolates between known coordinate fixes** and uses **dead reckoning** to extrapolate aircraft positions and fill tracking gaps between updates [1, 4].

---

💡 *Would you like to explore how aircraft headings and billboard orientations are projected in screen-space to prevent icon distortion during camera rotation?*

**Follow-up: Provenance of the 11,000+ Aircraft Figure**

The documentation **does not record an explicit numeric cap** on the total number of aircraft drawn simultaneously on the globe, nor does it define a measured GPU/entity rendering benchmark [1-3]. 

However, the sources detail specific **culling, LOD, and API request controls** that manage the layer's performance:

### 1. Recorded Benchmarks
* **Cold-Start Benchmark:** A point-in-time capture on an Apple M5 / Chrome setup measured a **median 1.86-second cold start** to initialize and settle the globe [2].
* **CI Allocation Gates:** Automated test suites execute Node.js allocation microbenchmarks during builds to catch memory leaks, though these measure runtime execution rather than WebGL frame rendering [1].

### 2. Culling & Level of Detail (LOD)
* **Horizon Culling:** Per-frame screen-space projections calculated in `src/data/iconOrientation.js` perform **horizon culling**, suppressing entities that fall outside the active viewport or behind the Earth's curvature [4-6].
* **Glyph-to-3D Dynamic LOD:** At high altitudes, aircraft render as lightweight 2D billboard glyphs [7, 8]. As the camera closes in, the system dynamically swaps the glyph for an optimized 3D airframe model (`.glb`) with reduced polycount, simplified geometry, and 256px WebP textures [7-9].

### 3. Feed Ingestion Caps & Request Budgets
* **OpenSky Credit Governor:** Server-side polling is throttled by an **OpenSky credit governor** to prevent rate-limit bans [3].
* **Spatial Fallback Bounding:** If OpenSky drops offline, the `adsb.lol` fallback mechanism restricts queries to a **capped 250 nautical-mile point snapshot** centered around the camera's current ground subpoint, avoiding the overhead of drawing worldwide fallback traffic [10].

---

💡 *Would you like to review how the 3D aircraft models in `public/models/` are vertex-baked and optimized to avoid Draco decoding bottlenecks during close-up camera handoffs?*

**Follow-up: Interpolation Method Between Fixes**

The provided project sources **do not contain the low-level mathematical or algorithmic specifications** for the interpolation and dead-reckoning routines. The documentation provides high-level architectural descriptions of the rendering behavior:

### 1. Interpolation Method (Linear vs. Great-Circle / Slerp)
* **What the sources state:** The engine "interpolates telemetry data one step behind real-time" [1] and "interpolates between known fixes" [2, 3] to ensure smooth visual movement despite choppy API arrival [2, 3].
* **What is missing:** The sources **do not specify** the mathematical interpolation function used (e.g., whether position coordinates use linear interpolation, great-circle calculations, or spherical linear interpolation / slerp) [1-3].

---

### 2. Per-Frame Tick Rate
* **What the sources state:** The module in `src/data/iconOrientation.js` calculates screen-space projections and heading alignments on a "per-frame" basis [2-4].
* **What is missing:** The documentation **does not state a specific numeric tick rate** or target frame rate (e.g., 60 Hz or `requestAnimationFrame` loop specifications) [2-4].

---

### 3. Heading & Velocity in Dead-Reckoning Extrapolation
* **What the sources state:** Icons point along their "true real-world heading" at every camera angle via per-frame screen-space course projection [2, 3], and "dead reckoning fills the gaps" [1-3] across 15–30 second polling windows [1-3].
* **What is missing:** The sources **do not document the dead-reckoning formula**, nor do they explicitly state whether velocity and track vectors from the raw ADS-B telemetry payload are ingested to extrapolate position between updates [1-4].

---

### 4. Client Behavior on Missed or Late Fixes
* **What the sources state:** Holding rendering "one interval behind real time" buffers against minor feed delays [1-3]. If OpenSky experiences an outage or has no usable snapshot, the local proxy fails over to a cached, capped 250 nautical-mile `adsb.lol` point snapshot around the current camera subpoint [5].
* **What is missing:** The sources **do not document client-side timeout thresholds**, entity purging logic, or coasting/removal behaviors when an individual aircraft's telemetry fix is missed or indefinitely delayed [1-3, 5].

---

💡 *Would you like to examine how other live feeds—such as the CelesTrak satellite layer using client-side SGP4 orbital propagation—handle positional rendering between updates?*

**Follow-up: The 1.86s Cold-Start Benchmark Conditions**

Based on the available project documentation, the specific parameters of that benchmark run are omitted:

* **Concurrent Aircraft Entities:** The sources **do not record the number of live aircraft entities** present in the scene during that capture [1].
* **Number of Benchmark Runs:** The sources **do not state how many runs** were conducted to calculate the median [1, 2].
* **Definition of "Settle":** The sources **do not provide a technical definition for "settle"**—they do not clarify whether "initial settle" refers to time-to-first-frame, complete entity placement/rendering, or reaching a stable frame rate [1].

### What the Sources Do Record
The documentation only provides the high-level environmental metadata for the benchmark [1]:
* **Environment:** Apple M5 processor, Chrome 150 [1].
* **Viewport Resolution:** 1440×900 [1].
* **Capture Date:** August 22, 2026 [1].
* **Result:** **1.86-second median cold start / initial settle**, referenced in `docs/PERFORMANCE.md` as a point-in-time regression baseline rather than a performance guarantee across hardware [1, 2].

---

💡 *Would you like to examine how automated CI performance checks use Node.js allocation microbenchmarks to catch memory leaks during builds?*

**Follow-up: Glyph-to-3D LOD Swap Threshold**

Based on the project documentation, the precise numerical triggers and memory caps for 3D model rendering are not explicitly documented:

### 1. Glyph-to-3D Model Swap Trigger
* **What the sources state:** The system uses 2D billboard glyphs for distant traffic and automatically swaps a contact from a 2D glyph to a 3D `.glb` airframe model **"as you close in"** [1, 2] for **"close-range tracking"** [3].
* **What is missing:** The sources **do not specify an exact numerical threshold**—such as a specific camera altitude in meters, viewing distance, or screen-space pixel size—that triggers this LOD transition.

---

### 2. Resident Model Limit During Handoffs
* **What the sources state:** To manage browser performance and prevent rendering slowdowns during close-up views, performance optimization is handled at the asset level [3, 4]:
  * **Texture Optimization:** PBR textures are downscaled to 256px WebP format [4].
  * **Geometry Optimization:** Polycounts and hierarchies are simplified/flattened, with orientation offsets vertex-baked directly into the mesh [4].
  * **Decoder Budgeting:** Core assets (like `airplane.glb`) remain uncompressed to avoid saturating GPU/Draco decoding capacity during dynamic loading [4].
* **What is missing:** The documentation **does not record an explicit numerical cap** on how many 3D models can be loaded into memory or rendered simultaneously on the globe at one time.

---

💡 *Would you like to review the specific per-model optimization parameters (such as vertex baking and coordinate axis alignments) used across the shipped aircraft models in `public/models/`?*

**Follow-up: Stale-Fix Failover Path and the 250 NM adsb.lol Cache**

### 1. Trigger for Switchover
* **What the sources state:** The failover to `adsb.lol` is initiated *"When OpenSky is unavailable and no last-good OpenSky response exists"* [1].
* **What is missing:** The documentation does not specify the exact technical trigger criteria—such as a specific HTTP timeout threshold in milliseconds, a required number of consecutive missed polling attempts, or specific HTTP error codes [1].

---

### 2. Cache Duration & Aging Out / Entity Dropping
* **What the sources state:** When activated, the server requests a *"cached, capped 250 nm adsb.lol point snapshot around the current camera subpoint"* to provide regional context [1].
* **What is missing:** The sources do not record how long a cached telemetry fix is permitted to drive an aircraft's position, nor do they define an explicit time-to-live (TTL), stale-data timeout, or entity removal threshold after which an un-updated flight is dropped from the globe [1].

---

### 3. Client Staleness & Provenance Indicators
* **What the sources state:** Rather than displaying a per-aircraft staleness timer, the application surfaces feed origin at the layer level: *"provenance is exposed in the Flights stats/context row"* whenever the fallback snapshot is active [1].
* **What is missing:** The sources do not mention any individual entity-level staleness badges, icon color shifts, or visual age indicators on the aircraft model or telemetry card [1].

---

💡 *Would you like to examine how other live feeds—such as the Launch Library 2 space missions layer—handle server-side disk caching and stale response serving during API outages?*

**Follow-up: What iconOrientation.js Actually Consumes Per Frame**

According to the project documentation, the low-level code implementation details for `src/data/iconOrientation.js` are not fully detailed:

### 1. Telemetry Heading vs. Derived Bearing Input
* **What the sources state:** The module in `src/data/iconOrientation.js` calculates screen-space course projections so that icons point along their **"true real-world heading"** relative to the virtual camera viewport [1, 2].
* **What is missing:** The documentation **does not specify** whether the input passed into `iconOrientation.js` is an explicit heading/track field extracted directly from the telemetry payload or a bearing computed mathematically from successive interpolated position fixes.

---

### 2. Driving Loop (Render Callback vs. `requestAnimationFrame` vs. Timer)
* **What the sources state:** The screen-space orientation alignment and horizon culling calculations occur on a **"per-frame"** basis [1-3].
* **What is missing:** The sources **do not state the specific JavaScript loop mechanism** driving this per-frame execution—such as a CesiumJS scene render event listener (`viewer.scene.preRender` / `postRender`), a native browser `requestAnimationFrame` loop, or a timer interval.

---

### Documented Scope of `src/data/iconOrientation.js`
The project files record the specific responsibilities of this module as:
1. **Screen-Space Course Projection:** Preventing standard 2D billboard icons from spinning, distorting, or locking to the viewport when the camera pitches toward the horizon [1, 2].
2. **Horizon Culling:** Performing screen-projected horizon culling to suppress icons that fall beyond the horizon or behind the Earth's curvature [3, 4].

---

💡 *Would you like to examine how other core frontend modules in `src/` (such as `mapStackController.js` or `hud.js`) interact with the CesiumJS viewer instance?*

**Follow-up: LOD Swap Implementation in Code**

**The provided sources do not contain the underlying source code or configuration constants that dictate the billboard-to-3D (`.glb`) model swap.** Consequently, the documentation does not specify whether the rendering logic evaluates camera altitude, distance-to-contact, or screen-space pixel size, nor does it identify the specific file or variable where that threshold value is defined.

### What the Sources Do Confirm:
* **Swap Behavior:** The rendering engine automatically replaces 2D billboard glyphs with detailed 3D `.glb` models for "close-range tracking" as the camera "closes in" on a contact [1, 2].
* **3D Model Catalog:** Per-class 3D assets (including `airplane.glb`, `b789.glb`, `atr72.glb`, `bell206.glb`, `c172.glb`, `citation2.glb`, `mq9.glb`, and `ship.glb`) are stored in `public/models/` and optimized with vertex-baked transforms and 256px WebP textures to minimize GPU overhead during close-up tracking [1-3].
* **Codebase Structure:** Entity rendering and layer-specific state logic are modularized in `src/data/<layer>.js` (e.g., `src/data/flights.js`) on top of **CesiumJS** [4-6].

---

💡 *Would you like to explore how other entity visual properties—such as screen-space heading alignment or horizon culling in `src/data/iconOrientation.js`—are documented in the project architecture?*

**Follow-up: 256px WebP and Uncompressed airplane.glb Basis**

Both of these optimization decisions come directly from the asset documentation file **`public/models/README.md`** (cited in the *Architectural Analysis of the God's Eye View Spatial Intelligence Platform*) [1, 2].

### 1. Documented Source and Rationales
* **`airplane.glb` Uncompressed:** `public/models/README.md` states that `airplane.glb` *"remains uncompressed to preserve Draco decoding capacity"* during dynamic loading [1].
* **256px WebP Textures:** The same source specifies that PBR textures across several models (e.g., `b789.glb`, `bell206.glb`, `c172.glb`, `citation2.glb`) were resized to **256px WebP** format as a geometry and texture optimization for browser and mobile rendering [1].

---

### 2. Benchmark Status & Numbers
* **No Benchmark Numbers Recorded:** The sources **do not provide any measured frame-rate, GPU memory, or decode-time benchmark numbers** behind these specific choices [1-3].
* **Convention vs. Benchmark:** They appear in the repository documentation as **design rules of thumb and asset preparation conventions** rather than empirical benchmarks [1, 2]. 

*(The only performance benchmark recorded in the project documentation is an unrelated point-in-time cold-start measurement of a 1.86-second median initial settle on an Apple M5 / Chrome setup [3-5]).*

---

💡 *Would you like to examine how other 3D assets in `public/models/` (such as `atr72.glb` using flat PBR factor colors instead of textures) are configured?*

**Follow-up: OpenSky Failover Trigger Implementation**

That detail is **genuinely absent** from the project's documentation. The sources do not define what constitutes "unavailable" at the code level [1].

Specifically, the notebook sources **do not document**:
* **HTTP Status Code Logic:** How the server differentiates between rate-limit throttling (HTTP 429), server errors (HTTP 5xx), or network failures.
* **Timeout & Retry Limits:** Numerical timeout thresholds in milliseconds or exponential backoff/retry attempt counts.
* **Payload Validation:** Whether an empty-but-successful state-vector payload (`200 OK` with zero aircraft rows) is treated as a valid response or flags the feed as degraded/unavailable.

### What the Sources Do Record Regarding OpenSky Fallback
* **Trigger Condition:** The fallback executes *"When OpenSky is unavailable and no last-good OpenSky response exists"* [1].
* **Credit Governor:** Server-side OpenSky requests run through an internal "credit governor" to throttle polling and manage request budgets [2].
* **Fallback Endpoint & Scope:** When activated, the server requests a cached, regional **250 nautical-mile point snapshot** centered around the active camera ground subpoint from `api.adsb.lol` rather than attempting a global snapshot [1, 3].
* **UI Provenance:** When active, feed origin is exposed directly to the user in the Flights stats/context row [1].

---

💡 *Would you like to examine how other layers in the repository (such as Launch Library 2 or Radio Browser) define stale-cache retention or degraded-payload policies during API outages?*

**Follow-up: Last-Good Snapshot Lifetime and Entity Aging**

Both of these implementation details are **absent from the project documentation**:

### 1. Storage and Expiration of the "Last-Good" OpenSky Snapshot
The sources state that when OpenSky becomes unavailable, the proxy relies on a "last-good OpenSky response" before triggering the regional `adsb.lol` fallback [1]. However, the documentation **does not specify whether this snapshot is stored in-memory or on disk**, nor does it define a maximum age or time-to-live (TTL) limit before the snapshot stops being considered usable [1]. 

By contrast, the documentation explicitly defines the cache mechanisms for several other data feeds in the platform:
* **Launch Library 2:** Cached for 15 minutes in memory and on disk [1].
* **TomTom Traffic:** Cached transiently for \\(\le\\)120 seconds on disk under `.gev-cache/` [2].
* **Radio Browser Directory:** Cached for 45 minutes, and can be served stale for up to 7 days during an outage [1].
* **Open-Meteo Weather:** Cached for 5 minutes, and can be served stale for up to 30 minutes [2].

No corresponding TTL or storage location is documented for the OpenSky flight buffer [1].

---

### 2. Client-Side Entity Pruning for Omitted Flights
The sources **do not document the client-side entity removal policy** when an aircraft is omitted from a subsequent telemetry payload [3, 4]. 

The documentation details that live flight feeds arrive every 15–30 seconds, with the rendering engine running one step behind real time to interpolate positions and fill short gaps via dead reckoning [3, 4]. However, the sources do not specify the timeout threshold, aging-out logic, or removal triggers that dictate whether an omitted entity is pruned from the WebGL scene or left rendered at its last known position [3, 4].

---

💡 *Would you like to examine how other layers—such as the CelesTrak satellite propagation module or city CCTV viewsheds—handle client-side state cleanup and entity updates?*

**Follow-up: Actual Implementation of iconOrientation.js**

The exact function signature, accepted parameters, and call sites for `src/data/iconOrientation.js` are **not present in the provided source materials** [1, 2]. Because the raw source code for this specific JavaScript file is not included in the repository documentation or project text passages, those code-level implementation details cannot be verified [1].

### What the Sources Do Confirm About `src/data/iconOrientation.js`:
* **File Purpose & Location:** `src/data/iconOrientation.js` is a dedicated helper module within the `src/data/` directory responsible for per-frame screen-space icon alignment and horizon culling [1, 3].
* **Screen-Space Course Projection:** It computes screen-space projections on a per-frame basis so that 2D billboard glyphs (such as aircraft and ships) maintain their true real-world heading relative to the camera viewport, preventing icons from spinning, distorting, or locking to the viewport when the camera pitches toward the horizon [2, 4].
* **Horizon Culling:** It performs screen-projected horizon culling to suppress and hide icons that fall beyond the visible horizon or behind the Earth's curvature [3, 5].

---

💡 *Would you like to examine how other documented modules in `src/data/` (such as layer orchestration or the local context store) interface with the rest of the application?*

**Follow-up: Horizon Culling Trigger Conditions**

The specific test and numerical thresholds used for horizon culling are **not specified in the sources** [1, 2]. The project documentation does not state whether the culling logic uses an ellipsoid occlusion check, a camera-pitch threshold, or a screen-space Y cutoff, nor does it record any specific cutoff values [1, 2].

### What the Sources Do Document:
* **Responsible Module:** Screen-projected heading alignment and horizon culling are managed by `src/data/iconOrientation.js` [1, 3].
* **Execution & Purpose:** Calculations run on a **per-frame basis** to project entity headings in screen space and perform horizon culling [1, 2]. This prevents 2D billboard icons (such as aircraft and ships) from spinning, distorting, or locking to the viewport when the camera pitches toward the horizon, while hiding entities that fall beyond the horizon or behind the Earth's curvature [2, 4].

---

💡 *Would you like to explore how other visual layers—such as the custom GLSL post-processing sensor shaders (NVG, FLIR, CRT)—are structured in the rendering pipeline?*

### Angle Battery

</details>

