## <a name="project-overview"></a>Project Overview
This Django project is web scraping, data processing, data visualization and a MySQL-backed Django application.

Project link: https://github.com/shown440/scraping\_project

-----
## <a name="prerequisites"></a>Prerequisites
Before you begin, ensure you have the following installed:

- Python 3.12+ (recommended)
- Git
- MySQL server (or another supported database)
- Virtual environment tool (venv, virtualenv)
- System dependencies for mysqlclient (on Ubuntu/Debian):

  sudo apt-get update
  sudo apt-get install default-libmysqlclient-dev build-essential

  sudo apt install python3.12 python3.12-venv python3.12-dev python3-pip -y 
-----
## <a name="installation-steps"></a>Installation Steps
1. **Clone the repository**

   git clone git@github.com:shown440/scraping\_project.git
   cd scraping\_project
1. **Create a virtual environment and activate it**

   python3.12 -m venv sebpo\_scrap\_env\_312
   source sebpo\_scrap\_env\_312/bin/activate
1. **Install Python dependencies**

   pip install --upgrade pip
   pip install -r requirements.txt
-----
## <a name="configuration"></a>Configuration
1. **Environment variables**

   Already inserted inside the code, because It’s anon production project.

-----
## <a name="database-setup-and-migrations"></a>Database Setup and Migrations
1. **Create the database** in MySQL:

   **1. Login inside mysql database**

   **2. CREATE** **DATABASE** sebpo\_scrap\_db;

   **3. GRANT ALL PRIVILEGES ON sebpo\_scrap\_db.\* TO 'ffwc'@'localhost';**

   **4. FLUSH PRIVILEGES;**

   **5. Exit**

   **6. Restore dumped mysql db: mysql -u db\_username -p sebpo\_scrap\_db < sebpo\_scrap\_db.sql**

1. **Apply migrations**:

   1. python3.12 manage.py makemigrations

   1. python3.12 manage.py migrate
1. **Create a superuser** (for admin access):

   python3.12 manage.py createsuperuser
-----
## <a name="running-the-development-server"></a>Running the Development Server
Start Django’s built-in development server:

Python3.12 manage.py runserver then it will run is:  0.0.0.0:8006

Visit http://127.0.0.1:8006/ in your browser.

-----
## <a name="running-scheduled-and-custom-commands"></a>Running Scheduled and Custom Commands
- **Daily scraping task**:

  python3.12 manage.py fetch\_cia\_data
- **Daily scraping task** via cron:

  1. goto project folder

  2. go to: /accessories/bash\_script\_and\_crontab/bash\_script/fetch\_cia\_data.sh

  3. find: “/var/www/prod/scraping\_project” then replace with your project path

  4. find: “/var/www/Project\_Environments/python\_environments/sebpo\_scrap\_env\_312

  ” then replace with your python environment path

  5. then provide permission update cia\_data.sh: sudo chmod 777 /var/www/prod/scraping\_project/accessories/bash\_script/fetch\_cia\_data.sh

  6. now write in terminal: sudo crontab -e

  Then: 20 15 \* \* \* /var/www/prod/scraping\_project/accessories/bash\_script/fetch\_cia\_data.sh

  Then: save and exit



-----
## <a name="static-files-production"></a>Static Files (Production)
1. Collect static assets:

   python3.12 manage.py collectstatic
1. Configure your web server (e.g., Nginx) to serve the static/ directory.

-----
## <a name="running-tests"></a><a name="deployment"></a>Deployment
For deploying to production, consider using:

- **Gunicorn + Nginx** 

**Gunicorn service:** Goto the path:  ../scraping\_project/accountable\_services/ubuntu\_server/scrap\_webservice\_port.service

1. find: “/var/www/Project\_Environments/python\_environments/sebpo\_scrap\_env\_312” then replace with your python environment path
1. Create Command: sudo nano scrap\_webservice\_port.service

And paste updated command inside here from: ../scraping\_project/accountable\_services/ubuntu\_server/scrap\_webservice\_port.service

1. Enable Command: sudo systemctl enable scrap\_webservice\_port.service
1. Start Command: sudo systemctl start scrap\_webservice\_port.service
1. Restart Command: sudo systemctl scrap\_webservice\_port.service
1. Monitoring Command: sudo systemctl status scrap\_webservice\_port.service

**Nginx configuration process:** Goto the path:  ../scraping\_project/accountable\_services/ubuntu\_server/scrap\_ng\_port

1. find: “/var/www/prod/scraping\_project” then replace with your python project path
1. find: “scrap.sebpo.com” then replace with your own domain
1. then copy the whole command and goto: sudo nano /etc/nginx/sites-available/scrap\_ng\_port and paste and save it
1. Link the Configuration File: sudo ln -s /etc/nginx/sites-available/ scrap\_ng\_port /etc/nginx/sites-enabled/
1. sudo nginx -t
1. sudo systemctl restart nginx

