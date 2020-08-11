const express = require("express");
const router = express.Router();
const Appliance = require("../models/appliance");

router.get("/on", getAppliance, async (req, res) => {
    if(req.body.name != null) {
        res.appliance.name= req.body.name
    }
        res.appliance.status= true
    
        try {
            const updateAppliance = await res.appliance.save()
            res.json(updateAppliance)
        } catch (err) {
            res.status(400).json({message: err.message})
        }
});

router.get("/off", getAppliance, async (req, res) => {
    if(req.body.name != null) {
        res.appliance.name= req.body.name
    }
        res.appliance.status= false
    
        try {
            const updateAppliance = await res.appliance.save()
            res.json(updateAppliance)
        } catch (err) {
            res.status(400).json({message: err.message})
        }
});

router.post("/", async (req,res) => {
    const appliance = new Appliance({
        name : req.body.name,
        status: req.body.status
    })
    try {
        const newAppliance = await appliance.save()
        res.status(201).json(newAppliance)
    } catch (err) {
        res.status(400).json({message: err.message})
    }
})

async function getAppliance(req, res, next) {
    let appliance
  try {
      appliance = await Appliance.findById("5f3300651d94a136c7167f06")
      if (appliance == null ){
          return res.status(400).json({message : 'Can\'t find the appliance'})
      }
  } catch (err) {
    return res.status(500).json({message : err.message})
  }

  res.appliance = appliance
  next()
}

module.exports = router;
