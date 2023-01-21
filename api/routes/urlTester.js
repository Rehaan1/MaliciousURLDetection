const router = require('express').Router()
const {spawn} = require('child_process')


// Endpoint to Test URL send in query
router.get('/',(req,res) => {
    var dataToSend;
    
    var url = req.query.url;

    // spawn new child process to call the python script
    const python = spawn('python', ['-c', 'import mlData.malicious as malicious; malicious.check_if_malicious("'+url+'")'])

    // collect data from script
    python.stdout.on('data', (data) => {
        console.log('Pipe data from python ....')
        dataToSend = data.toString();
    })

    //in close event we are sure that stream from child process is closed
    python.on('close', (code) => {
        console.log('child process close all stdio with code', code)
        // send data to browser
        res.send(JSON.parse(dataToSend))
    })
})

module.exports = router