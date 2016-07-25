# Living Progress - Data to Drops - Multi-Class Data Classification Web App

See https://www.topcoder.com/challenge-details/30054789/?type=develop

## Deployment

Install all dependencies:

    pip install -r requirements.txt

Start the app:

    python app.py

Open the app in your browser: http://localhost:5000

## Testing "Water Source Type"

Choose Water Source Type tab at the top of the page.

For Train, upload "Python Classification Training Data.csv"

For Classify, upload

    * "Python Classification Training Data.csv"
    * "Python Classification Training Data First 10.csv"
    * Any other CSV you want to run the classification on.

You'll get redirected to classify-results with a paginated table of results.

You can export the classified data into a CSV using the Export button.

## Testing "Status"

Choose Status tab at the top of the page.

For Train, upload "status/data/training.csv"

For Classify, upload

    * Any CSV you want to run the classification on (you can choose the same as for Train if you do not have any).

You'll get redirected to classify-results with a paginated table of results.

You can export the classified data into a CSV using the Export button.

## Customizing

The number of results to show per page in classify-results can be changed by
changing the RESULTS_PER_PAGE value in app.py.

You can change the port the server runs on with an env var named `PORT`, like:

    PORT=8000 python app.py
