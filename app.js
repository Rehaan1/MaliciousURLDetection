require('dotenv').config()

const express = require('express')
const {spawn} = require('child_process')
const cors = require('cors')

const urlTest = require('./api/routes/urlTester')

const app = express()

app.use(express.urlencoded({ extended: true }))
app.use(express.json())

app.use(cors())

app.use('/testURL', urlTest)

const port = process.env.PORT

app.get('/', (req,res) => {
    
    res.json({
        "Status": "API Up and Running, Use testURL Endpoint"
    })
})


app.listen(port, () => {
    console.log('Listening on Port:',port)
})