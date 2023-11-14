require('dotenv').config()
const express = require("express")
const path = require('path')
const PORT = process.env.PORT || 5000

const app = express()
app.use(express.json())
app.use(express.static(path.resolve(__dirname, 'static-files')))

const start = async () => {
    try {
        console.log("try start");
        app.listen(PORT, () => console.log(`Server started on port ${PORT}`))

    } catch (e) {
        console.log(e);
    }
}

start()