1. If need to https the we can use certbot to do that:
   1. Then install: pip install certbot certbot-nginx
   1. Renew https domain: sudo certbot –nginx
   1. sudo systemctl restart nginx

-----
## <a name="contributing"></a>Explanations of features:
1. **How the scraper works?:** 

   The scraper fetches CIA agreement data from the OIG website in three key steps:

1. **Data Extraction**
   1. Iterates through A-Z pages to scrape provider records
   1. Parses HTML tables using BeautifulSoup
   1. Captures provider names, locations, effective dates, and document links
1. **Change Detection**
   1. Generates SHA-256 hashes for each record
   1. Compares hashes with previous database pull
   1. Identifies added/removed records since last run
1. **Database Operations**
   1. Creates new DataPull entry for each execution
   1. Stores raw data in CIAData table
   1. Logs changes in DataChange table (additions/removals)
   1. Marks pull as processed after completion

The process tracks data evolution by comparing cryptographic hashes between runs, efficiently detecting changes without storing full historical datasets.


1. **How the refresh button works?:**   
   1. User Click:
- Clicking the "Refresh Data" button triggers a JavaScript event.
  1. Background Process Start:
- The button hides, and a "Processing..." spinner appears.
- A request is sent to Django's start\_processing URL.
- Django launches a background thread to scrape/process CIA data without blocking the user.
  1. Data Processing:
     1. Scrapes the latest CIA data from the OIG website.
     1. Compares new data with the previous pull to detect additions/removals.
     1. Logs changes in the database (DataChange model).

1. Auto-Refresh on Completion:
   1. JavaScript checks the dashboard every 3 seconds.
   1. When the "Latest Pull" timestamp updates, the page reloads automatically.
   1. The UI displays new changes (added/removed records).

1. Key Flow:

Click → Hide Button → Start Thread → Scrape → Compare → Save Changes → Detect Update → Reload Page

1. **How differences are displayed?:**   

   The differences are displayed in a **categorized, side-by-side format** based on change type:

1. **Added Items**:
   Added: [New Data]
   *(Shows only the new state)*
1. **Removed Items**:
   Removed: [Old Data]
   *(Shows only the previous state)*
1. **Modified Items**:
   Changed from: [Old Data] to [New Data]
   *(Directly compares previous → current values)*

Key features:

- Color-coded change types (visual distinction)
- Raw HTML rendering (|safe filter preserves formatting)
- Tabular layout with provider context
- Summary statistics at top (added/removed/modified counts)

1. **How latest data are displayed?:**   

Here's a concise explanation of how the latest data is displayed:

1. **Latest Data Pull**: The most recent DataPull entry is fetched from the database.
1. **Time Conversion**: The pull time is converted to GMT+6 and displayed in YYYY-MM-DD HH:MM format.
1. **Paginated Records**: Associated records from CIAData are displayed in a table with 25 entries per page.
1. **Table Structure**: Each row shows:
   1. Provider
   1. City
   1. State
   1. Effective Date
1. **Pagination Controls**: Users can navigate between pages using first/previous/next/last links.
1. **Fallback Handling**: Shows "No records found" if data is empty or "No data pulls available" if no pull exists.

Output is always timezone-adjusted and paginated for clarity.

1. **How authentication is enforced?:**   

   Authentication is enforced by applying the @login\_required **decorator** to every view function. This:

   1. **Restricts access** to authenticated users only.
   1. **Redirects unauthenticated users** to Django's default login page (handled internally).
   1. **Uses Django's built-in session-based authentication** system (no custom logic needed).
   1. **Result:** All routes (e.g., /dashboard, /history) are automatically protected. Unauthenticated requests get redirected to login.

**(Implementation: Decorators wrap each view, checking request.user.is\_authenticated behind the scenes.)**

1. **How to set up scheduled scraping?:**   
   1. Customize Paths

Edit fetch\_cia\_data.sh:

1. Replace /var/www/prod/scraping\_project with your project path.
1. Replace /var/www/Project\_Environments/... with your Python environment path.

1. Grant Script Permissions

Run:

1. sudo chmod 777 /path/to/fetch\_cia\_data.sh
1. Schedule in Cron

Execute:

1. sudo crontab -e

Add this line (runs daily at 15:20 or 3:20 pm):

1. 20 15 \* \* \* /path/to/fetch\_cia\_data.sh

Save and exit.

1. Schedule Syntax: 20 15 \* \* \*
   1. 20 → Minute 20 (of the hour)
   1. 15 → Hour 15 (3 PM in 24-hour time)
   1. \* → Every day of the month
   1. \* → Every month
   1. \* → Every day of the week (Monday-Sunday)



-----
## <a name="license"></a>Contributing
1. Fork the repository
1. Create a feature branch (git checkout -b feature/XYZ)
1. Commit your changes (git commit -m "Add XYZ feature")
1. Push to the branch (git push origin feature/XYZ)
1. Open a Pull Request
-----


