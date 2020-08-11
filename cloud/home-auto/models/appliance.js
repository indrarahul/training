const mongoose = require('mongoose')

const appliancesSchema = new mongoose.Schema({
        name: {
            type: String,
            required: true
        },
        status: {
            type: Boolean,
            required: true
        },
        createdDate:{
            type: String,
            required: true,
            default: Date.now
        }
})

module.exports = mongoose.model('Appliance', appliancesSchema)