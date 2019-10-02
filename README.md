# Spacewalk: a web app to find the most disability-accessible walking routes in San Francisco
Project for Insight Data Science Silicon Valley 2019C

Run: ./run.py

Mainfile: views.py

Workflow:
1. Parse the routes offered by the Google Maps Direections API into shapes
2. Merge each step of each route with the provided data files for information on sidewalk and curb status, as well as current construction permits.
3. Score the routes based on sidewalk width, curbs, and conditions
4. Print the highest scoring route to a map and report the sidewalk status to the user

Caveats:
1. The data files here are static permit files from September of 2019, and do not reflect real-time SF construciton permits. For data storage reasons, these files only list permits in the SOMA neighborhood.
2. User must supply a Google Maps Directions API Key.

See the results at www.spacewalk.site

