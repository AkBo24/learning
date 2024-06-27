const routes = (app) => {
    app.route('/contact')
        .get((req, res) => res.send(`GET request`))
        .post((req, res) => res.send(`POST request`));

    app.route('/contact:id')
        .get((req, res) => res.send(`GET request by ID`))
        .put((req, res) => res.send(`PUT request by ID`))
        .get((req, res) => res.send(`DELETE request by ID`));
};

export default routes;
