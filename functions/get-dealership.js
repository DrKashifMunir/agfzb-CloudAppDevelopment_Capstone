const express = require('express');
const app = express();
const port = process.env.PORT || 3000;
const Cloudant = require('@cloudant/cloudant');

// Initialize Cloudant connection with IAM authentication
async function dbCloudantConnect() {
    try {
        const cloudant = Cloudant({
            plugins: { iamauth: { iamApiKey: '6hTuzp8tXaRUItaIcw6dwp0DLa3w69sOYX-Bk6jhGNxh' } }, // Replace with your IAM API key
            url: 'https://c8f78e70-1d9c-4431-b283-fd0b33dfcb62-bluemix.cloudantnosqldb.appdomain.cloud', // Replace with your Cloudant URL
        });

        const db = cloudant.use('dealerships');
        console.info('Connect success! Connected to dealerships DB');
        return db;
    } catch (err) {
        console.error('Connect failure: ' + err.message + ' for Cloudant dealerships DB');
        throw err;
    }
}

async function db2CloudantConnect() {
    try {
        const cloudant = Cloudant({
            plugins: { iamauth: { iamApiKey: '6hTuzp8tXaRUItaIcw6dwp0DLa3w69sOYX-Bk6jhGNxh' } }, // Replace with your IAM API key
            url: 'https://c8f78e70-1d9c-4431-b283-fd0b33dfcb62-bluemix.cloudantnosqldb.appdomain.cloud', // Replace with your Cloudant URL
        });

        const db2 = cloudant.use('reviews');
        console.info('Connect success! Connected to reviews DB');
        return db2;
    } catch (err) {
        console.error('Connect failure: ' + err.message + ' for Cloudant reviews DB');
        throw err;
    }
}


let db;
let db2;

(async () => {
    db = await dbCloudantConnect();
})();

(async () => {
    db2 = await db2CloudantConnect();
})();


app.use(express.json());

// Define a route to get all dealerships with optional state and ID filters
app.get('/dealership', (req, res) => {
    const { state, id } = req.query;

    // Create a selector object based on query parameters
    const selector = {};
    if (state) {
        selector.state = state;
    }
    
    if (id) {
        selector.id = parseInt(id); // Filter by "id" with a value of 1
    }

    const queryOptions = {
        selector,
//        limit: 10, // Limit the number of documents returned to 10
    };

    db.find(queryOptions, (err, body) => {
        if (err) {
            console.error('Error fetching dealerships:', err);
            res.status(500).json({ error: 'An error occurred while fetching dealerships.' });
        } else {
            const dealerships = body.docs;
            res.json(dealerships);
        }
    });
});

// Define a route to get all reviews with optional dealership ID filter
app.get('/review', (req, res) => {
    const {dealership} = req.query;
    // Create a selector object based on query parameters
    const selector = {};
    if (dealership) {
        selector.dealership = parseInt(dealership); // Filter by "id" with a value of 1
    }

    const queryOptions = {
        selector,
    };

    db2.find(queryOptions, (err, body) => {
        if (err) {
            console.error('Error fetching dealerships:', err);
            res.status(500).json({ error: 'An error occurred while fetching dealerships.' });
        } else {
            const reviews = body.docs;
            res.json(reviews);
        }
    });
});


// Define a route to post a review
app.post('/review', (req, res) => {
    const { id, name, dealership, review, purchase, another, purchase_date, car_make, car_model, car_year } = req.body;
    
    // Validate required parameters
    if (!review) {
        return res.status(400).json({ error: 'Invalid request. Review is required.' });
    }

    // Create the document to be added to the database
    const reviewDocument = {
        id: id,
        name: name,
        dealership: parseInt(dealership),
        review: review,
        purchase: purchase || false,
        another: another,
        purchase_date: purchase_date,
        car_make: car_make,
        car_model: car_model,
        car_year: car_year,
    };

    console.log(reviewDocument)

    // Insert the document into the database
    db2.insert(reviewDocument, (err, body) => {
        if (err) {
            console.error('Error adding review:', err);
            return res.status(500).json({ error: 'An error occurred while adding the review.' });
        } else {
            return res.json({ success: true, id: body.id, rev: body.rev });
        }
    });
});



app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});