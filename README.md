# Bharat Coking Coal Limited - Production Analytics Portal

A comprehensive web application for tracking and analyzing coal production across multiple mining areas with advanced analytics and issue tracking capabilities.

## Problem Statement

Coal production teams manage data scattered across spreadsheets and static PDF reports. This makes it hard to get timely insights on targets vs actuals, identify operational issues across areas/coalfields, and communicate performance trends to leadership. Manual consolidation is slow, error‑prone, and limits proactive decision‑making.

## How This Helps

- **Single source of truth**: Upload area/coalfield reports (PDF/Excel/CSV) and capture monthly entries in one place.
- **Instant visuals**: Auto‑generated single or multi‑line graphs for distributions and trends; issue overlays for context.
- **Performance focus**: KPIs (performance %, variance) at area and overall levels.
- **Faster decisions**: Spot under‑performance, correlate with issues (land, climate, other), and act quickly.

## Features

### 🏗️ Initial Setup
- Configure number of mining areas (1-20)
- Set time duration for tracking (1-24 months)
- Dynamic system initialization

### 📊 Data Entry Interface
- Monthly data entry for each area
- Expected vs actual coal output tracking
- Real-time performance indicators
- Issue categorization system

### 📑 Document Ingestion (PDF/Excel/CSV)
- Upload area-wise coal distribution reports (single line graph when area + output)
- Upload other reports (multi-line graphs auto-detected by table structure)
- Robust PDF table and text parsing with numeric coercion

### 📈 Analytics Dashboard
- **Individual Area Analytics**: Green lines for expected production, red lines for actual production
- **Issue Visualization**: Green indicators for land acquisition issues, yellow for climate issues
- **Overall Production Dashboard**: Combined analytics across all areas
- **Performance Metrics**: Detailed KPIs and variance analysis

### 🎨 Professional UI
- Dark theme optimized for industrial environments
- Color-coded analytics with intuitive visual indicators
- Responsive design for various screen sizes
- Professional coal industry styling

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation Steps

1. **Clone or download the project files**
   ```bash
   # Ensure you have the following files in your project directory:
   # - app.py
   # - requirements.txt
   # - README.md
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Access the application**
   - Open your web browser
   - Navigate to `http://localhost:8501`
   - The application will automatically open in your default browser

## Deploy to Streamlit Community Cloud (free)

1. Push this folder to a public GitHub repository.
2. Go to `https://streamlit.io` > Sign in > Deploy an app.
3. Connect your GitHub repo, select branch and `app.py` as the entry point.
4. Add optional secrets in `App settings` if needed.
5. Deploy. Your app will get a public URL and is installable as a PWA.

## Usage Guide

### Step 1: Initial Setup
1. On the Setup page, enter the number of mining areas to track
2. Set the time duration in months for your analysis period
3. Click "Initialize Production Tracking" to create the system

### Step 2: Data Entry
1. Navigate to "Data Entry" page
2. Select the month and area for data entry
3. Enter expected and actual coal output values
4. Check relevant issue categories if applicable:
   - **Land Acquisition Issues**: Check if production was affected by land-related problems
   - **Climate Calamities**: Check if production was affected by climate events
5. Click "Save Data" to store the information

### Step 3: Analytics Review
1. **Area Analytics**: View individual area performance with line graphs
2. **Overall Dashboard**: Review combined production across all areas
3. Monitor performance metrics and identify trends
4. Use issue indicators to understand production variances

## Key Features Explained

### Color Coding System
- **Green Lines**: Expected coal production targets
- **Red Lines**: Actual coal production achieved
- **Green Indicators**: Land acquisition issues affecting production
- **Yellow Indicators**: Climate issues affecting production

### Performance Metrics
- **Performance Percentage**: Actual vs Expected output ratio
- **Variance**: Difference between actual and expected production
- **Issue Tracking**: Count of land and climate issues per area

### Data Persistence
- All data is stored in session state during your analysis session
- Use the "Reset Session" button to start fresh
- Data is maintained as you navigate between pages

## Technologies Used

- **Streamlit**: Front-end framework for rapid, reactive UI
- **Plotly**: Interactive charts (line, bar, multi-series)
- **Pandas / NumPy**: Data wrangling and calculations
- **pdfplumber**: PDF parsing (tables and text fallback)
- **tabula-py** (optional): Alternative PDF table extraction; requires Java

> Note: If Java is unavailable, the app uses `pdfplumber` and text-based parsing paths.

## Technical Specifications

### Dependencies
- **Streamlit**: Web application framework
- **Plotly**: Interactive data visualization
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **pdfplumber**: PDF parsing
- **tabula-py** (optional): PDF tables via Java

### Browser Compatibility
- Chrome (recommended)
- Firefox
- Safari
- Edge

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # If port 8501 is busy, Streamlit will automatically use the next available port
   # Check the terminal output for the correct URL
   ```

2. **Module not found errors**
   ```bash
   # Ensure all dependencies are installed
   pip install -r requirements.txt
   ```

3. **Data not saving**
   - Ensure you click "Save Data" after entering information
   - Check that the setup has been completed first

### Performance Tips
- For large datasets (20 areas, 24 months), the application is optimized for smooth performance
- Clear browser cache if experiencing display issues
- Use the Reset Session feature to clear memory if needed

## Support

For technical support or feature requests, please contact the development team.

---

**Bharat Coking Coal Limited** - Production Analytics Portal v1.0

