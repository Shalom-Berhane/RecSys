const spawn = require("child_process").spawn;
const fs = require('fs');

const newObject = {
    userId: 99,
    itemId: 5
}

fs.writeFile('./newUserId.json', JSON.stringify(newObject, null, 2), err => {
    if (err) {
        console.log(err);
    } else{
        console.log('File successfully written!');
    }
});

const pyProcess = spawn('python',["GettingStarted.py"]);
pyProcess.stdout.on('data',(data) => {
    // convert to string
    mystr = data.toString();

    // convert string into json
    myjson = JSON.parse(mystr);

    console.log(`Loved once for userId: ${myjson.userId}`);
    console.log(myjson.Loved);
    console.log('---------------------');
    console.log(`recommended for userId: ${myjson.userId}`);
    console.log(myjson.recommended);
})