var express = require('express')

var router = express.Router();

router.get('/:type', (req, res, next) => {
  console.log("Generating", req.params.type);
  res.send(req.params.type);
});

module.exports = router;
