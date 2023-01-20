const express = require('express')
const {spawn} = require('child_process')

const app = express()
const port = 3000

app.get('/', (req,res) => {
    
    var dataToSend;
    
    // spawn new child process to call the python script
    const python = spawn('python', ['-c', 'import mlData.malicious as malicious; malicious.check_if_malicious("http://www.garage-pirenne.be/index.php?option=com_content&view=article&id=70&vsig70_0=15")'])

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


app.listen(port, () => {
    console.log('Listening on Port:',port)
})