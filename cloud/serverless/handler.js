const rp = require('request-promise');
const TELEGRAM_TOKEN = '994345313:AAEJNJjBddtkx5v3t-KRc5WJJLCqIcV9aO0';

async function switchOn() {
  const status = {
    method: 'GET',
    uri: 'http://3.235.245.51/v1/on'
  };
  return rp(status);
}

async function switchOff() {
  const status = {
    method: 'GET',
    uri: 'http://3.235.245.51/v1/off'
  };
  return rp(status);
}

async function sendToUser(chat_id, text) {
  const options = {
    method: 'GET',
    uri: `https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage`,
    qs: {
      chat_id,
      text
    }
  };

  return rp(options);
}

module.exports.homeauto = async event => {
  const body = JSON.parse(event.body);
  const {chat, text} = body.message;

  if (text=="on") {
    let message = '';
    try {
      const result = await switchOn();
      const jsonResult = JSON.parse(result)
      message = `Status: ${jsonResult.status}`;
    } catch (error) {
      message = `Error: ${error.message}`;
    }
    await sendToUser(chat.id, message);
  
  } else if (text=="off"){
    let message = '';
    try {
      const result = await switchOff();
      const jsonResult = JSON.parse(result)
      message = `Status: ${jsonResult.status}`;
    } catch (error) {
      message = `Error: ${error.message}`;
    }
    await sendToUser(chat.id, message);
  }
  else {
    await sendToUser(chat.id, 'Text message is expected.');
  }

  return { statusCode: 200 };
};
