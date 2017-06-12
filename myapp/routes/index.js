var express = require('express');
var router = express.Router();
var bodyParser = require('body-parser');
const exec = require('child_process').exec;

router.use(bodyParser.json());
/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: '' });
});

router.post('/', function(req, res, next) {
  console.log(req.body.mytext);
  var prog = "score_app_web.py " + '"' + req.body.mytext + '"';
  exec(prog, (err, stdout, stderr) => {
		if (err) {
			console.error(err);
			return;
		}
		console.log(stdout);
		//var result = eval(stdout);
		//var result = stdout;
		var result = JSON.parse(stdout);
		
		var k = 'None', v = 0;
		
		var mdata = ''
		for (var r in result){
			if (v < result[r]){
				k = r;
				v = result[r];
			}
			mdata += r + ': ' + result[r] + " | ";
		}
		
		console.log(result['gary']);
		res.render('index', { typed: req.body.mytext, result: k, data: mdata});
	});
});
module.exports = router;
