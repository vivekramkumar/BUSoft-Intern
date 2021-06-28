const express = require('express');
const bodyParser = require('body-parser');
const app = express();
app.use(express.json())
app.set("view engine", "ejs");
app.use(express.static("public"));
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())
let p = require('python-shell');
var x;
app.get('/',function(req,res) {
  //res.sendFile('E:\\intern\\node-js\\form.ejs');
  res.render("form.ejs");
 // res.render("form.ejs",{name:'vivek'})
});




app.post('/send',(req,res)=>{
  console.log(req.body.fname);

  var options = {
      args:
      [
        JSON.stringify(req.body.fname)

      ]
    }
    p.PythonShell.run('test_similar.py', options, function  (err, results)  {

      console.log(results)
        res.render('index.ejs',{name:results});
      //res.send(JSON.parse(results));
      //res.end(); 
    });
   
})

var port=3000;
  app.listen(port, () => {
    console.log(`Server running on port${port}`);
    
  });
